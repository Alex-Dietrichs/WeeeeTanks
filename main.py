from cmu_112_graphics import *
import time
import objects
import players
import enemies
import levels
def appStarted(app): 
    app.enemyTanks = []
    app.bullets = []
    app.currentLayout = []
    app.levels = initLevels()
    app.currentLevel = 0
    app.missionLoading = False
    app.lives = 3
    app.wallSize = 50
    app.background = app.scaleImage(app.loadImage('images\\background.png'),1/2)
    app.time0 = time.time()
    app.mode = 'home'
    app.timerDelay = 10
    app.timeConstant = app.timerDelay/1000
def game_timerFired(app):
    if(app.currentLevel > 0 and not app.missionLoading):
        doCollisions(app)
        doMove(app)
        if(len(app.enemyTanks) == 0):
            completeLevel(app)
def loading_timerFired(app):
    if(time.time() - app.time0 > .5):
        startLevel(app)

def keyPressed(app, event):
    pass

def keyReleased(app, event):
    pass

def mousePressed(app, event):
    pass

def home_mouseReleased(app, event):
    if(app.currentLevel == 0 and event.x > 240 and event.x < 640
     and event.y > 220 and event.y < 420):
        completeLevel(app)


def game_mouseReleased(app, event):
    temp = app.player.fire(event.x-app.player.x,event.y-app.player.y)
    if(temp != None):
        app.bullets.append(temp)
    print(app.bullets)

def mouseMoved(app, event):
    pass

def sizeChanged(app):
    app.setSize(880,640)

def loading_redrawAll(app, canvas):
    drawMissionLoad(app,canvas)
def home_redrawAll(app, canvas):
    drawHomeScreen(app,canvas)

def game_redrawAll(app, canvas):
    drawLevel(app,canvas)
    drawObjects(app,canvas)

def drawHomeScreen(app,canvas):
    canvas.create_rectangle(240,220,640,420,fill = 'grey')
    canvas.create_text(440,320,text = 'Start', font = 'Arial 40 bold')

def drawLevel(app,canvas):
    levelData = app.levels[app.currentLevel-1][2]
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.background))
    for (row,col) in levelData:
        drawWall(canvas,row+1,col+1)
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
    for tank in app.enemyTanks:
        tank.draw(canvas)
    for bullet in app.bullets:
        bullet.draw(canvas)
    app.player.draw(canvas)
def drawMissionLoad(app,canvas):
    canvas.create_text(app.width/2,app.height/3,text = f'Mission {app.currentLevel}', font = 'Arial 40 bold')
    canvas.create_text(app.width/2,app.height/2,
    text = f'Enemy Tanks: {len(app.levels[app.currentLevel-1][1])}', font = 'Arial 40 bold')
    cx,cy = app.width*7/16,app.height*3/4
    canvas.create_rectangle(cx-25,cy-25,cx+25,cy+25,fill = 'blue')
    canvas.create_text(app.width/2,app.height*3/4,text = f'    X {app.lives}', font = 'Arial 40 bold',
    fill = 'blue')

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
    print(app.enemyTanks)
    app.currentLayout = app.levels[app.currentLevel-1][2]
    app.mode = 'game'

def doCollisions(app):
    pass
def doMove(app):
    for bullet in app.bullets:
        bullet.move(bullet.getSpeed()*app.timeConstant)
def completeLevel(app):
    app.currentLevel += 1
    if(app.currentLevel > levels.totalLevels):
        winGame(app)
    app.mode = 'loading'
    app.time0 = time.time()

def winGame(app):
    pass

def toTupleList(level):
    tupleList = []
    for i in range(len(level)):
        for j in range(len(level[0])):
            if level[i][j] == 1:
                tupleList.append((j,i))
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
