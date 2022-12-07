from cmu_112_graphics import *

def lost_redrawAll(app,canvas):
    drawGameLost(app,canvas)

def drawGameLost(app,canvas):
    canvas.create_text(app.width/2,app.height/2,text = 'You Lost!', font = 'Arial 40 bold')