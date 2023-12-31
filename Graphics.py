#Graphics file handles all the drawing functions and all the graphics of the program

from cmu_graphics import *
import random
from PIL import Image

#draws the first screen the user sees
def drawLogoScreen(app):
    drawImage(app.logoImage, 0, 0, width=app.width, height=app.height)
    drawLabel("Continue", app.width - 50, app.height - 20, size=24, fill='black')

#draws the menu screen where user can make choices
def drawMenuScreen(app):
    drawImage(app.menuImage, 0, 0, width=app.width, height=app.height)
    drawLabel("Select Difficulty", app.width/2, app.height/3, size = 35, bold  = True, fill = 'white')
    drawLabel("Press 'E' for Easy, 'M' for Medium, 'H' for Hard", app.width/2, app.height*2/3, size = 31, fill = 'white')
    if app.difficulty != None:
        drawLabel(f'Selected Difficulty: {app.difficulty.upper()}', app.width/2, app.height/2, size = 33, fill = 'white')
    drawLabel("Press a Number (1-3) to Choose Theme Color", app.width/2, app.height-100, size = 29, fill = 'white')
    if app.colorIndex != None:
        drawLabel(f'Selected Color: {app.colorMap[app.colorIndex]}', app.width/2, app.height-60, size = 29, fill = 'white')

#draws the minecounter and timer
def drawHeader(app):
    minesLeft = app.mines-len(app.flagged)
    drawRect(0, 0, app.width,app.headerHeight, fill = 'lightgray')
    drawLabel(f'Mines: {minesLeft}', app.width//2-100, app.headerHeight//2, size = 16)
    drawLabel(f'Timer: {app.counter}', app.width -200, app.headerHeight//2, size = 16)

#draws the board and tiles depending on the user's choices
def drawBoard(app):
    cellSize = min(app.width // (app.cols), (app.height-app.headerHeight) // app.rows)
    colors = {
        1: 'steelblue',
        2: 'green',
        3: 'red',
        4: 'navy',
        5: 'maroon',
        6: 'teal',
        7: 'purple',
        8: 'black'
    }

    for row in range(app.rows):
        for col in range(app.cols):
            x0 = col*cellSize
            x1 = x0 + cellSize
            y0 = row*cellSize + app.headerHeight
            y1 = y0 + cellSize
            originalTileColor = app.colorMap[app.colorIndex]
            tileColor = originalTileColor

            if col != app.cols - 1:
                drawLine(x0 + cellSize, y0, x0 + cellSize, y0 + cellSize, fill='white')
            if row != app.rows - 1:
                drawLine(x0, y0 + cellSize, x0 + cellSize, y0 + cellSize, fill='white')
            
            revealed = app.revealed[row][col]
            if not revealed:
                drawRect(x0, y0, x1, y1, fill = app.colorMap[app.colorIndex])
                drawLine(x0, y0, x1, y0, fill='white')  
                drawLine(x0, y0, x0, y1, fill='white')  
                drawLine(x0, y1, x1, y1, fill='white')      
                drawLine(x1, y0, x1, y1, fill='white')   
            else:
                if app.board[row][col] != 0 or app.board[row][col] == -2:
                    tileColor = 'light' + originalTileColor
                if app.revealed[row][col] and app.gameStarted and not app.gameOver:
                    if (row, col) == (app.mouseY // cellSize - app.headerHeight // cellSize, app.mouseX // cellSize):
                        tileColor = 'dark' + originalTileColor
                drawRect(x0, y0, x1, y1, fill=tileColor)
                drawLine(x0, y0, x1, y0, fill='white')  
                drawLine(x0, y0, x0, y1, fill='white')  
                drawLine(x0, y1, x1, y1, fill='white')      
                drawLine(x1, y0, x1, y1, fill='white')   
            
            if revealed:
                if app.board[row][col] == 0:
                    drawRect(x0, y0, x1, y1, fill='light' + app.colorMap[app.colorIndex])
                    drawLine(x0, y0, x1, y0, fill='white')
                    drawLine(x0, y0, x0, y1, fill='white')
                    drawLine(x0, y1, x1, y1, fill='white')
                    drawLine(x1, y0, x1, y1, fill='white')
                elif app.board[row][col] != -1:
                    num = app.board[row][col]
                    if num > 0:
                        numColor = colors[num] if num in colors else 'black'
                        drawLabel(str(num), x0 + cellSize / 2, y0 + cellSize / 2, size=20, bold=True, fill=numColor)
                else:
                    drawImage(app.bombImage, x0, y0, width = cellSize, height = cellSize)
            if (row,col) in app.flagged:
                drawImage(app.flagImage, x0, y0, width=cellSize, height=cellSize)

    for row in range(app.rows):
        x0 = app.cols * cellSize
        y0 = app.headerHeight
        drawLine(x0, y0, x0, app.height,fill = 'white')
        drawLine(x0, y1, app.width, y1, fill='white')
    for col in range(app.cols):
        x0 = col * cellSize
        y0 = app.headerHeight
        drawLine(x0, y0, x0, app.height, fill ='white')
        drawLine(x0 + cellSize, y0, x0 + cellSize, y1, fill='white')
    drawRect(app.cols * cellSize, app.headerHeight, app.width - (app.cols * cellSize), app.height - app.headerHeight, fill='darkSlateGray')