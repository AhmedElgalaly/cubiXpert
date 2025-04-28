import math

class AIPlayer:
    def __init__(self, game, depth=2):
        self.game = game
        self.depth = depth

    def get_best_move(self):
        best_move, _ = self.minimax(self.depth, True, -math.inf, math.inf)
        return best_move

    def minimax(self, depth, maximizing, alpha, beta):
        win, _ = self.game.check_winner(0)
        if win:
            return None, 10000
        win, _ = self.game.check_winner(1)
        if win:
            return None, -10000
        moves = self.game.get_available_moves()
        if not moves or depth == 0:
            return None, self.heuristic(0)
        if maximizing:
            max_val = -math.inf
            best_mv = None
            for mv in moves:
                x, y, z = mv
                self.game.make_move(x, y, z, 0)
                _, val = self.minimax(depth-1, False, alpha, beta)
                self.game.undo_move(x, y, z)
                if val > max_val:
                    max_val, best_mv = val, mv
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return best_mv, max_val
        else:
            min_val = math.inf
            best_mv = None
            for mv in moves:
                x, y, z = mv
                self.game.make_move(x, y, z, 1)
                _, val = self.minimax(depth-1, True, alpha, beta)
                self.game.undo_move(x, y, z)
                if val < min_val:
                    min_val, best_mv = val, mv
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return best_mv, min_val

    def heuristic(self, player):
        opp = 1 - player
        score = 0
        for line in self.game.winning_lines:
            pc = sum(self.game.board[z][y][x] == player for (x, y, z) in line)
            oc = sum(self.game.board[z][y][x] == opp for (x, y, z) in line)
            if pc > 0 and oc == 0:
                score += 10 ** pc
            elif oc > 0 and pc == 0:
                score -= 10 ** oc
        return score