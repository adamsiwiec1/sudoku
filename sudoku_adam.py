import random as rn
import logging
from datetime import datetime
import time

logging.basicConfig(filename='sudoku.log', encoding='utf-8', level=logging.DEBUG)


class Cell:
    def __init__(self, c):
        self.coordinate = c
        self.column = c[0]
        self.row = c[1]
        self.value = 0
        self.given = False
        self.empty = True


class SudokuGame:
    def __init__(self,name):
        self.puzzle = {
            'G1': {
                'A1': Cell('A1'),
                'B1': Cell('B1'),
                'C1': Cell('C1'),
                'A2': Cell('A2'),
                'B2': Cell('B2'),
                'C2': Cell('C2'),
                'A3': Cell('A3'),
                'B3': Cell('B3'),
                'C3': Cell('C3')
            },
            'G2': {
                'D1': Cell('D1'),
                'E1': Cell('E1'),
                'F1': Cell('F1'),
                'D2': Cell('D2'),
                'E2': Cell('E2'),
                'F2': Cell('F2'),
                'D3': Cell('D3'),
                'E3': Cell('E3'),
                'F3': Cell('F3')
            },
            'G3': {
                'G1': Cell('G1'),
                'H1': Cell('H1'),
                'I1': Cell('I1'),
                'G2': Cell('G2'),
                'H2': Cell('H2'),
                'I2': Cell('I2'),
                'G3': Cell('G3'),
                'H3': Cell('H3'),
                'I3': Cell('I3')
            },
            'G4': {
                'A4': Cell('A4'),
                'B4': Cell('B4'),
                'C4': Cell('C4'),
                'A5': Cell('A5'),
                'B5': Cell('B5'),
                'C5': Cell('C5'),
                'A6': Cell('A6'),
                'B6': Cell('B6'),
                'C6': Cell('C6')
            },
            'G5': {
                'D4': Cell('D4'),
                'E4': Cell('E4'),
                'F4': Cell('F4'),
                'D5': Cell('D5'),
                'E5': Cell('E5'),
                'F5': Cell('F5'),
                'D6': Cell('D6'),
                'E6': Cell('E6'),
                'F6': Cell('F6')
            },
            'G6': {
                'G4': Cell('G4'),
                'H4': Cell('H4'),
                'I4': Cell('I4'),
                'G5': Cell('G5'),
                'H5': Cell('H5'),
                'I5': Cell('I5'),
                'G6': Cell('G6'),
                'H6': Cell('H6'),
                'I6': Cell('I6')
            },
            'G7': {
                'A7': Cell('A7'),
                'B7': Cell('B7'),
                'C7': Cell('C7'),
                'A8': Cell('A8'),
                'B8': Cell('B8'),
                'C8': Cell('C8'),
                'A9': Cell('A9'),
                'B9': Cell('B9'),
                'C9': Cell('C9')
            },
            'G8': {
                'D7': Cell('D7'),
                'E7': Cell('E7'),
                'F7': Cell('F7'),
                'D8': Cell('D8'),
                'E8': Cell('E8'),
                'F8': Cell('F8'),
                'D9': Cell('D9'),
                'E9': Cell('E9'),
                'F9': Cell('F9')
            },
            'G9': {
                'G7': Cell('G7'),
                'H7': Cell('H7'),
                'I7': Cell('I7'),
                'G8': Cell('G8'),
                'H8': Cell('H8'),
                'I8': Cell('I8'),
                'G9': Cell('G9'),
                'H9': Cell('H9'),
                'I9': Cell('I9')
            },
        }
        self.puzzle_2d = []
        self.solution_2d = None
        self.name = name
        self.grid_dict = {}
        self.column_dict = {}
        self.row_dict = {}
        self.m = 9
        self.generate_puzzle()
        self.get_current_values()
        self.raw_grid_2d_arr()
        self.perform_tests()

    def clear_puzzle(self):
        for g in self.puzzle.keys():
            for c in self.puzzle.get(g).keys():
                self.puzzle.get(g).get(c).value = 0

    def generate_puzzle(self):
        self.clear_puzzle()
        for g in self.puzzle.keys():
            amt_random = rn.randint(2, 3)
            prev_int = 0
            for x in range(amt_random):
                c = rn.choice(list(self.puzzle.get(g).keys()))
                cell = self.puzzle.get(g).get(c)
                given = rn.randint(1, 9)
                while given == prev_int:
                    given = rn.randint(1, 9)
                cell.value = given
                cell.given = True
                prev_int = given
        self.get_current_values()
        self.raw_grid_2d_arr()

    def print_grid(self):
        grids = []
        for g in self.puzzle.keys():
            g = self.puzzle.get(g)
            y = [(i, (x+y), g.get(x+y).value) for i, (x, y) in enumerate(g, 1)]
            z = [(x[1]) for i,x in enumerate(y)]
            grids.append(z)
        print(f"\n{str(self.name)}'s Sudoku Game:")
        print('----------------------------------')
        for x in self.sections.keys():
            print('| {} {} {} | {} {} {} | {} {} {} |'.format(
                *(grids[self.sections.get(x)[0]][0:3] +
                  grids[self.sections.get(x)[1]][0:3] +
                  grids[self.sections.get(x)[2]][0:3])))
            print('| {} {} {} | {} {} {} | {} {} {} |'.format(
                *(grids[self.sections.get(x)[0]][3:6] +
                  grids[self.sections.get(x)[1]][3:6] +
                  grids[self.sections.get(x)[2]][3:6])))
            print('| {} {} {} | {} {} {} | {} {} {} |'.format(
                *(grids[self.sections.get(x)[0]][6:9] +
                  grids[self.sections.get(x)[1]][6:9] +
                  grids[self.sections.get(x)[2]][6:9])))
            print('----------------------------------')

    def print_game(self):
        print(f"\n{str(self.name)}'s Sudoku Game:")


        print('-------------------------')
        for x in range(9):
            print('| {} {} {} | {} {} {} | {} {} {} |'.format(
                *(self.puzzle_2d[x])))
            if x != 0 and x % 3 == 2:
                print('|-----------------------|')

    def get_current_values(self):
        # grid
        for grid in self.puzzle.keys():
            grid_cells = [self.puzzle.get(grid).get(x).value for x in self.puzzle.get(grid)]
            self.grid_dict[grid] = grid_cells
        # columns
        for column in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            self.column_dict[column] = []
            for g in self.puzzle.keys():
                for c in self.puzzle.get(g).keys():
                    cell=self.puzzle.get(g).get(c)
                    if cell.column == column:
                        self.column_dict.get(column).append(cell.value)
        # rows
        for row in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.row_dict[row] = []
            for g in self.puzzle.keys():
                for c in self.puzzle.get(g).keys():
                    cell = self.puzzle.get(g).get(c)
                    if cell.row == row:
                        self.row_dict.get(row).append(cell.value)

    def raw_grid_2d_arr(self):
        self.puzzle_2d = [self.row_dict.get('1'),
                            self.row_dict.get('2'),
                            self.row_dict.get('3'),
                            self.row_dict.get('4'),
                            self.row_dict.get('5'),
                            self.row_dict.get('6'),
                            self.row_dict.get('7'),
                            self.row_dict.get('8'),
                            self.row_dict.get('9')]

    def insert_value(self, coordinate, value):
        for x in self.puzzle.keys():
            for y in self.puzzle.get(x):
                if y == coordinate or y.lower() == coordinate:
                    # print(self.puzzle.get(x).get(y.upper()).coordinate)
                    self.puzzle.get(x).get(y.upper()).value = value

    def solve(self,grid,row,col,n):
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

    def solve_2darr(self,grid, r, c):
        if r == self.m - 1 and c == self.m:
            return True
        if c == self.m:
            r += 1
            c = 0
        if grid[r][c] > 0:
            return self.solve_2darr(grid, r, c + 1)

        for n in range(1, self.m + 1, 1):
            if self.solve(grid, r, c, n):
                grid[r][c] = n
                if self.solve_2darr(grid, r, c + 1):
                    return True
            grid[r][c] = 0
        return False

    def get_solution(self, grid, r, c):
        if self.solve_2darr(grid, r, c):
            print('Solution found.')
            self.solution_2d = grid
            return True
        else:
            print(self.puzzle_2d)
            self.print_game()
            print("Solution does not exist.")
            return False

    def perform_tests(self):
        '''
        each test method returns True if pass, False if fail
        '''
        seventeen_result = self.test_seventeen()
        grid_result = self.test_grid_duplicates()
        column_result = self.test_column_duplicates()
        row_result = self.test_row_duplicates()
        if False not in (seventeen_result, grid_result, column_result, row_result) and self.get_solution(self.puzzle_2d, 0, 0):
            if self.solution_2d:
                bools_45 = [True if sum(self.solution_2d[x]) == 45 else False for x in range(len(self.solution_2d))]
                print(bools_45)
                if False in bools_45:
                    # print('Tests failed. Trying again.')
                    self.generate_puzzle()
                    self.perform_tests()
                    return False
                else:
                    print('Tests passed')
                    return True
        else:
            # print('Tests failed. Trying again.')
            self.generate_puzzle()
            self.perform_tests()
            return False

    def test_seventeen(self):
        count_given = 0
        for g in self.puzzle.keys():
            d = self.puzzle.get(g)
            l = [d.get(x).value for x in d.keys()]
            l = [x for x in l if x > 0]
            count_given += len(l)
        if count_given <= 17:
            logging.error(f'\nPLAYER: {self.name}'
                          f'\nERROR: LESS THAN 17'
                          f'\nDATE: {datetime.now()}')
            return False
        else:
            return True

    def test_grid_duplicates(self):
        for g in self.puzzle.keys():
            d = self.puzzle.get(g)
            l = [d.get(x).value for x in d.keys()]
            l = [x for x in l if x > 0]
            if len(l) != len(set(l)):
                logging.error(f'\nPLAYER: {self.name}'
                              f'\nERROR: GRID DUPLICATES {g}'
                              f'\nDATE: {datetime.now()}')
                return False
            else:
                continue
        return True

    def test_column_duplicates(self):
        for column in ['A','B','C','D','E','F','G','H','I']:
            values=[]
            for g in self.puzzle.keys():
                for c in self.puzzle.get(g).keys():
                    cell = self.puzzle.get(g).get(c)
                    if cell.column == column:
                        if cell.value in values and cell.value != 0:
                            logging.error(f'\nPLAYER: {self.name}'
                                          f'\nERROR: COLUMN DUPLICATES {g}'
                                          f'\nDATE: {datetime.now()}')
                            return False
                        else:
                            values.append(cell.value)
                    else:
                        continue
        return True

    def test_row_duplicates(self):
        for row in ['1','2','3','4','5','6','7','8','9']:
            values = []
            for g in self.puzzle.keys():
                for c in self.puzzle.get(g).keys():
                    cell = self.puzzle.get(g).get(c)
                    if cell.row == row:
                        if cell.value in values and cell.value != 0:
                            logging.error(f'\nPLAYER: {self.name}'
                                          f'\nERROR: COLUMN DUPLICATES {g}'
                                          f'\nDATE: {datetime.now()}')
                            return False
                        else:
                            values.append(cell.value)
                    else:
                        continue
        return True


    # @staticmethod
    # def generate_random_combo_1_9(g_c_or_r_list):
    #     l = g_c_or_r_list
    #     while 0 in l:
    #         missing_i=[]
    #         [missing_i.append(i) if value == 0 and i is not None else None for i, value in enumerate(l)]
    #         not_in_s=rn.choice([x for x in range(10) if x not in l])
    #         l[missing_i[0]] = not_in_s
    #     if sum(l) == 45:
    #         return l
    #     else:
    #         print('Something went wrong generating numbers..')

def main():
    s = SudokuGame('test1hunna')
    s.print_game()

    # ouzzle_266 = [[7,0,0,0,9,6,0,5,0],
    #                 [0,3,0,0,0,0,0,0,1],
    #                 [5,0,2,1,0,4,0,0,0],
    #                 [0,0,0,5,0,0,0,1,8],
    #                 [0,5,0,0,0,0,0,3,0],
    #                 [3,6,0,0,0,1,0,0,0],
    #                 [0,0,0,4,0,2,3,0,7],
    #                 [1,0,0,0,0,0,0,2,0],
    #                 [0,2,0,8,7,0,0,0,9]
    # ]
    # s.get_solution(ouzzle_266,0,0)
    # s.print_game()
main()

# s.get_solution()
#
# print(s.solution_2d)

                        # KEY #

#               A B C   D E F   G H I
                # # # | # # # | # # # 1
# Section 1     # 1 # | # 2 # | # 3 # 2
                # # # | # # # | # # # 3
#               -----------------------
                # # # | # # # | # # # 4
# Section 2     # 4 # | # 5 # | # 6 # 5
                # # # | # # # | # # # 6
#               -----------------------
                # # # | # # # | # # # 7
# Section 3     # 7 # | # 8 # | # 9 # 8
                # # # | # # # | # # # 9
