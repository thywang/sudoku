import pygame

# constants
WIDTH, HEIGHT = 540, 610
GRID_WIDTH, GRID_HEIGHT = 450, 450
# cell side length
GAP = 50

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
        self.win = win
        # 2-d list of cells
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for i in range(rows)] for j in range(cols)]
        self.model = None
        # update model
        self.update_model()
        self.selected = None

    # function to update model (copy) of current board with confirmed values
    def update_model(self):
        self.model = [
            [self.cells[i][j].value for i in range(self.rows)] for j in range(self.cols)]
    
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
    def sketch(self, val):
        row, col = self.selected
        self.cells[row][col].temp = val

    # function to place the entered number in the cell
    def place(self, val):
        row, col = self.selected
        # check if cell is empty
        if self.cells[row][col].value == 0:
            # set the value
            self.cells[row][col].set(val)
            # update model
            self.update_model()
            # if value is valid and board can be solved
            if is_valid(self.model, (row, col), val) and self.solve():
                return True
            else:
                # change back the value
                self.cells[row][col].set(0)
                # update model
                self.update_model()
                # value can't be placed
                return False

    # function to select a cell
    def select(self, row, col):
        # reset all other cells
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].selected:
                    self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = row, col

    # function to draw the grid
    def draw(self):
        # draw grid lines
        startx = (WIDTH - GRID_WIDTH) / 2
        starty = startx + 10
        for i in range(self.rows + 1):
            if i % 3 == 0:
                line_width = 3
            else:
                line_width = 1
            # draw horizontal grid line
            pygame.draw.line(self.win, BLACK, (startx, starty + i * GAP),
                            (startx + 9 * GAP, starty + i * GAP), line_width)
            # draw vertical grid line
            pygame.draw.line(self.win, BLACK, (startx + i * GAP, starty),
                            (startx + i * GAP, starty + 9 * GAP), line_width)
        # draw the cells
        


class Cell:
    # properties: value, temp, row (i.e. y), column (i.e. x), width, height, selected (boolean)
    # note width, height are the width and height of the entire grid / board
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    # function that draws a cell
    def draw(self, win):
        pygame.draw.rect(win, BLACK, (2, 2, self.width, self.height), 1)
        # regular black border
        # thicker light blue border if selected

    # function that sets the value
    def set(self, val):
        self.value = val

# function that searches for empty cell
def search_empty(bo):
    for row in range(len(bo)):
        for col in range(len(bo[0])):
            if bo[row][col] == 0:
                return (row, col)
    # no empty cells found
    return None

# function to check if value is valid
def is_valid(bo, pos, n):
    x = pos[0]
    y = pos[1]
    # check across the row
    for i in range(len(bo[0])):
        if bo[x][i] == n and y != i:
            return False
    # check down the column
    for i in range(len(bo)):
        if bo[i][y] == n and x != i:
            return False
    # check square
    x1 = x + (3-x % 3)
    y1 = y + (3-y % 3)
    for i in range(y - y % 3, y1):
        for j in range(x - x % 3, x1):
            if bo[i][j] == n and (i, j) != pos:
                return False

    return True

def main():
    global WIDTH
    global HEIGHT
    global GRID_WIDTH
    global GRID_HEIGHT
    global GAP
    rows = 9
    cols = 9

    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku!")

    board = Grid(GRID_WIDTH, GRID_HEIGHT, rows, cols, win)

    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        win.fill(WHITE)
        board.draw()
        
        pygame.display.update()

main()
pygame.quit()
