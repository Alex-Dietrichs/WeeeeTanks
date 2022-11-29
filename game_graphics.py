from helperFunc import *
from cmu_112_graphics import *

def game_redrawAll(app, canvas):
    #countFrames(app)
    drawLevel(app,canvas)
    drawObjects(app,canvas)
    if(app.hitPause):
        drawMissionFailed(app,canvas)
    elif(app.paused):
        drawPauseScreen(app,canvas)
def drawLevel(app,canvas):
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.background))
    for (row,col) in app.currentLayout:
        drawWall(canvas,row,col)
    drawOutsideWalls(app,canvas)
def drawOutsideWalls(app,canvas):
    for i in range(26):
        drawWall(canvas,i-1,0-1)
        drawWall(canvas,i-1,15-1)
    for j in range(16):
        drawWall(canvas,0-1,j-1)
        drawWall(canvas,25-1,j-1)

def drawWall(canvas,row,col):
    cx,cy = cellToLocation((row,col))
    canvas.create_rectangle(cx-20,cy-20,cx+20,cy+20,fill = 'tan4')
def drawObjects(app,canvas):
    for tank in app.enemyTanks:
        tank.draw(canvas)
    for bullet in app.bullets:
        bullet.draw(canvas)
    if not app.hitPause:
        app.player.draw(canvas)

def drawMissionFailed(app,canvas):
    canvas.create_rectangle(0,app.height*5/8,1040,app.height*3/8,fill = 'white')
    canvas.create_text(app.width/2,app.height/2,text = 'Mission Failed', font = 'Arial 40 bold')

def drawPauseScreen(app,canvas):
    canvas.create_rectangle(0,app.height*5/8,1040,app.height*3/8,fill = 'white')
    canvas.create_text(app.width/2,app.height/2,text = 'Paused, press p to start', font = 'Arial 40 bold')