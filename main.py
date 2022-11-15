from cmu_112_graphics import *
import time
import objects
import players
import enemies
def appStarted(app): 
    app.enemyTanks = []
    app.enemyBullets = []
    app.playerBullets = []
    app.currentLevel = 0
    app.levels = initLevels()
    app.currentLevel = 0
    app.missionLoading = False
    app.totalLevels = 2
    app.lives = 3
def timerFired(app):
    if(app.currentLevel > 0 and not app.missionLoading):
        doCollisions()
        doMove()
        if(len(app.enemyTanks) == 0):
            completeLevel()

def keyPressed(app, event):
    pass

def keyReleased(app, event):
    app.messages.append('keyReleased: ' + event.key)

def mousePressed(app, event):
    app.messages.append(f'mousePressed at {(event.x, event.y)}')

def mouseReleased(app, event):
    app.messages.append(f'mouseReleased at {(event.x, event.y)}')

def mouseMoved(app, event):
    app.messages.append(f'mouseMoved at {(event.x, event.y)}')

def mouseDragged(app, event):
    app.messages.append(f'mouseDragged at {(event.x, event.y)}')

def sizeChanged(app):
    app.messages.append(f'sizeChanged to {(app.width, app.height)}')

def redrawAll(app, canvas):
    if app.missionLoading:
        drawMissionLoad(app,canvas)
    elif app.currentLevel == 0:
        drawHomeScreen(app,canvas)
    else:
        drawLevel(app,canvas)
        drawObjects(app,canvas)

def drawHomeScreen(app,canvas):
    pass
def drawLevel(app,canvas):
    levelData = app.levels[app.currentLevel][2]

def drawObjects(app,canvas):
    pass
def drawMissionLoad():
    pass
#level format is list of tuple (Player,EnemyList,WallTupleList)
def initLevels():
    levels = []

    return levels

def startLevel(app):
    app.player = app.levels[app.currentLevel][0]
    app.enemyTanks
    pass

def doCollisions():
    pass
def doMove():
    pass
def completeLevel(app):
    app.currentLevel += 1
    if(app.currentLevel > app.totalLevels):
        winGame(app)
    app.missionLoading = True
    app.time0 = time.time()
def winGame(app):
    pass

runApp(width=1000, height=800)