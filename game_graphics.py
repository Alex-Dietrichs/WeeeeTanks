from helperFunc import *
from cmu_112_graphics import *

def game_redrawAll(app, canvas):
    #time0 = time.time()
    drawLevel(app,canvas)
    drawObjects(app,canvas)
    if(app.hitPause):
        drawMissionFailed(app,canvas)
    elif(app.paused):
        drawPauseScreen(app,canvas)
    #print(f'Total Graphics Draw Time: {time.time()-time0}')
def drawLevel(app,canvas):
    canvas.create_image(app.width/2,app.height/2,image = app.background)
    #canvas.create_rectangle(0,0,app.width,app.height,fill = '#aa9459',width=0)
    for (row,col) in app.currentLayout:
        drawWall(canvas,app,row,col)
    for (row,col) in app.currentHoles:
        drawHole(canvas,app,row,col)
    drawOutsideWalls(app,canvas)
def drawOutsideWalls(app,canvas):
        #canvas.create_image(app.width/2,20, image=ImageTk.PhotoImage(app.xWall))
        #canvas.create_image(20,app.height/2, image=ImageTk.PhotoImage(app.yWall))
        #canvas.create_image(app.width-20,app.height/2, image=ImageTk.PhotoImage(app.yWall))
        canvas.create_rectangle(0,0,app.width,40,fill = '#8a6b33',width = 0)
        canvas.create_rectangle(0,0,40,app.height,fill = '#8a6b33',width = 0)
        canvas.create_rectangle(0,app.height,app.width,app.height-40,fill = '#8a6b33',width = 0)
        canvas.create_rectangle(app.width,0,app.width-40,app.height,fill = '#8a6b33',width = 0)
def drawWall(canvas,app,row,col):
    cx,cy = cellToLocation((row,col))
    canvas.create_image(cx,cy,image = app.wall)
def drawHole(canvas,app,row,col):
    cx,cy = cellToLocation((row,col))
    canvas.create_image(cx,cy,image=app.hole)
def drawObjects(app,canvas):
    for tank in app.enemyTanks:
        tank.draw(canvas)
    for bullet in app.bullets:
        bullet.draw(canvas)
    if not app.hitPause:
        app.player.draw(canvas)

def drawMissionFailed(app,canvas):
    canvas.create_rectangle(0,app.height*5/8,app.width,app.height*3/8,fill = 'white')
    canvas.create_text(app.width/2,app.height/2,text = 'Mission Failed', font = 'Arial 40 bold')

def drawPauseScreen(app,canvas):
    canvas.create_rectangle(0,app.height*5/8,app.width,app.height*3/8,fill = 'white')
    canvas.create_text(app.width/2,app.height/2,text = 'Paused, press p to start', font = 'Arial 40 bold')