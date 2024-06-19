import pygame,sys,numpy as np
import pygame.draw

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("CONWAY'S GAME OF LIFE")

cell_size = 20
cols, rows = SCREEN_WIDTH // cell_size, SCREEN_HEIGHT // cell_size
grid = np.zeros((rows, cols))

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)


def start(grid,positions):
    for pos in positions:
        x,y = pos
        grid[x][y]=1

####GAME_LOGIC#######
def live(v, i, j):
    s = -v[i][j]  # Subtract the current cell from the sum
    
    for k in range(i - 1, i + 2):
        for l in range(j - 1, j + 2):
            s += v[k][l]
    
    if v[i][j] == 1:
        if s == 2 or s == 3:
            return 1
        else:
            return 0
    else:
        if s == 3:
            return 1
        else:
            return 0
 

def gameOfLife(grid):
    m = len(grid)
    n = len(grid[0])
    matrix = [[0] * (n + 2) for _ in range(m + 2)]

    for i in range(m):
        for j in range(n):
            matrix[i + 1][j + 1] = grid[i][j]

    for i in range(m):
        for j in range(n):
            a = live(matrix, i + 1, j + 1)
            grid[i][j] = a
########################

#GAME_LOOP
clock = pygame.time.Clock()
    
paused = False

positions = set()
    
while True:
    # 1. EVENT HANDLING LIKE QUITTING THE GAME ETC.
    # count = 0
    
    # positions = set()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // cell_size
            row = y // cell_size
            pos = (row, col)

            if pos in positions:
                positions.remove(pos)
            else:
                positions.add(pos)
                start(grid,positions)    
            # start(grid,positions)    
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    
                if event.key == pygame.K_RETURN:
                    grid = np.zeros((rows, cols))
                    positions.clear()  
                    paused = False
        # start(grid,positions)
        
    if paused:
        continue 
        
# 2. UPDATING POSITIONS OF GAME OBJECTS 
    # start(grid,positions)
    
# 3. DRAWING ALL THE OBJECTS, THAT IS TO SHOW THE UPDATED OBJECTS
    WINDOW.fill(GREY)
    
    # count = 0
    for y in range(rows):
        for x in range(cols):
            color = YELLOW if grid[y][x] == 1 else GREY
            pygame.draw.rect(WINDOW, color, (x * cell_size, y * cell_size, cell_size, cell_size))
            pygame.draw.rect(WINDOW, BLACK, (x * cell_size, y * cell_size, cell_size, cell_size), 1)  # Draw grid lines

    gameOfLife(grid)
    pygame.display.flip()
    clock.tick(5)  