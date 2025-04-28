import math

class AIPlayer:
    def __init__(self, game, depth=2):
        self.game = game
        self.depth = depth
        self.board_size = game.BOARD_SIZE

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
        """Alternative heuristic focusing on layer dominance and potential threats"""
        opp = 1 - player
        score = 0
        
        # 1. Layer control bonus (middle layers are more valuable)
        layer_weights = [1, 3, 3, 1] if self.board_size == 4 else [1, 2, 1]
        for z in range(self.board_size):
            layer_score = 0
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.game.board[z][y][x] == player:
                        layer_score += layer_weights[z] * 5
                    elif self.game.board[z][y][x] == opp:
                        layer_score -= layer_weights[z] * 5
            score += layer_score
        
        # 2. Edge and corner control
        edge_bonus = 15
        corner_bonus = 25
        for z in range(self.board_size):
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.is_edge_or_corner(x, y, z):
                        if self.game.board[z][y][x] == player:
                            score += corner_bonus if self.is_corner(x, y, z) else edge_bonus
                        elif self.game.board[z][y][x] == opp:
                            score -= corner_bonus if self.is_corner(x, y, z) else edge_bonus

        # 3. Line potential with progressive blocking
        for line in self.game.winning_lines:
            pc = sum(1 for (x, y, z) in line if self.game.board[z][y][x] == player)
            oc = sum(1 for (x, y, z) in line if self.game.board[z][y][x] == opp)
            
            if pc > 0 and oc > 0:  # Blocked line
                continue
                
            if pc > 0:
                line_value = 10 ** (pc + 1)
                if pc == self.board_size - 1:  # Immediate win
                    line_value *= 10
                score += line_value
            elif oc > 0:
                line_value = 10 ** (oc + 1)
                if oc == self.board_size - 1:  # Immediate loss
                    line_value *= 10
                score -= line_value * 2  # Higher penalty for opponent's potential

        # 4. Mobility factor (encourage keeping options open)
        available_moves = len(self.game.get_available_moves())
        score += available_moves * (1 if player == 0 else -1) * 5

        return score

    def is_edge_or_corner(self, x, y, z):
        """Check if cell is on edge or corner"""
        max_idx = self.board_size - 1
        return (x in (0, max_idx) or 
                y in (0, max_idx) or 
                z in (0, max_idx))

    def is_corner(self, x, y, z):
        """Check if cell is a 3D corner"""
        max_idx = self.board_size - 1
        return (x in (0, max_idx) and 
                y in (0, max_idx) and 
                z in (0, max_idx))

    #def heuristic(self, player):
        opp = 1 - player
        score = 0
        threat_length = self.board_size - 1  # Cells needed for immediate win
        
        # 1. Center control evaluation
        center_bonus = 20
        for (x, y, z) in self.game.center_cells:
            if self.game.board[z][y][x] == player:
                score += center_bonus
            elif self.game.board[z][y][x] == opp:
                score -= center_bonus

        # 2. Line potential analysis
        for line in self.game.winning_lines:
            pc = sum(self.game.board[z][y][x] == player for (x, y, z) in line)
            oc = sum(self.game.board[z][y][x] == opp for (x, y, z) in line)

            if pc > 0 and oc == 0:
                if pc == threat_length:  # Immediate win potential
                    score += 10000
                else:  # Progressive bonus for consecutive pieces
                    score += 10 ** pc
                    # Additional bonus for 3D diagonal patterns
                    if self.is_3d_diagonal(line):
                        score += 50 * pc
            elif oc > 0 and pc == 0:
                if oc == threat_length:  # Block opponent's immediate win
                    score -= 10000
                else:  # Progressive penalty for opponent's progress
                    score -= 10 ** oc
                    # Additional penalty for 3D opponent patterns
                    if self.is_3d_diagonal(line):
                        score -= 50 * oc

        # 3. Spatial distribution bonus
        score += self.calculate_spatial_distribution(player)
        score -= self.calculate_spatial_distribution(opp)

        return score

    #def is_3d_diagonal(self, line):
        """Check if line is a 3D diagonal (more strategic value)"""
        coords = line
        return (all(x == y == z for x, y, z in coords) or
                all(x == y and z == self.board_size-1-x for x, y, z in coords) or
                all(x == z and y == self.board_size-1-x for x, y, z in coords) or
                all(y == z and x == self.board_size-1-y for x, y, z in coords))

    #def calculate_spatial_distribution(self, player):
        """Reward positions that participate in multiple potential lines"""
        distribution_score = 0
        for z in range(self.board_size):
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.game.board[z][y][x] == player:
                        # Count how many winning lines this cell participates in
                        line_count = sum(1 for line in self.game.winning_lines if (x, y, z) in line)
                        distribution_score += line_count * 2  # Weight for line participation
        return distribution_score