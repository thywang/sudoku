#include <stdio.h>
#include <stdbool.h>

// helper function to print the grid
void printGrid(int g[9][9])
{
    for (int y = 0; y < 9; y++)
    {
        int min = 0;
        int max = 3;
        while (max <= 9)
        {
            printf("| ");
            for (int x = min; x < max; x++)
            {
                if (!(g[y][x]))
                {
                    printf("- ");
                }
                else
                {
                    printf("%d ", g[y][x]);
                }
            }
            min = max;
            max += 3;
        }
        printf("|");
        printf("\n");
        if (y + 1 < 9 && (y + 1) % 3 == 0)
        {
            for (int i = 0; i < 25; i++)
            {
                printf("-");
            }
            printf("\n");
        }
    }
}

// This helper function checks if it's possible for a specific cell to be a specific number
bool is_possible(int grid[9][9], int y, int x, int n)
{
    if (grid[y][x] != 0)
    {
        printf("cell is not empty\n");
        return false;
    }
    // if number doesn't appear in the row, column and square the cell occupies
    // the number is possible for the cell
    // check if x and y and n are valid
    if (n < 0 || n > 9)
    {
        printf("Invalid n value.\n");
        return false;
    }
    if (x < 0 || x > 9)
    {
        printf("Invalid x value.\n");
        return false;
    }
    if (y < 0 || y > 9)
    {
        printf("Invalid y value.\n");
        return false;
    }
    // check the row
    for (int j = 0; j < 9; j++)
    {
        if (grid[y][j] == n)
        {
            return false;
        }
    }
    // check the column
    for (int i = 0; i < 9; i++)
    {
        if (grid[i][x] == n)
        {
            return false;
        }
    }
    // check the square
    int x1, y1;
    x1 = x + (3 - x % 3);
    y1 = y + (3 - y % 3);
    for (int i = y - y % 3; i < y1; i++)
    {
        for (int j = x - x % 3; j < x1; j++)
        {
            if (grid[i][j] == n)
            {
                return false;
            }
        }
    }
    // number is not in the row, column nor square
    return true;
}

// This function solves a 9x9 sudoku puzzle
void solve(int grid[9][9])
{
    for (int y = 0; y < 9; y++)
    {
        for (int x = 0; x < 9; x++)
        {
            // if cell is empty
            if (grid[y][x] == 0)
            {
                // check through 1 to 9 to see if any number(s) can go in
                for (int i = 1; i <= 9; i++)
                {
                    if (is_possible(grid, y, x, i))
                    {
                        // place number in the cell
                        grid[y][x] = i;
                        // try to continue solving after making the choice
                        solve(grid);
                        // if we return back here, the choice was bad
                        // backtrack
                        grid[y][x] = 0;
                    }
                }
                // checked through all the possibilities for the cell
                return;
            }
        }
    }
    // print solution
    printGrid(grid);
    char c;
    printf("More? (press return)");
    scanf("%c", &c);
}

int main(void)
{
    int grid[9][9] = {{5, 3, 0, 0, 7, 0, 0, 0, 0},
                      {6, 0, 0, 1, 9, 5, 0, 0, 0},
                      {0, 9, 8, 0, 0, 0, 0, 6, 0},
                      {8, 0, 0, 0, 6, 0, 0, 0, 3},
                      {4, 0, 0, 8, 0, 3, 0, 0, 1},
                      {7, 0, 0, 0, 2, 0, 0, 0, 6},
                      {0, 6, 0, 0, 0, 0, 2, 8, 0},
                      {0, 0, 0, 4, 1, 9, 0, 0, 5},
                      {0, 0, 0, 0, 8, 0, 0, 0, 0}};
    //printGrid(grid);
    //printf("\n");
    solve(grid);
    //printf("%d\n", is_possible(grid, 8, 3, 4));
    return 0;
}