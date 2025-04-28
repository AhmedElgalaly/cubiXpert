from models.cubic_game import CubicGame
from models.ai_logic import AIPlayer
from views.gui.game_gui import GameGUI
from time import sleep
import pygame
import random

def main():
    pygame.init()
    game = CubicGame()
    ai = AIPlayer(game)
    gui = GameGUI(game)
    clock = pygame.time.Clock()
    running = True

    if not gui.show_start_menu():
        pygame.quit()
        return

    while True:
        play_again = True
        if not play_again:
            pygame.quit()
            return False
        else:
            game = CubicGame()
            ai = AIPlayer(game)
            gui = GameGUI(game)
            last_move = None
            human_turn = random.choice([True, False])
            running = True



        while running:
            gui.draw_board(last_move)

            # 1) handle quit + human clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if human_turn and event.type == pygame.MOUSEBUTTONDOWN:
                    cell = gui.get_grid_position(event.pos)
                    if cell and cell in game.get_available_moves():
                        # do exactly one human move
                        game.make_move(*cell, 1)
                        last_move = cell
                        human_turn = False

                        # check human win/draw
                        win, line = game.check_winner(1)
                        if win:
                            gui.draw_board(last_move)
                            gui.draw_win_line(line, gui.colors['win_line_color'])
                            play_again = gui.show_end_screen('You Win!', 100)
                            running = False
                        elif not game.get_available_moves():
                            gui.draw_board(last_move)
                            play_again = gui.show_end_screen("It's a Draw!", 50)
                            running = False
                        # break immediately so no further events trigger another move
                        break

            # 2) exactly one AI move, _after_ all events have been processed
            if not human_turn and running:
                mv = ai.get_best_move()
                if mv:
                    game.make_move(*mv, 0)
                    last_move = mv
                human_turn = True

                # check AI win/draw
                win, line = game.check_winner(0)
                if win:
                    gui.draw_board(last_move)
                    gui.draw_win_line(line, gui.colors['win_line_color'])
                    
                    play_again = gui.show_end_screen('AI Wins!', 0)
                    running = False
                    print(play_again, running)
                elif not game.get_available_moves():
                    gui.draw_board(last_move)
                    play_again = gui.show_end_screen("It's a Draw!", 50)
                    running = False

            clock.tick(30)

def game_over(gui, msg, score):
    play_again = gui.show_end_screen(msg, score)
    if play_again:
        return True
    else:
        pygame.quit()
        return False
    


if __name__ == '__main__':
    main()