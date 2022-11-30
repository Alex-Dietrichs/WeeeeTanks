import math
import time
def cellToLocation(cell):
    i,j = cell
    x = 20+40*(i+1)
    y = 20+40*(j+1)
    return (x,y)

def locationToCell(location):
    x,y = location
    i = round((x-20)/40)
    j = round((y-20)/40)
    return (i-1,j-1)
    
def toTupleList(level,num):
    tupleList = []
    for i in range(len(level)):
        for j in range(len(level[0])):
            if level[i][j] == num:
                tupleList.append((j,i))
    return tupleList


def hitTaken(app):
    app.paused = True
    app.hitPause = True
    app.time0 = time.time()
    for bullet in app.bullets:
        bullet.destroyBullet()

def calcPlayerMove(app):
    dx,dy = 0,0
    if app.dir.up and not app.dir.down:
        dy = -1
    elif app.dir.down and not app.dir.up:
        dy = 1
    else:
        dy = 0

    if app.dir.left and not app.dir.right:
        dx = -1
    elif app.dir.right and not app.dir.left:
        dx = 1
    else:
        dx = 0

    if dx != 0 and dy != 0:
        mag = math.sqrt(dx**2 + dy**2)
        app.player.dx = dx/mag
        app.player.dy = dy/mag
    else:
        app.player.dx = dx
        app.player.dy = dy

def wonGame(app):
    app.mode = 'won'
    app.currentLevel = 0