import pygame
import time

import pygame.freetype

# Initialize Pygame
pygame.init()

font_choice = pygame.font.SysFont('Comic Sans MS', 30)
maze = [
    ['S', '.', '.', '#', '.', '.', '.'],
    ['#', '#', '.', '#', '.', '#', '.'],
    ['#', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '#', '#', '#', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '.'],
    ['#', '#', '#', '#', '#', '#', 'E']
]


# Maze and display setup
cols = len(maze[0])
rows = len(maze)
WIDTH, HEIGHT = cols*100,rows*100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DFS Maze Solver")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Grid setup
cell_size = WIDTH // cols

# DFS function to solve the maze.
def dfs_maze_with_visualization(maze, x, y, visited=None, path=None):
    rows, cols = len(maze), len(maze[0])
    
    # If we don't already possess arrays or sets, we initialise them here to prevent unexpected behaviour. 
    if visited is None:
        visited = set()
    if path is None:
        path = []

    # (In order): if trying to leave grid, or trying to go through a wall, or we're about to backtrack, we don't go there...
    if x < 0 or y < 0 or x >= rows or y >= cols or maze[x][y] == '#' or (x, y) in visited:
        return False
    
    # Add current position to path
    path.append((x, y))
    visited.add((x, y))


    # Draw the current path
    screen.fill(WHITE)
    draw_maze(maze)
    # Now, everytime we run through this function, we redraw our path, which means if we've pruned elements from it, they won't be blue anymore (appear to be 'overwritten')
    for (px, py) in path:
        # Drawing our actual path.
        # Now, the reason we address x and y in the opposite order here is because the x-coordinate corresponds to the second index ("y-coordinate" of array) and vice versa. 
        pygame.draw.rect(screen, BLUE, (py * cell_size, px * cell_size, cell_size, cell_size))

    pygame.display.flip()
    pygame.time.delay(100)  # Makes our code pause so we can actually see what's going on, otherwise would be too fast too see!

    if maze[x][y] == 'E':
        pygame.draw.rect(screen,YELLOW,(y*cell_size,x*cell_size,cell_size,cell_size))
        text_surface = font_choice.render('Victory!', False, (255, 255, 0))
        screen.blit(text_surface, (0, 0))
        pygame.display.flip()
        time.sleep(1)
        return True

    # We try to move in every direction from a given point -> quickly stops barking up wrong tree due to our earlier check
    if (dfs_maze_with_visualization(maze, x + 1, y, visited, path) or
        dfs_maze_with_visualization(maze, x - 1, y, visited, path) or
        dfs_maze_with_visualization(maze, x, y + 1, visited, path) or
        dfs_maze_with_visualization(maze, x, y - 1, visited, path)):
        return True

    # If we're stuck, we remove our current position from the path and pass to the next call. 
    path.pop()
    text_surface = font_choice.render('Backtracking...', False, (255, 255, 255))
    screen.blit(text_surface, (0, 0))
    pygame.display.flip()
    time.sleep(0.8)
    return False
# Function that draws our maze for us
def draw_maze(maze):
    # looping over our maze array to draw our initial maze. 
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = WHITE
            if maze[y][x] == '#':
                color = BLACK
            elif maze[y][x] == 'S':
                color = GREEN
            elif maze[y][x] == 'E':
                color = RED
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

# Main loop
def main():
    running = True
    start_x, start_y = 0, 0  # Starting point coordinates (row, col)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Run DFS visualization
        boolVal = dfs_maze_with_visualization(maze, start_x, start_y)
        if boolVal == False:
            text_surface = font_choice.render('Unable to solve maze!', False, (255, 0, 0))
            screen.blit(text_surface, (0, 0))
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
        # Wait for a key press to close
        pygame.time.wait(2000)  # Delay at the end for the visualization to be shown
    
    pygame.quit()

if __name__ == "__main__":
    main()