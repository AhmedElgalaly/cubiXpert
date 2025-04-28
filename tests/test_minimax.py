import time
import math
from models.cubic_game import CubicGame
from models.ai_logic import AIPlayer

class MinimaxTester:
    def __init__(self, depth=3):
        self.depth = depth
        self.total_wins = 0
        self.total_time = 0
        self.move_times = []
    
    def heuristic(self, game, player):
        opp = 1 - player
        score = 0
        for line in game.winning_lines:
            pc = sum(game.board[z][y][x] == player for (x, y, z) in line)
            oc = sum(game.board[z][y][x] == opp for (x, y, z) in line)
            if pc > 0 and oc == 0:
                score += 10 ** pc
            elif oc > 0 and pc == 0:
                score -= 10 ** oc
        return score

    def get_move(self, game):
        start_time = time.time()
        move, _ = self._minimax(game, self.depth, True)
        elapsed = time.time() - start_time
        self.move_times.append(elapsed)
        self.total_time += elapsed
        return move

    def _minimax(self, game, depth, maximizing):
        # Terminal checks
        win0, _ = game.check_winner(0)
        win1, _ = game.check_winner(1)
        if win0: return (None, -math.inf)
        if win1: return (None, math.inf)
        if depth == 0 or not game.get_available_moves():
            return (None, self.heuristic(game, 1))

        best_move = None
        moves = game.get_available_moves()
        
        if maximizing:
            max_val = -math.inf
            for move in moves:
                x, y, z = move
                game.make_move(x, y, z, 1)
                _, val = self._minimax(game, depth-1, False)
                game.undo_move(x, y, z)
                
                if val > max_val:
                    max_val = val
                    best_move = move
            return (best_move, max_val)
        else:
            min_val = math.inf
            for move in moves:
                x, y, z = move
                game.make_move(x, y, z, 0)
                _, val = self._minimax(game, depth-1, True)
                game.undo_move(x, y, z)
                
                if val < min_val:
                    min_val = val
                    best_move = move
            return (best_move, min_val)

def run_minimax_tests(num_games=10):
    tester = MinimaxTester(depth=2)
    log = []
    
    for i in range(num_games):
        game = CubicGame()
        ai = AIPlayer(game)
        current_player = 0
        tester.move_times = []
        
        while True:
            if current_player == 0:
                move = ai.get_best_move()
            else:
                move = tester.get_move(game)
            
            x, y, z = move
            game.make_move(x, y, z, current_player)
            
            win, _ = game.check_winner(current_player)
            if win:
                result = "AI Wins" if current_player == 0 else "Minimax Wins"
                if current_player == 1: tester.total_wins += 1
                break
            
            if not game.get_available_moves():
                result = "Draw"
                break
                
            current_player = 1 - current_player
        
        log.append(
            f"Game {i+1}: {result} | "
            f"Moves: {len(tester.move_times)} | "
            f"Avg Time: {sum(tester.move_times)/len(tester.move_times):.4f}s"
        )
    
    # Write log file
    with open("tests/minimax_results.txt", "w") as f:
        f.write("\n".join(log))
        f.write(f"\n\nFinal Results ({num_games} games):\n")
        f.write(f"Minimax Wins: {tester.total_wins}\n")
        f.write(f"Win Rate: {tester.total_wins/num_games:.1%}\n")
        f.write(f"Average Move Time: {tester.total_time/sum(len(t.move_times) for t in [tester]):.4f}s")

if __name__ == "__main__":
    run_minimax_tests()