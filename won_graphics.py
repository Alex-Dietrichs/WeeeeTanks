from cmu_112_graphics import *


def won_redrawAll(app,canvas):
    drawGameWon(app,canvas)

def drawGameWon(app,canvas):
    canvas.create_text(app.width/2,app.height/2,text = 'You Beat the Game!', font = 'Arial 40 bold')
