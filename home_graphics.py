from cmu_112_graphics import *

def home_redrawAll(app, canvas):
    drawHomeScreen(app,canvas)

def drawHomeScreen(app,canvas):
    if(not app.homePress):
        canvas.create_rectangle(280,260,680,460,fill = 'grey')
    else:
        canvas.create_rectangle(280,260,680,460, fill = 'grey24')
    canvas.create_text(app.width/2,app.height/2,text = 'Start', font = 'Arial 40 bold')

