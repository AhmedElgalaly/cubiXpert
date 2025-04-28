import math
import random

class CubicGame:
    def __init__(self, board_size=4):
        self.BOARD_SIZE = board_size
        self.board = self.create_board()
        self.winning_lines = self.generate_winning_lines()
        self.center_cells = self.generate_center_cells()

    def create_board(self):
        return [[[-1 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)] for __ in range(self.BOARD_SIZE)]

    def generate_winning_lines(self):
        raw = []
        for z in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                raw.append([(x, y, z) for x in range(self.BOARD_SIZE)])
            for x in range(self.BOARD_SIZE):
                raw.append([(x, y, z) for y in range(self.BOARD_SIZE)])
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                raw.append([(x, y, z) for z in range(self.BOARD_SIZE)])

        for z in range(self.BOARD_SIZE):
            raw.append([(i, i, z) for i in range(self.BOARD_SIZE)])
            raw.append([(i, self.BOARD_SIZE-1-i, z) for i in range(self.BOARD_SIZE)])
        for x in range(self.BOARD_SIZE):
            raw.append([(x, i, i) for i in range(self.BOARD_SIZE)])
            raw.append([(x, i, self.BOARD_SIZE-1-i) for i in range(self.BOARD_SIZE)])
        for y in range(self.BOARD_SIZE):
            raw.append([(i, y, i) for i in range(self.BOARD_SIZE)])
            raw.append([(i, y, self.BOARD_SIZE-1-i) for i in range(self.BOARD_SIZE)])

        raw.append([(i, i, i) for i in range(self.BOARD_SIZE)])
        raw.append([(i, i, self.BOARD_SIZE-1-i) for i in range(self.BOARD_SIZE)])
        raw.append([(i, self.BOARD_SIZE-1-i, i) for i in range(self.BOARD_SIZE)])
        raw.append([(self.BOARD_SIZE-1-i, i, i) for i in range(self.BOARD_SIZE)])

        lines = []
        for line in raw:
            if len(line) < self.BOARD_SIZE:
                continue
            dx = line[1][0] - line[0][0]
            dy = line[1][1] - line[0][1]
            dz = line[1][2] - line[0][2]
            valid = True
            for i in range(1, len(line)):
                if (line[i][0] - line[i-1][0] != dx or
                    line[i][1] - line[i-1][1] != dy or
                    line[i][2] - line[i-1][2] != dz):
                    valid = False
                    break
            if valid:
                lines.append(line)
        return lines

    def generate_center_cells(self):
        mid = self.BOARD_SIZE // 2
        coords = []
        if self.BOARD_SIZE % 2 == 0:
            coords = [mid-1, mid]
        else:
            coords = [mid]
        return [(x, y, z) for x in coords for y in coords for z in coords]

    def get_available_moves(self):
        return [(x, y, z)
                for z in range(self.BOARD_SIZE)
                for y in range(self.BOARD_SIZE)
                for x in range(self.BOARD_SIZE)
                if self.board[z][y][x] == -1]

    def make_move(self, x, y, z, player):
        self.board[z][y][x] = player

    def undo_move(self, x, y, z):
        self.board[z][y][x] = -1

    def check_winner(self, player):
        for line in self.winning_lines:
            if all(self.board[z][y][x] == player for (x, y, z) in line):
                return True, line
        return False, None