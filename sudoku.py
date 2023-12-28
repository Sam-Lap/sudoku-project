
class SudokuConstraints:
    def __init__(self, board):
        self.row_cstrs = [set() for _ in range(9)]
        self.col_cstrs = [set() for _ in range(9)]
        self.box_cstrs = [set() for _ in range(9)]
        self.empty_cells = []
        self.initialize_cstrs(board)
    
    def initialize_cstrs(self, board):
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != 0:
                    self.add_number(row, col, num)
                else:
                    self.empty_cells.append((row, col))        

    def add_number(self, row, col, num):
        self.row_cstrs[row].add(num)
        self.col_cstrs[col].add(num)
        self.box_cstrs[(row // 3) * 3 + col // 3].add(num)

    def remove_number(self, row, col, num):
        self.row_cstrs[row].remove(num)
        self.col_cstrs[col].remove(num)
        self.box_cstrs[(row // 3) * 3 + col // 3].remove(num)

    def is_number_valid(self, row, col, num):
        if (num in self.row_cstrs[row] or \
            num in self.col_cstrs[col] or \
            num in self.box_cstrs[(row // 3) * 3 + col // 3]):
            return False
        return True
       
    def get_options(self, row, col):
        box_index = (row // 3) * 3 + col // 3
        possible_numbers = set(range(1, 10))
        used_numbers = self.row_cstrs[row] | self.col_cstrs[col] | self.box_cstrs[box_index]
        return possible_numbers - used_numbers


def solve_sudoku(board):
    constraints = SudokuConstraints(board)
    return backtrack(board, constraints)

def backtrack(board, constraints):
    if not constraints.empty_cells:
        return True

    row, col = select_mrv_cell(board, constraints)
    constraints.empty_cells.remove((row, col))

    for num in constraints.get_options(row, col):
        if constraints.is_number_valid(row, col, num):
            board[row][col] = num
            constraints.add_number(row, col, num)
        
            if forward_check(constraints, row, col):
                if backtrack(board, constraints):
                    return True
            
            board[row][col] = 0
            constraints.remove_number(row, col, num)

    constraints.empty_cells.append((row, col))
    return False

def select_mrv_cell(board, constraints):
    min_options = 10
    mrv_cell = None

    for row, col in constraints.empty_cells:
        options = constraints.get_options(row, col)
        num_options = len(options)
        
        if num_options < min_options:
            min_options = num_options
            mrv_cell = (row, col)
            if num_options == 1:
                break

    return mrv_cell

def forward_check(constraints, current_row, current_col):
    for row in range(9):
        for col in range(9):
            if (row == current_row or col == current_col or \
                (row // 3 == current_row // 3 and col // 3 == current_col // 3)) and \
                (row, col) in constraints.empty_cells:   
                if len(constraints.get_options(row, col)) == 0:
                    return False
    return True

def print_board(board):
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("══════╬═══════╬══════")

        for col in range(9):
            if col % 3 == 0 and col != 0:
                print("║", end=" ")
                
            val = board[row][col]
            print_val = val if val != 0 else "-"
            print(print_val, end=" ")
                
            if col == 8:
                print()


if __name__ == "__main__":
    # Example usage
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    if solve_sudoku(board):
        print_board(board)
    else:
        print("No solution exists")