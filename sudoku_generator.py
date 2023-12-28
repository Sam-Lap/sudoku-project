'''
Sudoku Generator
'''
import random
from copy import deepcopy
from sudoku_solver import solve_sudoku, print_board

class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.rows_available = [[i for i in range(1, 10)] for _ in range(9)]
        self.cols_available = [[i for i in range(1, 10)] for _ in range(9)]
        self.blocks_available = [[i for i in range(1, 10)] for _ in range(9)]

    def generate_full_board(self):
        self.fill_board(0, 0)

    def fill_board(self, row, col):
        if row == 9:
            return True
        if col == 9:
            return self.fill_board(row + 1, 0)

        block = (row // 3) * 3 + col // 3
        possible_nums = set(self.rows_available[row]) & set(self.cols_available[col]) & set(self.blocks_available[block])
        nums = list(possible_nums)
        random.shuffle(nums)

        for num in nums:
            if self.place_number(num, row, col):
                if self.fill_board(row, col + 1):
                    return True
                self._remove_number(num, row, col)
        return False

    def place_number(self, num, row, col):
        block = (row // 3) * 3 + col // 3
        self.board[row][col] = num
        self.rows_available[row].remove(num)
        self.cols_available[col].remove(num)
        self.blocks_available[block].remove(num)
        return True

    def _remove_number(self, num, row, col):
        block = (row // 3) * 3 + col // 3
        self.board[row][col] = 0
        self.rows_available[row].append(num)
        self.cols_available[col].append(num)
        self.blocks_available[block].append(num)

    def remove_numbers(self, difficulty):
        remaining = 81
        target = 81 - difficulty

        while remaining > target:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0
                
                board_copy = deepcopy(self.board)
                if solve_sudoku(board_copy) and self._is_unique_solution(self.board):
                    remaining -= 1
                else:
                    self.board[row][col] = backup

    def _is_unique_solution(self, board):
        self.solution_count = 0
        self._solve_and_count_solutions(deepcopy(board), 0, 0)
        return self.solution_count == 1

    def _solve_and_count_solutions(self, board, row, col):
        if row == 9:
            self.solution_count += 1
            return

        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)

        if board[row][col] == 0:
            for num in range(1, 10):
                if self._is_valid(num, row, col, board):
                    board[row][col] = num
                    self._solve_and_count_solutions(board, next_row, next_col)
                    board[row][col] = 0
                    if self.solution_count > 1:
                        return  # Early exit if more than one solution is found
        else:
            self._solve_and_count_solutions(board, next_row, next_col)

    def _is_valid(self, num, row, col, board):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def generate_puzzle(self):
        self.generate_full_board()
        self.remove_numbers(37)  # Adjust difficulty here
        return self.board

if __name__ == "__main__":
    generator = SudokuGenerator()
    puzzle = generator.generate_puzzle()
    print("Generated Puzzle")
    print_board(puzzle)
    
    # if solve_sudoku(puzzle):
    #     print("Solved Puzzle")
    #     print_board(puzzle)
    
        
