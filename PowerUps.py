#PowerUps file handles everything that has to do with the powerups: initialization, drawing, activation, and deactivation

from cmu_graphics import *
import random
from PIL import Image

#PowerUp class takes 5 parametrs(self, powerupName, positionX, poisitonY, maxUsage)
class PowerUp:
    def __init__(self, name, x, y, maxUsage):
        self.name = name
        self.x = x
        self.y = y
        self.maxUsage = maxUsage
        self.usageCount = 0
        self.available = False

#function creates powerups with paramaters fromn powerUp class above and gives each one an icon
def initializePowerUps(app):
    cellSize = min(app.width // (app.cols), (app.height-app.headerHeight) // app.rows)
    rightMargin = 50  
    gridWidth = app.cols * cellSize  

    if app.difficulty == 'easy':
        app.powerUps = [
            PowerUp('Reveal', rightMargin + gridWidth, 50, 1),
            PowerUp('Extra Life', rightMargin + gridWidth, 100, 1),
            PowerUp('Detect', rightMargin + gridWidth, 150, 1)
        ]
    elif app.difficulty == 'medium':
        app.powerUps = [
            PowerUp('Reveal', rightMargin + gridWidth, 50, 1),
            PowerUp('Extra Life', rightMargin + gridWidth, 100, 1),
            PowerUp('Detect', rightMargin + gridWidth, 150, 1)
        ]
    elif app.difficulty == 'hard':
        app.powerUps = [
            PowerUp('Reveal', rightMargin + gridWidth, 50, 1),
            PowerUp('Extra Life', rightMargin + gridWidth, 100, 1),
            PowerUp('Detect', rightMargin + gridWidth, 150, 1)
        ]
    else:
        app.powerUps = [
            PowerUp('Reveal', rightMargin + gridWidth, 50, 1),
            PowerUp('Extra Life', rightMargin + gridWidth, 100, 1),
            PowerUp('Detect', rightMargin + gridWidth, 150, 1)
        ]

    app.powerUps[0].iconC = app.revealImageC
    app.powerUps[1].iconC = app.extraLifeImageC
    app.powerUps[2].iconC = app.detectImageC
    app.powerUps[0].iconB = app.revealImageB
    app.powerUps[1].iconB = app.extraLifeImageB
    app.powerUps[2].iconB = app.detectImageB

#draws the Powerups on screen to the right of the grid
def drawPowerUps(app):
    iconSize = 100 
    spacing = 150  

    yPosition = 100   
    for powerUp in app.powerUps:
        if powerUp.available:
            drawImage(powerUp.iconC, powerUp.x, yPosition, width=iconSize, height=iconSize)
        else:
            drawImage(powerUp.iconB, powerUp.x, yPosition, width=iconSize, height=iconSize)
        yPosition += spacing

#reveals a random number of tiles/cells, depending on the difficulty   
def useReveal(app):
    if app.powerUps[0].usageCount < app.powerUps[0].maxUsage and app.powerUps[0].available:
        if app.difficulty == 'easy':
             cellsToReveal = 5
        elif app.difficulty == 'medium':
            cellsToReveal = 7
        elif app.difficulty == 'hard':
            cellsToReveal = 10
        else:
            cellsToReveal = 5

        revealedCount = 0
        totalCells = app.rows * app.cols
        cellIndices = list(range(totalCells))

        for i in range(len(cellIndices)):
            randIndex = random.randint(i, len(cellIndices) - 1)
            cellIndices[i], cellIndices[randIndex] = cellIndices[randIndex], cellIndices[i]

        for index in cellIndices:
            row = index // app.cols
            col = index % app.cols
            if not app.revealed[row][col] and (row, col) not in app.mineLocations:
                app.revealed[row][col] = True
                revealedCount += 1
                if revealedCount == cellsToReveal:
                    app.powerUps[0].usageCount +=1
                    app.powerUps[0].available = False 
                    return 

#gives user an extra chance of life                    
def useExtraLife(app):
    if app.powerUps[1].usageCount < app.powerUps[1].maxUsage and app.powerUps[1].available:
            app.powerUps[1].usageCount += 1
            app.extraLives += 1
            app.powerUps[1].available = False

# automatically flags a number of mines, depending on the difficulty
def useDetect(app):
    if not app.powerUps[2].available:
        return
    if app.difficulty == 'easy':
        detectedMines = 2
    elif app.difficulty == 'medium':
        detectedMines = 4
    elif app.difficulty == 'hard':
        detectedMines = 8
    
    if app.powerUps[2].usageCount < app.powerUps[2].maxUsage and app.powerUps[2].available:
        flaggedCount = 0
        for row in range(app.rows):
            for col in range(app.cols):
                if app.board[row][col] == -1 and (row, col) not in app.flagged:
                    app.flagged.append((row, col))
                    flaggedCount += 1
                    if flaggedCount == detectedMines:
                        return 
        app.powerUps[2].usageCount += 1   
        app.powerUps[2].available = False
    
#conditions to activate each powerup
#Reveal - active from start
#Extra Life - reveal 20 tiles
#Detect - correctly flag a certain amount of tiles
def updatePowerUpAvailability(app):
    if app.powerUps[0].usageCount >= app.powerUps[0].maxUsage:
        app.powerUps[0].available = False
    else:
        app.powerUps[0].available = True

    if app.tilesRevealed >= 20:
        if app.powerUps[1].usageCount >= app.powerUps[1].maxUsage:
            app.powerUps[1].available = False
        else:
            app.powerUps[1].available = True
    else:
        app.powerUps[1].available = False

    correctlyFlaggedMines = 0
    for (row, col) in app.flagged:
        if (row, col) in app.mineLocations:
            correctlyFlaggedMines += 1
    
    if correctlyFlaggedMines == app.minesToDetect: 
        app.powerUps[2].available = True  
    else:
        app.powerUps[2].available = False

    return app.powerUps