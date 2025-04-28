import pygame
import random
import os

class GameGUI:
    def __init__(self, game):
        pygame.init()
        pygame.mixer.init()
        try:
            music_path = os.getcwd() + '/views/gui/assets/sounds/MarwanMoussa-ElBoslaDa3et.mp3'
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)  # softer
            pygame.mixer.music.play(loops= -1,start= 35)  # loop forever
        except pygame.error as e:
            print(f"Failed to load music: {e}")
            print(os.getcwd())
        self.game = game
        self.CELL_SIZE = 40
        self.LAYER_SPACING = 8
        # fixed window for trapezoid style
        self.WIDTH = 600
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('CubiXpert: Galaxy Edition 3D Tic-Tac-Toe')
        font_path = os.path.join(os.getcwd(), 'views/gui/assets/fonts/Consolas.ttf')
        self.font = pygame.font.SysFont(font_path, 32, bold=True)
        self.end_title_font = pygame.font.SysFont(font_path, 24, bold=True)
        self.end_score_font = pygame.font.SysFont(font_path, 22, bold=True)
        self.end_button_font = pygame.font.SysFont(font_path, 20, bold=True)
        self.start_title_font = pygame.font.SysFont(font_path, 80, bold=True)
        self.credits_font = pygame.font.SysFont(font_path, 30, bold=True)
        self.star_positions = [
            (random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT))
            for _ in range(200)
        ]
        self.colors = {
            'dark_bg':       (10, 10, 30),
            'star_color':    (180, 180, 255),
            'grid_color':    (100, 100, 255),
            'x_color':       (0, 255, 255),
            'o_color':       (255, 0, 255),
            'neon_green':    (0, 255, 180),
            'win_line_color':(255, 255, 100),
            'button_bg':     (50, 0, 80, 180),
            'text_color':    (220, 220, 255),
            'white':         (255, 255, 255),
        }

    def draw_starfield(self):
        for pos in self.star_positions:
            pygame.draw.circle(self.screen, self.colors['star_color'], pos, 1)

    def get_grid_position(self, pos):
        mx, my = pos
        N = self.game.BOARD_SIZE
        W = self.WIDTH
        H = self.CELL_SIZE * N
        S = self.LAYER_SPACING
        top_w = W * 0.6
        bot_w = W * 0.8
        # check each layer trapezoid
        for z in range(N):
            top_y = 50 + z * (H + S)
            bot_y = top_y + H
            if my < top_y or my > bot_y:
                continue
            fy = (my - top_y) / H
            left_xt = (W - top_w) / 2
            left_xb = (W - bot_w) / 2
            left_x  = left_xt * (1 - fy) + left_xb * fy
            width   = top_w * (1 - fy) + bot_w * fy
            if mx < left_x or mx > left_x + width:
                return None
            y = int(fy * N)
            fx = (mx - left_x) / width
            x = int(fx * N)
            return (x, y, z)
        return None

    def draw_board(self, last_move=None):
        # clear & stars
        self.screen.fill(self.colors['dark_bg'])
        self.draw_starfield()

        N = self.game.BOARD_SIZE
        W = self.WIDTH
        H = self.CELL_SIZE * N
        S = self.LAYER_SPACING
        top_w = W * 0.6
        bot_w = W * 0.8

        for z in range(N):
            top_x = (W - top_w) / 2
            bot_x = (W - bot_w) / 2
            top_y = 50 + z * (H + S)
            bot_y = top_y + H
            # corners
            pts = [
                (top_x,         top_y),
                (top_x + top_w, top_y),
                (bot_x + bot_w, bot_y),
                (bot_x,         bot_y)
            ]
            # border
            pygame.draw.polygon(self.screen, self.colors['grid_color'], pts, 2)
            # vertical lines
            for i in range(1, N):
                fx = i / N
                start = (top_x + fx * top_w, top_y)
                end   = (bot_x + fx * bot_w, bot_y)
                pygame.draw.line(self.screen, self.colors['grid_color'], start, end, 1)
            # horizontal lines
            for i in range(1, N):
                a = i / N
                left  = (top_x * (1 - a) + bot_x * a,
                         top_y * (1 - a) + bot_y * a)
                right = ((top_x + top_w) * (1 - a) + (bot_x + bot_w) * a,
                         top_y * (1 - a) + bot_y * a)
                pygame.draw.line(self.screen, self.colors['grid_color'], left, right, 1)

        # overlay tokens
        self.draw_moves(last_move)
        pygame.display.flip()

    def draw_moves(self, last_move=None):
        N = self.game.BOARD_SIZE
        W = self.WIDTH
        H = self.CELL_SIZE * N
        S = self.LAYER_SPACING
        top_w = W * 0.6
        bot_w = W * 0.8

        for z in range(N):
            top_x = (W - top_w) / 2
            bot_x = (W - bot_w) / 2
            top_y = 50 + z * (H + S)
            bot_y = top_y + H
            # precompute edges
            left_edge = []
            right_edge = []
            for i in range(N + 1):
                alpha = i / N
                lx = top_x * (1 - alpha) + bot_x * alpha
                ly = top_y * (1 - alpha) + bot_y * alpha
                rx = (top_x + top_w) * (1 - alpha) + (bot_x + bot_w) * alpha
                ry = top_y * (1 - alpha) + bot_y * alpha
                left_edge.append((lx, ly))
                right_edge.append((rx, ry))

            for y in range(N):
                for x in range(N):
                    v = self.game.board[z][y][x]
                    if v == -1:
                        continue
                    # compute cell corners
                    b1 = x / N
                    b2 = (x + 1) / N
                    p1 = (left_edge[y][0] * (1 - b1) + right_edge[y][0] * b1,
                          left_edge[y][1] * (1 - b1) + right_edge[y][1] * b1)
                    p2 = (left_edge[y][0] * (1 - b2) + right_edge[y][0] * b2,
                          left_edge[y][1] * (1 - b2) + right_edge[y][1] * b2)
                    p3 = (left_edge[y+1][0] * (1 - b2) + right_edge[y+1][0] * b2,
                          left_edge[y+1][1] * (1 - b2) + right_edge[y+1][1] * b2)
                    p4 = (left_edge[y+1][0] * (1 - b1) + right_edge[y+1][0] * b1,
                          left_edge[y+1][1] * (1 - b1) + right_edge[y+1][1] * b1)
                    # highlight last move: draw full cell border
                    if last_move == (x, y, z):
                        pygame.draw.polygon(
                            self.screen,
                            self.colors['neon_green'],
                            [p1, p2, p3, p4],
                            3
                        )
                    # draw symbol
                    symbol = 'X' if v == 1 else 'O'
                    color  = self.colors['x_color'] if v == 1 else self.colors['o_color']
                    text   = self.font.render(symbol, True, color)
                    self.screen.blit(text, text.get_rect(center=(((p1[0]+p3[0])/2), ((p1[1]+p3[1])/2))))

    def draw_win_line(self, line, color):
        """
        Draws the winning line connecting the centers of the first and last cells in the win `line`.
        Uses the same trapezoidal cell scheme as draw_moves for accurate alignment.
        """
        N = self.game.BOARD_SIZE
        W = self.WIDTH
        H = self.CELL_SIZE * N
        S = self.LAYER_SPACING
        top_w = W * 0.6
        bot_w = W * 0.8

        def cell_center(x, y, z):
            # layer-specific trapezoid
            top_x = (W - top_w) / 2
            bot_x = (W - bot_w) / 2
            top_y = 50 + z * (H + S)
            bot_y = top_y + H

            # compute edge points for row y and y+1
            alpha_y  = y / N
            alpha_y1 = (y + 1) / N
            lx_y  = top_x * (1 - alpha_y)  + bot_x * alpha_y
            ly_y  = top_y * (1 - alpha_y)  + bot_y * alpha_y
            rx_y  = (top_x + top_w) * (1 - alpha_y)  + (bot_x + bot_w) * alpha_y
            ry_y  = top_y * (1 - alpha_y)  + bot_y * alpha_y
            lx_y1 = top_x * (1 - alpha_y1) + bot_x * alpha_y1
            ly_y1 = top_y * (1 - alpha_y1) + bot_y * alpha_y1
            rx_y1 = (top_x + top_w) * (1 - alpha_y1) + (bot_x + bot_w) * alpha_y1
            ry_y1 = top_y * (1 - alpha_y1) + bot_y * alpha_y1

            # interpolate horizontally within the row for column x
            b1 = x / N
            b2 = (x + 1) / N
            p1 = (lx_y  * (1 - b1) + rx_y  * b1,
                  ly_y  * (1 - b1) + ry_y  * b1)
            p3 = (lx_y1 * (1 - b2) + rx_y1 * b2,
                  ly_y1 * (1 - b2) + ry_y1 * b2)

            # center is midpoint of top-left and bottom-right corners
            return ((p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2)

        # compute start and end points
        start = cell_center(*line[0])
        end   = cell_center(*line[-1])
        pygame.draw.line(self.screen, color, start, end, 4)
        pygame.display.flip()


    def show_end_screen(self, msg, score):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.colors['button_bg'])
        self.screen.blit(overlay, (0, 0))
        title = self.end_title_font.render(msg, True, self.colors['text_color'])
        title_rect = title.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 -40))
        self.screen.blit(title, title_rect)
        score_txt = self.end_score_font.render(f"Score: {score}/100", True, self.colors['text_color'])
        score_rect = score_txt.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        self.screen.blit(score_txt, score_rect)
        btn = pygame.Rect(self.WIDTH//2-80, self.HEIGHT//2+30, 160, 50)
        pygame.draw.rect(self.screen, (80, 0, 120), btn, 0, border_radius=8)
        btn_text = self.end_button_font.render('Play Again', True, self.colors['white'])
        btn_text_rect = btn_text.get_rect(center=btn.center)
        self.screen.blit(btn_text, btn_text_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos):
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return True
            pygame.time.Clock().tick(30)


    def show_start_menu(self):
        """
        Display a start menu with a 'Start Game' button.
        Returns True if the player clicks Start, False on quit.
        """
        pygame.mixer.music.pause()
        clock = pygame.time.Clock()
        btn_w, btn_h = 200, 60
        btn_rect = pygame.Rect(
            (self.WIDTH - btn_w) // 2,
            (self.HEIGHT - btn_h) // 2,
            btn_w, btn_h
        )
        title_surf = self.start_title_font.render('CubiXpert', True, self.colors['text_color'])
        title_rect = title_surf.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 100))

        while True:
            self.screen.fill(self.colors['dark_bg'])
            self.draw_starfield()
            # draw title
            self.screen.blit(title_surf, title_rect)
            # draw start button
            pygame.draw.rect(self.screen, self.colors['grid_color'], btn_rect, border_radius=10)
            txt_surf = self.font.render('Start Game', True, self.colors['white'])
            txt_rect = txt_surf.get_rect(center=btn_rect.center)
            self.screen.blit(txt_surf, txt_rect)
            # draw credits
            lines = [
                'By the Incredibles',
                'Ahmed Elgalay',
                'Abdelrahman Salah',
                'Amr Fawzy',
                'Ahmed Zidan'
            ]

            # Starting vertical position
            start_y = self.HEIGHT // 2 + 100

            for i, line in enumerate(lines):
                line_surf = self.credits_font.render(line, True, self.colors['text_color'])
                line_rect = line_surf.get_rect(center=(self.WIDTH//2, start_y + i * 40))  # 40 pixels spacing between lines
                self.screen.blit(line_surf, line_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos):
                    return True
            clock.tick(30)
