from cmu_112_graphics import *

def home_redrawAll(app, canvas):
    drawHomeScreen(app,canvas)

def drawHomeScreen(app,canvas):
    canvas.create_rectangle(320,220,720,420,fill = 'grey')
    canvas.create_text(app.width/2,app.height/2,text = 'Start', font = 'Arial 40 bold')

