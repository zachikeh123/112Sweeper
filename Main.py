#Main file controls all the gameplay and its logic

from cmu_graphics import *
from PowerUps import *
from Graphics import *
import random
from PIL import Image

def onAppStart(app):
    app.setMaxShapeCount(3000)
    #https://cdn.textstudio.com/output/sample/normal/5/8/6/6/reveal-logo-73-6685.png
    app.revealImageC = Image.open('reveal.jpg')
    app.revealImageC = CMUImage(app.revealImageC)
    #https://ih1.redbubble.net/image.864988964.4796/st,small,845x845-pad,1000x1000,f8f8f8.u4.jpg
    app.extraLifeImageC = Image.open('extraLife.jpg')
    app.extraLifeImageC = CMUImage(app.extraLifeImageC)
    #https://previews.123rf.com/images/carmenbobo/carmenbobo1401/carmenbobo140100051/25103336-stamp-with-word-detect-inside-vector-illustration.jpg
    app.detectImageC = Image.open('detect.jpg')
    app.detectImageC = CMUImage(app.detectImageC)
    #Filtered using https://blackandwhite.imageonline.co/
    app.revealImageB = Image.open('revealB.jpg')
    app.revealImageB = CMUImage(app.revealImageB)
    app.extraLifeImageB = Image.open('extraLifeB.jpg')
    app.extraLifeImageB = CMUImage(app.extraLifeImageB)
    app.detectImageB = Image.open('detectB.jpg')
    app.detectImageB = CMUImage(app.detectImageB)
    app.extraLives = 0
    app.powerUps = []
    app.logoScreen = True
    app.menu = False
    app.difficulty = None
    app.color = 'gray'
    app.colorIndex = None
    app.colorMap = {1: 'green', 2: 'blue', 3: 'salmon'}
    app.rows, app.cols, app.mines = 0, 0, 0
    app.headerHeight = 50
    app.revealed = []
    app.flagged = []
    app.gameStarted = False
    app.gameOver = False
    app.stepsPerSecond = 1
    app.counter = 0
    app.mouseX = 0
    app.mouseY = 0
    #https://img.itch.zone/aW1nLzYyODI5MjIucG5n/original/%2BKYM32.png
    app.flagImage = Image.open('flag.jpg')
    app.flagImage = CMUImage(app.flagImage)
    #https://img.freepik.com/premium-vector/cannon-balls-cute-cartoon-black-bomb_634248-10.jpg
    app.bombImage = Image.open('bomb.jpg')
    app.bombImage = CMUImage(app.bombImage)
    #https://commons.wikimedia.org/wiki/File:Minesweeper_flag.svg
    app.menuImage = Image.open('menuScreen.jpg')
    app.menuImage = CMUImage(app.menuImage)
    #https://retro-dev.fandom.com/wiki/Minesweeper
    app.logoImage = Image.open('logo.jpg')
    app.logoImage = CMUImage(app.logoImage)
    app.tilesRevealed = 0
    app.mineLocations = set()
    app.minesToDetect = 2

#setsdifficult of game depending on user's choice
def setDifficulty(app):
    if app.difficulty == 'easy':
        app.rows, app.cols, app.mines = 8, 8, 10
        app.minesToDetect = 2
    elif app.difficulty == 'medium':
        app.rows, app.cols, app.mines = 12, 12, 20
        app.minesToDetect = 4
    elif app.difficulty == 'hard':
        app.rows, app.cols, app.mines = 16, 16, 40
        app.minesToDetect = 6
    
    app.board = createBoard(app, app.rows, app.cols, app.mines)
    app.menu = False
    app.flagged = []
    app.gameStarted = False
    initializePowerUps(app)

#actually creates the board
def createBoard(app, rows, cols, mines):
    board = []
    for _ in range(rows):
        row = [0] * cols
        board.append(row)

    placedMines = 0
    while placedMines < mines:
        mineRow = random.randint(0, rows-1)
        mineCol = random.randint(0, cols-1)

        if (mineRow, mineCol) not in app.mineLocations:
            app.mineLocations.add((mineRow, mineCol))
            board[mineRow][mineCol] = -1
            placedMines +=1

            for r in range(max(0,mineRow-1), min(rows, mineRow + 2)):
                for c in range(max(0, mineCol-1), min(cols, mineCol + 2)):
                    if board[r][c] != -1 and 0<=r<rows and 0<=c<cols:
                        board[r][c] +=1
    return board
    
#Inspiration from https://en.wikipedia.org/wiki/Flood_fill#Stack-based_recursive_implementation_(four-way)
#once the user clicks a tile that has neighboring 0s the function clears those tiles
def floodFill(app, row, col):
    stack = [(row, col)]

    while stack:
        r, c = stack.pop()

        if 0 <= r < app.rows and 0 <= c < app.cols and not app.revealed[r][c]:
            if app.board[r][c] == 0:
                app.revealed[r][c] = True

                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        stack.append((r + dr, c + dc))
            else:
                app.revealed[r][c] = True
     
#called when the game is over to show the user where all the mines were located
def revealAllMines(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == -1 and (row, col) not in app.flagged:
                app.revealed[row][col] = True

#checks to see if the user has won
def checkWinCondition(app):
    flaggedMines = 0
    correctlyFlagged = 0

    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == -1:
                if (row, col) in app.flagged:
                    flaggedMines += 1
                    if (row, col) in app.mineLocations:
                        correctlyFlagged += 1
            else:
                if (row, col) in app.flagged:
                    return False 

    return flaggedMines == app.mines and correctlyFlagged == app.mines

#user presses key to choose difficulty, theme color, and flag mines
def onKeyPress(app, key):
    if key == 'e':
        app.difficulty = 'easy'
    elif key == 'm':
        app.difficulty = 'medium'
    elif key == 'h':
        app.difficulty = 'hard'
    elif key == 'space':
        if app.logoScreen == False and app.menu == False and not app.gameOver:
            cellSize = min(app.width // (app.cols), (app.height-app.headerHeight) // app.rows)
            row = (app.mouseY-app.headerHeight)//cellSize        
            col = app.mouseX//cellSize
            if 0 <= row < app.rows and 0 <= col < app.cols:
                if app.revealed[row][col]:
                    return  
                if (row, col) in app.flagged:
                    app.flagged.remove((row, col))  
                elif len(app.flagged) < app.mines:
                    app.flagged.append((row, col)) 
            return 

    if app.menu and key.isdigit():
        if 1<=int(key)<=3:
            app.colorIndex = int(key)
    if app.colorIndex and app.difficulty and not app.gameOver:
        setDifficulty(app)
        cellSize = min(app.width // (app.cols), (app.height-app.headerHeight) // app.rows)
    app.revealed = [[False] * app.cols for _ in range(app.rows)]

#keeps track of the mouse position, used for flagging
def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

#used mostly for and clearing tiles and button pressing, such as play again, continue, and using the powerups
def onMousePress(app, mouseX, mouseY):
    if app.logoScreen:
        if app.width - 150 <= mouseX <= app.width + 50 and app.height - 50 <= mouseY <= app.height+10:
            app.logoScreen = False
            app.menu = True

    if app.logoScreen == False and app.menu == False and not app.gameOver:
        cellSize = min(app.width // (app.cols), (app.height-app.headerHeight) // app.rows)
        row = (mouseY-app.headerHeight)//cellSize        
        col = mouseX//cellSize
        
        if 0<=row<app.rows and 0<=col<app.cols:
            if (row, col) in app.flagged:
                return
            if (row, col) in app.mineLocations and (row, col) not in app.flagged:
                if app.extraLives > 0 and not app.revealed[row][col]:  
                    app.extraLives -= 1  
                    app.gameStarted = True 
                    app.revealed[row][col] = True 
                else:
                    app.gameOver = True
                    revealAllMines(app)
            else:
                if app.board[row][col] == -1:
                    app.gameOver = True
                    revealAllMines(app)
                else:
                    if not app.revealed[row][col]:
                        if app.board[row][col] == 0:
                            floodFill(app, row, col)
                        else:
                            app.revealed[row][col] = True
                        app.gameStarted = True
            if checkWinCondition(app):
                app.gameOver = True

        iconSize = 100 
        spacing = 150
        rightMargin = 50  
        gridWidth = app.cols * cellSize  
        powerUpIndex = 0
        
        for powerUp in app.powerUps:
            iconX = rightMargin + gridWidth + iconSize / 2
            iconY = 100 + powerUpIndex * spacing + iconSize / 2

            if (mouseX >= iconX - iconSize / 2
                and mouseX <= iconX + iconSize / 2
                and mouseY >= iconY - iconSize / 2
                and mouseY <= iconY + iconSize / 2
                and powerUp.available):
                if powerUp.name == 'Reveal':
                    useReveal(app)
                elif powerUp.name == 'Extra Life':
                    useExtraLife(app)
                elif powerUp.name == 'Detect':
                    useDetect(app)
                break 
            
            powerUpIndex += 1

    if app.gameOver:
        buttonX = app.width // 2
        buttonY = app.height // 2 + 50
        buttonWidth = 100
        buttonHeight = 30
        if buttonX -10 < mouseX < buttonX + buttonWidth+ 10 and buttonY-10 < mouseY < buttonY + buttonHeight+10:
            app.revealed = [[False] * app.cols for _ in range(app.rows)]
            app.flagged = []
            app.gameOver = False
            app.gameStarted = False
            app.tilesRevealed = 0
            app.mineLocations = set()
            app.difficulty = None
            app.counter = 0
            app.logoScreen = False
            app.colorIndex = None
            app.menu = True  

# counts how many tiles have been revealed, for extra life powerup
def countRevealedTiles(app):
    count = 0
    for row in app.revealed:
        count += row.count(True)  
    return count

#every second, it adds 1 to the timer, checks if the condition to activate the powerups have been met,
# checks if game is over
def onStep(app):
    if app.gameStarted and not app.gameOver:
        updatePowerUpAvailability(app)
        app.counter += 1
        app.tilesRevealed = countRevealedTiles(app)
    if not app.gameStarted:
        app.counter = 0
        app.tilesRevealed = 0 
    elif checkWinCondition(app):
        app.gameOver = True
    if app.gameOver: 
        revealAllMines(app)
    
#draws everything, including the game over messages
def redrawAll(app):
    if app.logoScreen == True:
        drawLogoScreen(app)
    elif app.menu == True:
        drawMenuScreen(app)
    else:
        drawHeader(app)
        drawBoard(app)
        drawPowerUps(app)
    
    if app.gameOver:
        if checkWinCondition(app):
            drawLabel("Victory!", app.width / 2, app.height / 2, fill='green', size=60, bold = True, align ='center')
        else:
            drawLabel("Game Over!", app.width / 2, app.height / 2, fill='red', size=60, bold = True, align ='center')
        buttonWidth = 100
        buttonHeight = 30
        buttonX = (app.width-buttonWidth) // 2
        buttonY = app.height // 2 + 50
       
        drawRect(buttonX, buttonY, buttonWidth, buttonHeight, fill='gray')
        drawLabel("Play Again", buttonX + buttonWidth // 2, buttonY + buttonHeight // 2, size=18)

def main():
    app.width = 400
    app.height = 400
    runApp()

main()