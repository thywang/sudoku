# This helper function checks if it's possible for a specific cell to be a specific number


def is_possible(board, y, x, n):
    if board[y][x] != 0:
        print("cell is not empty")
        return False
    # if number doesn't appear in the row, column and square the cell occupies
    # the number is possible for the cell
    # check if x and y and n are valid
    if n < 0 or n > 9:
        print("Invalid value for n")
        return False
    if x < 0 or x > 9:
        print("Invalid value for x")
        return False
    if y < 0 or y > 9:
        print("Invalid value for y")
        return False

    # check the row
    for j in range(0, 9):
        # second condition is to prevent checking where we want to place value in
        if board[y][j] == n and x != j:
            return False
    # check the column
    for i in range(0, 9):
        # second condition is to prevent checking where we want to place value in
        if board[i][x] == n and y != i:
            return False
    # check the square
    x1 = x + (3-x % 3)
    y1 = y + (3-y % 3)
    for i in range(y - y % 3, y1):
        for j in range(x - x % 3, x1):
            # second condition is to prevent checking where we want to place value in
            if board[i][j] == n and (i,j) != (x,y):
                return False

    # number is not in the row, column nor square
    return True

# This function solves a 9x9 sudoku puzzle


def solve(board):
    for y in range(0, 9):
        for x in range(0, 9):
            # if cell is empty
            if board[y][x] == 0:
                # check through 1 to 9 to see if any number(s) can go in
                for i in range(1, 10):
                    if is_possible(board, y, x, i):
                        board[y][x] = i
                        solve(board)
                        board[y][x] = 0
                return
    print_board(board)
    input("More?")

# helper function to print out the board


def print_board(board):
    for y in range(9):
        min = 0
        max = 3
        while max <= 9:
            print("| ", end=" ")
            for x in range(min, max):
                if (not(board[y][x])):
                    print("- ", end=" ")
                else:
                    print("%d " % (board[y][x]), end=" ")
            min = max
            max += 3
        print("|")
        if y + 1 < 9 and (y + 1) % 3 == 0:
            for i in range(19):
                print("-", end=" ")
            print()


# main program
board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]
# print(board)
solve(board)
