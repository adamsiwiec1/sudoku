import random as rn
import logging
from datetime import datetime
import copy as cp
import time

logging.basicConfig(filename='../dev_and_old/sudoku.log', encoding='utf-8', level=logging.DEBUG)


class SudokuGame:
    def __init__(self,name):
        self.name = name
        self.puzzle = []
        # self.staging = []
        self.solution = None
        self.rows = None
        self.grids = [[]]*9
        self.columns = [[]]*9

    def generate_puzzle(self):
        self.clear_puzzle()
        for row in range(0,9):
            prev_vals = []
            prev_cols = []
            for x in range(rn.choice([2, 3])):
                given = rn.randint(1, 9)
                while given in prev_vals:
                    given = rn.randint(1, 9)
                prev_vals.append(given)
                col = rn.randint(0, 8)
                while col == prev_cols:
                    col = rn.randint(0, 8)
                prev_cols.append(col)
                self.puzzle[row][col] = given
        self.rows = self.puzzle

    def get_columns(self):
        for row in range(0, 9):
            column_row = []
            for column in range(0, 9):
                column_row.append(self.rows[column][row])
            self.columns[row] = column_row

    def get_grids(self):
        for x in range(0, 9, 3):
            self.grids[x] = self.rows[x][0:3] + self.rows[x+1][0:3] + self.rows[x+2][0:3]
            self.grids[x+1] = self.rows[x][3:6] + self.rows[x+1][3:6] + self.rows[x+2][3:6]
            self.grids[x+2] = self.rows[x][6:9] + self.rows[x+1][6:9] + self.rows[x+2][6:9]
            # same logic with columns
            # self.grids[x] = self.columns[x][0:3] + self.columns[x+1][0:3] + self.columns[x+2][0:3]
            # self.grids[x+1] = self.columns[x][3:6] + self.columns[x+1][3:6] + self.columns[x+2][3:6]
            # self.grids[x+2] = self.columns[x][6:9] + self.columns[x+1][6:9] + self.columns[x+2][6:9]

    def print_puzzle(self):
        print(f"\n{str(self.name)}'s Sudoku Game:")
        print('-------------------------')
        for x in range(9):
            print('| {} {} {} | {} {} {} | {} {} {} |'.format(
                *(self.puzzle[x])))
            if x != 0 and x % 3 == 2:
                print('-------------------------')

    def print_solution(self):
        print(f"\n{str(self.name)}'s Sudoku Game:")
        print('-------------------------')
        for x in range(9):
            print('| {} {} {} | {} {} {} | {} {} {} |'.format(
                *(self.solution[x])))
            if x != 0 and x % 3 == 2:
                print('-------------------------')

    def clear_puzzle(self):
        self.puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def perform_tests(self):
        self.generate_puzzle()
        self.get_columns()
        self.get_grids()
        for x in [self.rows, self.columns, self.grids]:
            for y in x:
                z = [z for z in y if z != 0]
                if len(z) != len(set(z)) or len(x) == 0:
                    return False
        return True

    def new_game(self):
        tests_pass = self.perform_tests()

        while not tests_pass:
            tests_pass = self.perform_tests()
        solution_found = self.get_current_solution()
        if not solution_found:
            self.new_game()

    # solution methods
    def get_current_solution(self):
        r = 0
        c = 0
        m = 9
        grid = cp.deepcopy(self.rows)
        if self.solve(grid, r, c, m):
            logging.log(1,  f'\nPLAYER: {self.name}'
                            f'\nLOG: CURRENT SOLUTION FOUND'
                            f'\nDATE: {datetime.now()}')
            self.solution = grid
            return True
        else:
            return False

    def get_given_solution(self,grid):
        r = 0
        c = 0
        m = 9
        grid = cp.deepcopy(grid)
        if self.solve(grid, r, c, m):
            logging.log(1,  f'\nPLAYER: {self.name}'
                            f'\nLOG: GIVEN SOLUTION FOUND'
                            f'\nDATE: {datetime.now()}')
            self.solution = grid
            return True
        else:
            return False

    def solve(self, grid, r, c, m):
        if r == m - 1 and c == m:
            return True
        if c == m:
            r += 1
            c = 0
        if grid[r][c] > 0:
            return self.solve(grid, r, c + 1, m)
        for n in range(1, m + 1, 1):
            if self.solve_cell(grid, r, c, n):
                grid[r][c] = n
                if self.solve(grid, r, c + 1, m):
                    return True
            grid[r][c] = 0
        return False

    @staticmethod
    def solve_cell(grid, row, col, n):
        for x in range(9):
            if grid[row][x] == n:
                return False
        for x in range(9):
            if grid[x][col] == n:
                return False

        start_r = row - row % 3
        start_c = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_r][j + start_c] == n:
                    return False
        return True

s = SudokuGame('Adam')
s.new_game()
s.print_puzzle()
s.print_solution()
s.print_puzzle()
