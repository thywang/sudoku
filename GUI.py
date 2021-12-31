import pygame

# set up display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku!")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Grid:
    board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
             [6, 0, 0, 1, 9, 5, 0, 0, 0],
             [0, 9, 8, 0, 0, 0, 0, 6, 0],
             [8, 0, 0, 0, 6, 0, 0, 0, 3],
             [4, 0, 0, 8, 0, 3, 0, 0, 1],
             [7, 0, 0, 0, 2, 0, 0, 0, 6],
             [0, 6, 0, 0, 0, 0, 2, 8, 0],
             [0, 0, 0, 4, 1, 9, 0, 0, 5],
             [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    # properties: width, height, row, column
    def __init__(self, width, height, rows, cols, win):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        # 2-d list of cells
        self.cells = [[Cell(self.board[i][j], i, j, width, height)
                       for i in range(rows)] for j in range(cols)]
        self.model = None
        # update model
        self.update_model()
        self.selected = None
        self.win = win

    # function to update model (copy) of current board with confirmed values
    def update_model(self):
        self.model = [
            [self.board[i][j].value for i in range(self.rows)] for j in range(self.cols)]
    
    # function that checks if the current board (with only the confirmed / entered values) can be solved
    def solve(self):
        found = search_empty(self.model)
        if not found:
            # board is solved
            return True
        else:
            # empty position found
            row, col = found

        # check through 1 to 9 to see if any number(s) can go in
        for i in range(1, 10):
            if is_valid(self.model, (row, col), i):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0
                    
        return False
        
    # function to sketch the guessed number
    # function to check if the number entered is correct
    # function to place the entered number in the cell
    # function to highlight a cell


class Cell:
    # properties: value, temp, row (i.e. y), column (i.e. x), width, height, selected (boolean)

    def __init__(self, value, temp, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

# function that searches for empty cell
def search_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    # no empty cells found
    return None

# function to check if value is valid
def is_valid(board, pos, n):
    x = pos[0]
    y = pos[1]
    # check row
    for i in range(9):
        if board[x][i] == n and y != i:
            return False
    # check column
    for i in range(9):
        if board[i][y] == n and x != i:
            return False
    # check square
    x1 = x + (3-x % 3)
    y1 = y + (3-y % 3)
    for i in range(y - y % 3, y1):
        for j in range(x - x % 3, x1):
            if board[i][j] == n and (i,j) != pos:
                return False

    return True

# def main():