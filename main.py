import pygame
import sys
import time  # For adding delay
import random

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_SIZE = 600
GRID_SIZE = SCREEN_SIZE // 9
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Sudoku Solver")
font = pygame.font.Font(None, 40)


# Drawing functions
def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            line_width = 4
        else:
            line_width = 1
        pygame.draw.line(screen, pygame.Color('black'), (i * GRID_SIZE, 0), (i * GRID_SIZE, SCREEN_SIZE), line_width)
        pygame.draw.line(screen, pygame.Color('black'), (0, i * GRID_SIZE), (SCREEN_SIZE, i * GRID_SIZE), line_width)


def fill_numbers(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, pygame.Color('blue'))
                screen.blit(text, (j * GRID_SIZE + GRID_SIZE // 3, i * GRID_SIZE + GRID_SIZE // 7))


def update_display(grid):
    screen.fill(pygame.Color('white'))
    draw_grid()
    fill_numbers(grid)
    pygame.display.flip()


# Modified solve_sudoku to work with Pygame
def solve_sudoku(grid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    empty = find_empty(grid)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            update_display(grid)
            time.sleep(0.2)  # Adjust delay for visibility

            if solve_sudoku(grid):
                return True

            grid[row][col] = 0  # Backtrack
            update_display(grid)
            time.sleep(0.05)  # Adjust delay for visibility

    return False


def remove_numbers(grid, cells_to_remain=20):
    """Remove numbers from the grid randomly but ensure at least 'cells_to_remain' are filled."""
    cells_filled = sum(1 for row in grid for cell in row if cell != 0)
    cells_to_remove = 81 - cells_to_remain

    while cells_to_remove > 0 and cells_filled > cells_to_remain:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            cells_filled -= 1
            cells_to_remove -= 1


def fill_grid(grid):
    empty = find_empty(grid)
    if not empty:
        return True  # Success: grid fully filled
    row, col = empty

    numbers = list(range(1, 10))
    random.shuffle(numbers)  # Randomize the numbers to generate different solutions
    for num in numbers:
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if fill_grid(grid):
                return True
            grid[row][col] = 0  # Backtrack

    return False  # Failure: no valid number found for this cell


def create_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_grid(grid)  # Fill the grid completely
    remove_numbers(grid, cells_to_remain=40)  # Remove numbers to create the puzzle
    # Ensure solve_sudoku fills the entire grid
    successfully_solved = solve_sudoku(grid)
    if not successfully_solved:
        raise Exception("Failed to solve the grid from an empty state.")
    # Then remove numbers to create the puzzle, ensuring at least 20 cells remain filled
    # remove_numbers(grid, cells_to_remain=20)
    return grid


def is_valid(grid, row, col, num):
    # Check row and column
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    # Check 3x3 subgrid
    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[subgrid_row + i][subgrid_col + j] == num:
                return False
    return True


def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


# Main function to run the solver
def main():
    global grid
    grid = create_sudoku()  # Prepare the grid
    update_display(grid)
    solved = solve_sudoku(grid)
    if solved:
        print("Puzzle Solved!")
    else:
        print("No solution found.")

    # Keep the window open until the user closes it
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
