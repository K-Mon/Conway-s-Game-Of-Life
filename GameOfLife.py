import pygame, sys, os
import numpy as np
from pygame.locals import *
import button

def arraySetUp():
    ## Create the underlying array that represents the environment
    grid = np.zeros((TOTALBLOCKS,TOTALBLOCKS))
    return grid

def rectSetUp(grid):
    ## Set up the rectangle Positions
    origI, origJ = 100, 50
    blocks = []
    for i in range(TOTALBLOCKS):
        tempI = origI; tempJ = origJ
        row = []
        for j in range(TOTALBLOCKS):
            block = pygame.Rect(tempI, tempJ, BSIZE, BSIZE)
            row.append( block)
            tempI += BSIZE
        
        blocks.append(row)
        origJ += BSIZE
        origI = 100

    return blocks

def drawRectangles(grid, blocks):
    ## Draw the rectangles
    for i in range(TOTALBLOCKS):
        for j in range(TOTALBLOCKS):
            if grid[i ,j] == 0:
                pygame.draw.rect(DISPLAYSURFACE, DEAD, blocks[i][j])
            else:
                pygame.draw.rect(DISPLAYSURFACE, LIVE, blocks[i][j])

def updateButtons(window, buttons, mousePosition, mouseClick):
    for button in buttons:
        button.drawButton(window, mousePosition, mouseClick)

def cellSelected(mousePosition):
    ## Checks to see if a cell is selected
    if mousePosition[0] < 701 and mousePosition[0] > 99:
        if mousePosition[1] < 651 and mousePosition[1] > 49:
            return True
    else:
        return False

def updateStatus(grid, blocks, mousePosition):
    for i in range(TOTALBLOCKS):
        for j in range(TOTALBLOCKS):
            if blocks[i][j].collidepoint(mousePosition[0],
                                                     mousePosition[1]):
                grid[i][j] = 1

    return grid

def simulate(grid):
    ## Simulate the round, create the new Array that will hold the new values
    nextGrid = grid.copy()
    for i in range(TOTALBLOCKS):
        for j in range(TOTALBLOCKS):
            cell = grid[i ,j]
            nextGrid = cellRules(grid, nextGrid, cell, i, j)

    return nextGrid

def cellRules(grid, nextGrid, cell, i, j):
    ## This function will play out the simulation rules
    ## If cell is not a wall
    aliveCount = 0
    neighbors = np.array([])

    ## Upper Left Corner
    if i == 0 and j == 0:

        neighbors = np.append(neighbors, grid[i, j + 1])
        neighbors = np.append(neighbors, grid[i + 1, j + 1])
        neighbors = np.append(neighbors, grid[i + 1, j])
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid = determineStatus(i, j, cell, aliveCount, nextGrid)

    ## Upper right corner
    elif i == 0 and j == TOTALBLOCKS - 1:

        neighbors = np.append(neighbors, grid[i, j - 1])
        neighbors = np.append(neighbors, grid[i + 1, j - 1])
        neighbors = np.append(neighbors, grid[i + 1, j])
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid = determineStatus(i, j,cell, aliveCount, nextGrid)

    ## Lower Left Corner
    elif j == 0 and i == TOTALBLOCKS - 1:

        neighbors = np.append(neighbors, grid[i, j + 1])
        neighbors = np.append(neighbors, grid[i - 1, j + 1])
        neighbors = np.append(neighbors, grid[i - 1, j])
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid  = determineStatus(i, j,cell, aliveCount, nextGrid)

    ## Lower Right Corner
    elif j == TOTALBLOCKS - 1 and i == TOTALBLOCKS -1:

        neighbors = np.append(neighbors, grid[i, j - 1])
        neighbors = np.append(neighbors, grid[i - 1, j - 1])
        neighbors = np.append(neighbors, grid[i - 1, j])
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid  = determineStatus(i, j,cell, aliveCount, nextGrid)

    ## Left column
    elif j == 0:

        neighbors = np.append(neighbors, grid[i, j + 1]) ## right
        neighbors = np.append(neighbors, grid[i + 1, j + 1]) ## lower Diag
        neighbors = np.append(neighbors, grid[i - 1, j]) ## Top
        neighbors = np.append(neighbors, grid[i - 1, j + 1]) ## Upper Diag
        neighbors = np.append(neighbors, grid[i + 1, j]) ## bottom
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid  = determineStatus(i, j,cell, aliveCount, nextGrid)
        
    ## Top row
    elif i == 0:

        neighbors = np.append(neighbors, grid[i, j + 1]) ## right
        neighbors = np.append(neighbors, grid[i + 1, j + 1]) ## lower Right Diag
        neighbors = np.append(neighbors, grid[i, j - 1]) ## left
        neighbors = np.append(neighbors, grid[i + 1, j - 1]) ## lower Left Diag
        neighbors = np.append(neighbors, grid[i + 1, j]) ## bottom
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid  = determineStatus(i, j,cell, aliveCount, nextGrid)

    ## Right column
    elif j == TOTALBLOCKS - 1:

        neighbors = np.append(neighbors, grid[i, j - 1]) ## left
        neighbors = np.append(neighbors, grid[i + 1, j - 1]) ## lower Diag
        neighbors = np.append(neighbors, grid[i - 1, j]) ## top
        neighbors = np.append(neighbors, grid[i - 1, j - 1]) ## Upper Diag
        neighbors = np.append(neighbors, grid[i + 1, j]) ## bottom
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid  = determineStatus(i, j,cell, aliveCount, nextGrid)
    
    # Bottom row
    elif i == TOTALBLOCKS - 1:
        neighbors = np.append(neighbors, grid[i, j + 1]) ## right
        neighbors = np.append(neighbors, grid[i - 1, j + 1]) ## upper Right Diag
        neighbors = np.append(neighbors, grid[i, j - 1]) ## left
        neighbors = np.append(neighbors, grid[i - 1, j - 1]) ## upper Left Diag
        neighbors = np.append(neighbors, grid[i - 1, j]) ## top
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid = determineStatus(i, j,cell, aliveCount, nextGrid)

    else: ## Middle Blocks 
        ## Get upper neighbors
        neighbors = np.append(neighbors, grid[i - 1, j - 1: j + 2])
        ## Get lower neighbors 
        neighbors = np.append(neighbors, grid[i + 1, j - 1: j + 2])
        ## adjacent neighbors
        neighbors = np.append(neighbors, grid[i, j - 1]) ## Left
        neighbors = np.append(neighbors, grid[i, j + 1]) ## Right
        aliveCount = neighborCT(neighbors, aliveCount)
        nextGrid  = determineStatus(i, j, cell, aliveCount, nextGrid)

    return nextGrid

def neighborCT(neighbors, count):
    ## Counts the alive neighbors 
    for neighbor in neighbors:
        if neighbor == 1:
                count += 1
    return count

def determineStatus(i, j, cell, aliveCount, nextGrid):
    ## If alive and count > 3 or < 2 then it is dead.
    if cell == 1:
        if aliveCount > 3 or aliveCount < 2:
            nextGrid[i, j] = 0
    else:
        if aliveCount == 3:
            nextGrid[i, j] = 1

    return nextGrid


def main():

    global DISPLAYSURFACE, TOTALBLOCKS, LIVE, DEAD, WINDOWSIZE, BSIZE
    TOTALBLOCKS = 18; LIVE = (255, 128, 0); DEAD = (255, 255, 255)
    WINDOWSIZE = 800; BSIZE = round(600/TOTALBLOCKS)
    pygame.init()
    pygame.display.set_caption("Game Of Life")
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
    ## Store the mouse coordinates
    mousePos = (0,0)
    ##set up the background grid and the array of blocks
    grid = arraySetUp()
    blocks = rectSetUp(grid)
    ## set background color
    ## Set up the start, stop, and reset button
    x = 109; y = 675; w = 175; h = 100
    startButton = button.Button((100, 200, 0), x, y, w, h, text = "Start")
    stopButton = button.Button((255, 100, 0), x + 200, y, w, h, text = "Stop")
    resetButton = button.Button((55, 100, 255), x + 400, y, w, h, text = "Reset")
    buttons = (startButton, stopButton, resetButton)
    ## set up the status that will determine that the simulation can run
    status = False
    ## main loop
    while True:

        ## initialize variables 
        mouseClick = False

        ## Create the environemnt section of the window
        DISPLAYSURFACE.fill((150, 150, 150))
        updateButtons(DISPLAYSURFACE, buttons, mousePos, mouseClick)

        # event handling loop
        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos() 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                os.exit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouseClick = True
            
        drawRectangles(grid, blocks)
        ## If the status = False the simulation does not run
        if status == False:

            if mouseClick == True:
                ## if the start, reset, stop button selected do something
                if cellSelected(mousePos) == True:
                    grid = updateStatus(grid, blocks, mousePos)
                ## If the start Button is pressed start the game
                elif startButton.getRect().collidepoint(mousePos[0], mousePos[1]):
                    startButton.drawButton(DISPLAYSURFACE, mousePos, mouseClick)
                    status = True
                # If the reset button is pressed reset the grid to blank
                elif resetButton.getRect().collidepoint(mousePos[0], mousePos[1]):
                    resetButton.drawButton(DISPLAYSURFACE, mousePos, mouseClick)
                    grid = arraySetUp()

        ## If the status is true the only options are to let it play out or stop it       
        else:
            if mouseClick == True:
                ## The stop Button will stop the simulation
                if stopButton.getRect().collidepoint(mousePos[0], mousePos[1]):
                    stopButton.drawButton(DISPLAYSURFACE, mousePos, mouseClick)
                    status = False

            grid = simulate(grid)
            pygame.time.wait(500)


        pygame.display.update()

main()