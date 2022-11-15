from cmu_112_graphics import *
import time
import objects
import players
import enemies
import levels
def appStarted(app): 
    app.enemyTanks = []
    app.enemyBullets = []
    app.playerBullets = []
    app.currentLayout = []
    app.levels = initLevels()
    app.currentLevel = 0
    app.missionLoading = False
    app.lives = 3
    app.wallSize = 50
    app.background = app.loadImage('images\\background.png')
    app.time0 = time.time()
def timerFired(app):
    if(app.currentLevel > 0 and not app.missionLoading):
        doCollisions()
        doMove()
        if(len(app.enemyTanks) == 0):
            completeLevel(app)
    if(time.time() - app.time0 > 2 and app.missionLoading):
        startLevel(app)

def keyPressed(app, event):
    pass

def keyReleased(app, event):
    pass

def mousePressed(app, event):
    pass

def mouseReleased(app, event):
    if(app.currentLevel == 0 and event.x > 350 and event.x < 750
     and event.y > 300 and event.y < 500):
        completeLevel(app)

def mouseMoved(app, event):
    pass

def sizeChanged(app):
    app.setSize(880,640)

def redrawAll(app, canvas):
    if app.missionLoading:
        drawMissionLoad(app,canvas)
    elif app.currentLevel == 0:
        drawHomeScreen(app,canvas)
    else:
        drawLevel(app,canvas)
        drawObjects(app,canvas)

def drawHomeScreen(app,canvas):
    canvas.create_rectangle(350,300,750,500,fill = 'grey')
    canvas.create_text(550,400,text = 'Start', font = 'Arial 40 bold')

def drawLevel(app,canvas):
    levelData = app.levels[app.currentLevel-1][2]
    canvas.create_image(500,400,image = ImageTk.PhotoImage(app.background))
    for (row,col) in levelData:
        drawWall(canvas,row-1,col-1)
    drawOutsideWalls(app,canvas)

def drawOutsideWalls(app,canvas):
    for i in range(22):
        drawWall(canvas,i,0)
        drawWall(canvas,i,15)
    for j in range(16):
        drawWall(canvas,0,j)
        drawWall(canvas,21,j)
def drawWall(canvas,row,col):
    cx,cy = cellToLocation((row,col))
    canvas.create_rectangle(cx-20,cy-20,cx+20,cy+20,fill = 'tan4')

def drawObjects(app,canvas):
    pass
def drawMissionLoad(app,canvas):
    pass

#level format is list of tuple (Player,EnemyList,WallTupleList)
def initLevels():
    gameLevels = []
    for i in range(levels.totalLevels):
        tempPlayer = levels.playerList[i]
        tempEnemies = levels.enemyList[i] 
        tempLayout = toTupleList(levels.layoutList[i])
        gameLevels.append((tempPlayer,tempEnemies,tempLayout))
    return gameLevels

def startLevel(app):
    app.player = app.levels[app.currentLevel-1][0]
    app.enemyTanks = app.levels[app.currentLevel-1][1]
    app.currentLayout = app.levels[app.currentLevel-1][2]
    app.missionLoading = False

def doCollisions():
    pass
def doMove():
    pass
def completeLevel(app):
    app.currentLevel += 1
    if(app.currentLevel > levels.totalLevels):
        winGame(app)
    app.missionLoading = True
    app.time0 = time.time()
    print(app.time0)

def winGame(app):
    pass

def toTupleList(level):
    tupleList = []
    for i in range(len(level)):
        for j in range(len(level[0])):
            if level[i][j] == 1:
                tupleList.append((i,j))
    return tupleList

def cellToLocation(cell):
    i,j = cell
    x = 20 + 40*i
    y = 20 + 40*j
    return (x,y)

def locationToCell(location):
    x,y = location
    i = (x-20)//22
    j = (y-20)//16
    return (i,j)

runApp(width=880, height=640)
