import pygame,sys,numpy as np
import pygame.draw

##GAME RULES, PRESS SPACE_BAR TO START, RESUME OR PAUSE, 
### AND PRESS ENTER KEY IF YOU WANT TO RESET ALL THE CELL SELECTIONS YOU HAVE MADE

pygame.init()

# ENTER THE HEIGHT AND WIDTH OF WINDOW WHICH WILL BE DISPLAYED LATER ON

SCREEN_HEIGHT = int(input("Enter the GRID height (eg. 800): "))   
SCREEN_WIDTH = int(input("Enter the GRID width (eg. 800): "))

# SETTING UP THE WINDOW WHERE OUR GAME WILL GET DISPLAYED, WITH THE PARAMETERS ENTERED BY THE USER

WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# DEFINING THE CELL SIZE OF THE GRID   

cell_size = 20
cols, rows = SCREEN_WIDTH // cell_size, SCREEN_HEIGHT // cell_size ##TOTAL ROWS AND COLUMNS IN OUR GRID


# DEFINING THE RGB CODE FOR COLOR OF THE OBJECTS WHICH WILL APPEAR ON OUR SCREEN
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)


# THIS FUNCTION WILL HELP US IN CREATING A GRID ON OUR SCREEN, AS THE ACTUAL GAME
# WHERE WE WILL SELECT THE CELLS


#positions is the set of x and y coordinates of each live cell in the grid
def GRID_CREATE(positions):
    
    # HERE I AM DEFINING THE COLOR OF LIVE CELL, CHOSEN YELLOW FOR IT
    for position in positions:
        x, y = position
        pygame.draw.rect(WINDOW, YELLOW, (x * cell_size, y * cell_size, cell_size, cell_size))


# CREATING THE GRID LINES     
    # HERE I AM MAKING THE HORIZONTAL LINES FOR THE GRID
    for y in range(rows):
        pygame.draw.line(WINDOW, WHITE, (0, y * cell_size), (SCREEN_WIDTH, y * cell_size))
    # SIMILARILY CREATING THE VERTICAL LINES FOR THE GRID
    for x in range(cols):
        pygame.draw.line(WINDOW, WHITE, (x * cell_size, 0), (x * cell_size, SCREEN_HEIGHT))
        
        
#################### GAME_LOGIC ########################

# THIS FUNCTION IS HELPFUL IN RETURNING THE LIST OF COORDINATES OF THE CELLS
# NEIGHBOURING TO THE CELL THAT HAS COORDINATES POSITION, WHICH IS AN ARGUMENT IN THIS FUNCTION

def total_neighbours(pos):
    list = []
    
    x,y = pos
    
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if((x==i and j==y) or (i>=SCREEN_HEIGHT or j>=SCREEN_WIDTH)):
                continue
            else:
                list.append((i,j))
                
    return list

# THE FUNCTION WILL RETURN THE UPDATED COORDINATES OF LIVE CELLS
def new_grid(positions):
    positions_new = set() # THIS SET WILL CONTAIN THE POSITION OF NEW LIVE CELL
    all_neighbours = set() # AN EXTRA SET DEFINED HELPFUL FOR MANAGING THE ENTRIES OF positions_new
    
    for pos in positions:                   #  FOR EVERY POSITION IN THE SET POSITIONS
        neighbours = total_neighbours(pos)  #  POSITIONS OF ALL THE NEIGHBOURHOOD CELLS ARE ENTERED TO NEIGHBOURS SET
        all_neighbours.update(neighbours)   #  AND FOR EVERY POS, all_neighbours IS UPDATED WITH THE NEW POSITIONS

        count = 0                           
        
        ##THIS CODE BLOCK HELPS IN FINDING WHETHER THE ALREADY LIVING CELLS WILL STAY ALIVE OR NOT
        for neighbour in neighbours:
            if neighbour in positions:
                count += 1
        
        if count in [2, 3]:
            positions_new.add(pos)
        #######################################
        
    ##THIS CODE BLOCK HELPS IN FINDING WHETHER ANY DEAD CELL WILL GET ALIVE OR NOT
    for pos in all_neighbours:
        neighbours = total_neighbours(pos)
        
        count = 0
        
        for neighbour in neighbours:    #THIS TIME WE ARE INTERESTED IN THE NEIGHBOURS OF LIVING CELLS, AS ONLY SUCH CELLS HAVE POTENTIAL 
            if neighbour in positions:  # BECAUSE EVERY DEAD CELL REQUIRES, LIVING CELLS AROUND TO GET ALIVE, SO WE CHECK IF THERE ARE ANY DEAD CELL 
                count += 1              # SURROUNDING THE LIVING CELL AS THERE MIGHT BE SOME POSSIBILITY FOR IT TO GET ALIVE
        
        if count == 3:
            positions_new.add(pos)
    
    return positions_new

############################################

def main():
    
    clock = pygame.time.Clock()

    running = True
    paused = False
    frq = 60
    count = 0
    positions = set()
    
    while running:
        
        clock.tick(500) # SET THE FPS TO 500, BASICALLY THE SPEED OF CHANGES IN THE CELL, HIGHER THE VALUE, HIGHER IS THE SPEED OF CHANGES THAT TAKE PLACE
         
         
        # FOLLOWING CODE BLOCK IS HELPFUL IN DETERMINING THE PERIOD BREAK TO UPDATE THE
        # GRID WITH THE CHANGES, WHEN THE GAME IS PAUSED AND THE LOOP KEEPS ON ITERATING 
        # , IF THE COUNT >= 60 IT STARTS UPDATING THE POSITIONS ELSE IT WAITS FOR IT TO GET TO 60
        # BEFORE SHOWING ANY CHANGE
        if paused:
            count += 1
        
        if count >= frq:
            count = 0
            positions = new_grid(positions)
         
        pygame.display.set_caption("PLAYING :)" if paused else "PAUSED :(" )#DISPLAYS PAUSED IF GAME IS PAUSED ELSE PLAYING
        
        for event in pygame.event.get(): #HELPS IN HANDLIND THE EVENTS, BASED ON WHAT THE USER DOES
            if event.type == pygame.QUIT: #QUITS WHEN QUIT OPTION CHOSEN
                running = False
         
            if event.type == pygame.MOUSEBUTTONDOWN: #SELECTS A CELL WHEN CHOSEN
                x, y = pygame.mouse.get_pos()
                col = x // cell_size
                row = y // cell_size
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
                  
            if event.type == pygame.KEYDOWN: ##WHEN PRESSED A KEY
                if event.key == pygame.K_SPACE: ##IF THE KEY IS SPACE-BAR, THE GAME CONTINUES IF PAUSED AND VICE VERSA
                    paused = not paused
                    
                if event.key == pygame.K_RETURN: #RESETS ALL THE MARKED CELLS IF ENTERY IS PRESSED
                    count = 0
                    positions = set()
                    paused = False


        WINDOW.fill(BLACK) #FILLS THE COLOR OF WINDOW, CHOSEN BLACK
        GRID_CREATE(positions) #CREATES THE GRID
        pygame.display.update() #UPDATES WITH ALL THE CHANGES AND STEPS
        
        
##EXECUTE!
if __name__ == "__main__":
    main()