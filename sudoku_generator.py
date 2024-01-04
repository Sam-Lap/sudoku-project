'''
Sudoku Generator
'''
import random
import copy 
from sudoku_solver import SudokuConstraints, solve_sudoku, print_board

class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.constraints = SudokuConstraints(self.board)

    def fill_board(self, row=0, col=0):
        if row == 9: 
            return True
        if col == 9: 
            return self.fill_board(row + 1, 0)
        
        options = random.sample(range(1, 10), 9)
        
        for num in options:
            if self.constraints.is_number_valid(row, col, num):
                self.board[row][col] = num
                self.constraints.add_number(row, col, num)
                
                if self.fill_board(row, col + 1):
                    return True
                
                self.board[row][col] = 0
                self.constraints.remove_number(row, col, num)
        return False

    def remove_numbers(self, num_to_remove):
        
        while num_to_remove > 0: 
            row, col= random.randint(0, 8), random.randint(0, 8)
            
            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0

                # Check if the board still has a unique solution
                copy_board = copy.deepcopy(self.board)
                
                if solve_sudoku(copy_board) and self.is_unique(copy_board):
                    num_to_remove -= 1
                else:
                    self.board[row][col] = backup
            

    def is_unique(self, board):
        self.solution_count = 0
        self.count_solutions(copy.deepcopy(board), 0, 0)
        return self.solution_count == 1
        
        
    def count_solutions(self, board, row, col):
        if row == 9:
            self.solution_count += 1
            return

        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)

        if board[row][col] == 0:
            for number in range(1, 10):
                if self.constraints.is_number_valid(row, col, number):
                    board[row][col] = number
                    self.count_solutions(board, next_row, next_col)
                    board[row][col] = 0
                    if self.solution_count > 1:
                        return
        else:
            self.count_solutions(board, next_row, next_col)
        

    def print_board(self):
        for row in range(9):
            if row % 3 == 0 and row != 0:
                print("══════╬═══════╬══════")

            for col in range(9):
                if col % 3 == 0 and col != 0:
                    print("║", end=" ")
                    
                val = self.board[row][col]
                print_val = val if val != 0 else "-"
                print(print_val, end=" ")
                    
                if col == 8:
                    print()


# Example Usage
generator = SudokuGenerator()
generator.fill_board()
print("Complete Board:")
generator.print_board()

generator.remove_numbers(30)
print("\nPuzzle with Removed Numbers:")
generator.print_board()