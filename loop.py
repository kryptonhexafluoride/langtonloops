import numpy as np
import pygame

from copy import deepcopy

# these are the minimum values
#TODO: make these adjustable by the user when the program starts
SCREEN_SIZE = 800
GRID_SIZE = 200
FRAMES_PER_SECOND = 10
COLOURS = [
    "#00202e",
    "#2c4875",
    "#8a508f",
    "#bc5090",
    "#ff6361",
    "#ff8531",
    "#ffa600",
    "#ffd380"
]
STARTING_POSITIONS = {
    (0, 1): 2,
    (0, 2): 2,
    (0, 3): 2,
    (0, 4): 2, 
    (0, 5): 2,
    (0, 6): 2,
    (0, 7): 2,
    (0, 8): 2, 
    (1, 0): 2,
    (1, 1): 1,
    (1, 2): 7,
    (1, 4): 1, 
    (1, 5): 4, 
    (1, 7): 1, 
    (1, 8): 4,
    (1, 9): 2, 
    (2, 0): 2,
    (2, 2): 2,
    (2, 3): 2,
    (2, 4): 2, 
    (2, 5): 2,
    (2, 6): 2,
    (2, 7): 2, 
    (2, 9): 2,
    (3, 0): 2,
    (3, 1): 7, 
    (3, 2): 2,
    (3, 7): 2, 
    (3, 8): 1,
    (3, 9): 2,
    (4, 0): 2, 
    (4, 1): 1, 
    (4, 2): 2, 
    (4, 7): 2, 
    (4, 8): 1, 
    (4, 9): 2,
    (5, 0): 2, 
    (5, 2): 2, 
    (5, 7): 2,
    (5, 8): 1, 
    (5, 9): 2,
    (6, 0): 2, 
    (6, 1): 7,
    (6, 2): 2, 
    (6, 7): 2, 
    (6, 8): 1, 
    (6, 9): 2, 
    (7, 0): 2, 
    (7, 1): 1, 
    (7, 2): 2, 
    (7, 3): 2, 
    (7, 4): 2, 
    (7, 5): 2, 
    (7, 6): 2, 
    (7, 7): 2, 
    (7, 8): 1,
    (7, 9): 2, 
    (7, 10): 2, 
    (7, 11): 2, 
    (7, 12): 2, 
    (7, 13): 2, 
    (8, 0): 2,
    (8, 2): 7,
    (8, 3): 1, 
    (8, 5): 7, 
    (8, 6): 1, 
    (8, 8): 7, 
    (8, 9): 1,
    (8, 10): 1,
    (8, 11): 1, 
    (8, 12): 1, 
    (8, 13): 1, 
    (8, 14): 2, 
    (9, 1): 2, 
    (9, 2): 2, 
    (9, 3): 2, 
    (9, 4): 2, 
    (9, 5): 2, 
    (9, 6): 2, 
    (9, 7): 2, 
    (9, 8): 2, 
    (9, 9): 2, 
    (9, 10): 2, 
    (9, 11): 2, 
    (9, 12): 2, 
    (9, 13): 2, 

    #TODO: FINISH THIS 
}

DIMENSION = SCREEN_SIZE/GRID_SIZE
GRID_CENTRE = int(GRID_SIZE/2)

# parse rules
rules = {}
rules_file = open("rules.txt", "r")
for rule in rules_file.readlines():
    rule = rule.strip()
    value = int(rule[-1])
    key = rule[:-1]
    rules[key] = value

# initialise grid 
grid = np.full((GRID_SIZE, GRID_SIZE), 0)
for (x, y) in STARTING_POSITIONS.keys():
    grid[x+GRID_CENTRE][y+GRID_CENTRE] = STARTING_POSITIONS[(x,y)]

def update_grid():
    new_grid = deepcopy(grid)
    for i in range(0, GRID_SIZE):
        for j in range(0, GRID_SIZE):
            # check each neighbour 
            # look up the configuration in the rules list 
            # update colour as needed
            curr = new_grid[i][j]
            top = new_grid[i-1][j] if (i-1 > -1) else new_grid[GRID_SIZE-1][j]
            bottom = new_grid[i+1][j] if (i+1 < GRID_SIZE) else new_grid[0][j]
            left = new_grid[i][j-1] if (j-1 > -1) else new_grid[i][GRID_SIZE-1]
            right = new_grid[i][j+1] if (j+1 < GRID_SIZE) else new_grid[i][0]

            key1 = str(curr) + str(top) + str(right) + str(bottom) + str(left) 
            if(key1 in rules.keys()):
                grid[i][j] = rules[key1]
            else:
                key2 = str(curr) + str(right) + str(bottom) + str(left) + str(top)
                if(key2 in rules.keys()):
                    grid[i][j] = rules[key2]
                else: 
                    key3 = str(curr) + str(bottom) + str(left) + str(top) + str(right)
                    if(key3 in rules.keys()):
                        grid[i][j] = rules[key3]
                    else: 
                        key4 = str(curr) + str(left) + str(top) + str(right) + str(bottom)
                        if(key4 in rules.keys()):
                            grid[i][j] = rules[key4]
    
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # remove stuff from last frame 
    screen.fill("black")

    for i in range(0, GRID_SIZE):
        for j in range(0, GRID_SIZE):
            rect = pygame.Rect(DIMENSION*i, DIMENSION*j, DIMENSION, DIMENSION)
            colour = grid[i][j]
            pygame.draw.rect(screen, COLOURS[colour], rect)

    pygame.display.flip()
    clock.tick(FRAMES_PER_SECOND)
    update_grid()

pygame.quit()