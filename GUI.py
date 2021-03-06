import pygame

pygame.init()

# constants
WIDTH, HEIGHT = 540, 610
GRID_WIDTH, GRID_HEIGHT = 450, 450
# cell side length
GAP = 50

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (89, 221, 255)
RED = (255, 0, 0)

# fonts
VALUE_FONT = pygame.font.SysFont('helveticaneue', 35)
SKETCH_FONT = pygame.font.SysFont('helveticaneue', 15)


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
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        # update model
        self.update_model()
        # the position (row, col) of selected cell
        self.selected = None

     # function to draw the grid
    def draw(self):
        # draw grid lines
        start_x = (WIDTH - GRID_WIDTH) / 2
        start_y = start_x + 10
        for i in range(self.rows + 1):
            if i % 3 == 0:
                line_width = 3
            else:
                line_width = 1
            # draw horizontal grid line
            pygame.draw.line(self.win, BLACK, (start_x, start_y + i * GAP),
                             (start_x + 9 * GAP, start_y + i * GAP), line_width)
            # draw vertical grid line
            pygame.draw.line(self.win, BLACK, (start_x + i * GAP, start_y),
                             (start_x + i * GAP, start_y + 9 * GAP), line_width)

        # draw the cells (write numbers inside cells)
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw_num(self.win, start_x, start_y)

    # function to update model (copy) of current board with confirmed values
    def update_model(self):
        self.model=[[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # function that checks if the current board (with only the confirmed / entered values) can be solved
    def solve(self):
        found = search_empty(self.model)
        if not found:
            # board is full / solved
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

                # cannot solve, so change back to 0
                self.model[row][col] = 0
                    
        return False

    # function that solves the board with animation
    def gui_solve(self):
        start_x = (WIDTH - GRID_WIDTH) / 2
        start_y = start_x + 10
        # uses just the model
        self.update_model()
        found = search_empty(self.model)
        if not found:
            # board is full / solved
            return True
        else:
            # empty position found
            row, col = found

        # check through 1 to 9 to see if any number(s) can go in
        for i in range(1, 10):
            if is_valid(self.model, (row, col), i):
                self.model[row][col] = i
                self.cells[row][col].set(i)
                # assume it's true
                self.cells[row][col].draw_change(self.win, start_x, start_y, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.gui_solve():
                    return True

                # cannot solve, so change back to 0
                self.model[row][col] = 0
                self.cells[row][col].set(0)
                self.update_model()
                # it's false
                self.cells[row][col].draw_change(self.win, start_x, start_y, False)
                pygame.display.update()
                pygame.time.delay(100)


        return False
        
    # function that checks if the board is full
    def is_full(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].value == 0:
                    # empty cell found
                    return False
        # no empty cells found
        return True
       
    # function that returns the row and column of cell clicked
    def click(self, pos):
        start_x = (WIDTH - GRID_WIDTH) / 2
        start_y = start_x + 10
        x, y = pos
        # if x and y within the board
        if start_x < x < start_x + GRID_WIDTH and start_y < y < start_y + GRID_HEIGHT:
            # get row and column
            row = int((y - start_y) // GAP)
            col = int((x - start_x) // GAP)
            return (row, col)
        else:
            return None
    
    # function that clears a cell
    def clear(self):
        row, col = self.selected
        # if there's no confirmed value in the cell
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    # function to sketch the guessed number
    def sketch(self, num):
        row, col = self.selected
        self.cells[row][col].set_temp(num)

    # function to place the entered number in the cell (if possible)
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
                # reset the temp
                self.cells[row][col].set_temp(0)
                # update model
                self.update_model()
                # value can't be placed
                return False

    # function to select a cell
    def select(self, row, col):
        # reset all cells
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].selected:
                    self.cells[i][j].selected = False
        
        # select the specific cell
        self.cells[row][col].selected = True
        self.selected = row, col
                

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
    
    # function that draws the number in the cell
    def draw_num(self, win, start_x, start_y):
        # fixed bug: x corresponds to col, y corresponds to row, not the other way around
        x = start_x + GAP * self.col
        y = start_y + GAP * self.row

        # if cell is empty and a temporary value is entered
        if self.temp != 0 and self.value == 0:
            text = SKETCH_FONT.render(str(self.temp), 1, GRAY)
            win.blit(text, (x + 5, y + 5))
        # if cell isn't empty
        elif self.value != 0:
            text = VALUE_FONT.render(str(self.value), 1, BLACK)
            win.blit(text, (x + (GAP - text.get_width()) / 2, y + (GAP - text.get_height()) / 2))
        
        # draw thicker light blue border if selected
        if self.selected:
            pygame.draw.rect(win, LIGHT_BLUE, (x, y, GAP, GAP), 3)

    # function that draws the change of a cell
    def draw_change(self, win, start_x, start_y, correct=True):
        x = start_x + GAP * self.col
        y = start_y + GAP * self.row

        # cover up the cell
        pygame.draw.rect(win, WHITE, (x, y, GAP, GAP), 0)

        # write value
        text = VALUE_FONT.render(str(self.value), 1, BLACK)
        win.blit(text, (x + (GAP - text.get_width()) / 2, y + (GAP - text.get_height()) / 2))

        # correct -- draw light blue border
        if correct:
            pygame.draw.rect(win, LIGHT_BLUE, (x, y, GAP, GAP), 3)
        # incorrect -- draw red border
        else:
            pygame.draw.rect(win, RED, (x, y, GAP, GAP), 3)

    # function that sets the value
    def set(self, val):
        self.value = val

    # function that sets the temporary value
    def set_temp(self, temp):
        self.temp = temp

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
    # pos sent in as (row, col)
    # which is (y, x)
    y = pos[0]
    x = pos[1]
    # check across the row
    for i in range(len(bo[0])):
        if bo[y][i] == n and x != i:
            return False
    # check down the column
    for i in range(len(bo)):
        if bo[i][x] == n and y != i:
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

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku!")

    board = Grid(GRID_WIDTH, GRID_HEIGHT, rows, cols, win)
    running = True
    key = None

    # control how fast the screen updates
    clock = pygame.time.Clock()
    frame_count = 0
    FPS = 60

    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6 
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                # for keypad
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_s:
                    board.gui_solve()

                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                     
                if event.key == pygame.K_RETURN:
                    row, col = board.selected
                    if board.cells[row][col].temp != 0:
                        if board.place(board.cells[row][col].temp):
                            print("Correct!")
                        else:
                            print("Incorrect.")
                    key = None
                    
                    # check if all the cells are filled
                    if board.is_full():
                        print("Complete!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get (x, y) position of mouse
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                # if a cell is clicked
                if clicked:
                    # clicked[0] is the row, clicked[1] is the column
                    board.select(clicked[0], clicked[1])
                    key = None
        
        if board.selected and key != None:
            board.sketch(key)
        
        win.fill(WHITE)

        # "stopwatch"
        # calculate total seconds
        total_seconds = frame_count // FPS
        # divide by 60 to get total minutes
        minutes = total_seconds // 60
        # use modulus to get seconds
        seconds = total_seconds % 60
        # use string formatting to format in leading zeroes
        output = "{0:02}:{1:02}".format(minutes, seconds)

        # render and blit
        text = VALUE_FONT.render(output, True, BLACK)
        win.blit(text, [400, 530])

        frame_count += 1

        # limit frames per second
        clock.tick(FPS)

        board.draw()
        pygame.display.update()

main()
pygame.quit()