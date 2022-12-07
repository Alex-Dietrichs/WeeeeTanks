from cmu_112_graphics import *

def loading_redrawAll(app, canvas):
    drawMissionLoad(app,canvas)

def drawMissionLoad(app,canvas):
    canvas.create_text(app.width/2,app.height/3,text = f'Mission {app.currentLevel}', font = 'Arial 40 bold')
    canvas.create_text(app.width/2,app.height/2,
    text = f'Enemy Tanks: {len(app.levels[app.currentLevel-1][1])}', font = 'Arial 40 bold')
    cx,cy = app.width*7/16,app.height*3/4
    canvas.create_rectangle(cx-25,cy-25,cx+25,cy+25,fill = 'blue')
    canvas.create_text(app.width/2,app.height*3/4,text = f'    X {app.lives}', font = 'Arial 40 bold',
    fill = 'blue')