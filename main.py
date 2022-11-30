from cmu_112_graphics import *
import time
import levels
import math
from helperFunc import *
import controls
from game_graphics import *
from loading_graphics import *
from home_graphics import *
from lost_graphics import *
from won_graphics import *
def appStarted(app): 
    app.enemyTanks = []
    app.bullets = []
    app.currentLayout = []
    app.currentLayoutSet = set()
    app.currentHoles = []
    app.currentTotalSet = set()
    app.levels = initLevels()
    app.currentLevel = 6
    app.missionLoading = False
    app.lives = 3
    app.wallSize = 50
    #image from https://www.textures-resource.com/fullview/12548/
    app.background = app.scaleImage(app.loadImage('images\\background.png'),1/1.8)
    app.wall = app.scaleImage(app.loadImage('images\\wall2.1.png'),1/3.75)
    app.hole = app.scaleImage(app.loadImage('images\\hole.png'),1/3.75)

    #self made images
    app.bulletPNG = app.scaleImage(app.loadImage('images\\bullet.png'),1/2.5)
    app.fastBulletPNG = app.scaleImage(app.loadImage('images\\fastBullet.png'),1/2.5)
    #app.xWall = app.loadImage('images\\wall2.1.png').resize((40*24,40))
    #app.yWall = app.loadImage('images\\wall2.1.png').resize((40,40*26))
    app.time0 = 0
    app.mode = 'home'

    app.timerDelay = 20
    app.timeConstant = app.timerDelay/1000

    app.paused = False
    app.hitPause = False
    app.dir = controls.controller()
    app.homePress = False
    app.timeSinceLastFire = 2
#Game
def game_timerFired(app):
    if not app.paused:
        doCollisions(app)
        doRicochet(app)
        doMove(app)
        app.timeSinceLastFire += app.timeConstant
        if(len(app.enemyTanks) == 0):
            completeLevel(app)
    if(app.hitPause and time.time() - app.time0 > 3):
        resetLevel(app)

def game_keyPressed(app, event):
    key = event.key
    if(not app.dir.up and key == 'w'):
        app.dir.up = True
    elif(not app.dir.down and key == 's'):
        app.dir.down = True
    elif(not app.dir.left and key == 'a'):
        app.dir.left = True
    elif(not app.dir.right and key == 'd'):
        app.dir.right = True

def game_keyReleased(app, event):
    key = event.key
    if(app.dir.up and key == 'w'):
        app.dir.up = False
    elif(app.dir.down and key == 's'):
        app.dir.down = False
    elif(app.dir.left and key == 'a'):
        app.dir.left = False
    elif(app.dir.right and key == 'd'):
        app.dir.right = False
    elif(key.lower() == 'p' and not app.hitPause):
        app.paused = not app.paused

def game_mouseReleased(app, event):
    if(app.timeSinceLastFire > .05):
        tempBullet = app.player.fire(event.x-app.player.x,event.y-app.player.y)
        if(tempBullet != None):
            tempBullet.initImage(app)
            app.bullets.append(tempBullet)
            app.timeSinceLastFire = 0

def game_mouseMoved(app,event):
    theta = math.atan2(event.x-app.player.x,event.y-app.player.y)+math.pi
    app.player.rotateTurretImage(theta)

#Home
def home_mouseReleased(app, event):
    if(event.x > 280 and event.x < 680
     and event.y > 260 and event.y < 460 and app.homePress):
        completeLevel(app)
    else:
        app.homePress = False
def home_mousePressed(app, event):
    if(event.x > 280 and event.x < 680
     and event.y > 260 and event.y < 460):
        app.homePress = True

#Loading
def loading_timerFired(app):
    if(time.time() - app.time0 > 1):
        startLevel(app)

#Won
def won_timerFired(app):
    if(time.time() - app.time0 > 5):
        app.mode = 'home'
        appStarted(app)

#Lost
def lost_timerFired(app):
    if(time.time() - app.time0 > 5):
        app.mode = 'home'
        appStarted(app)

#Initializing
#level format is list of tuple (Player,EnemyList,WallTupleList,HoleTupleList)
def initLevels():
    gameLevels = []
    for i in range(levels.totalLevels):
        tempPlayer = copy.copy(levels.playerList[i])
        tempEnemies = copy.copy(levels.enemyList[i])
        tempLayout = copy.copy(toTupleList(levels.layoutList[i],1))
        tempHoles = copy.copy(toTupleList(levels.layoutList[i],2))
        gameLevels.append((tempPlayer,tempEnemies,tempLayout,tempHoles))
    return gameLevels

def startLevel(app):
    app.player = app.levels[app.currentLevel-1][0]
    app.player.setPos(levels.playerList[app.currentLevel-1].getPos())
    app.player.initImage(app)
    app.enemyTanks = app.levels[app.currentLevel-1][1]
    for tank in app.enemyTanks:
        tank.x = tank.startx
        tank.y = tank.starty
        tank.initImage(app)
    app.currentLayout = app.levels[app.currentLevel-1][2]
    app.currentLayoutSet = set(app.currentLayout)
    app.currentHoles = app.levels[app.currentLevel-1][3]
    app.currentTotalSet = set(app.currentLayout + app.currentHoles)
    app.bullets = []
    app.mode = 'game'
    app.dir = controls.controller()

def resetLevel(app):
    app.lives -= 1
    app.hitPause = False
    app.paused = False
    app.time0 = time.time()
    if(app.lives == 0):
        app.currentLevel = 0
        app.mode = 'lost'
    else:
        app.mode = 'loading'

def completeLevel(app):
    app.currentLevel += 1
    if(app.currentLevel > levels.totalLevels):
        wonGame(app)
    else:
        app.mode = 'loading'
    app.time0 = time.time()       

#Do functions
def doCollisions(app):
    newBullets = copy.copy(app.bullets)
    for i in range(len(app.bullets)):
        for j in range(i+1,len(app.bullets)):
            if (app.bullets[i].checkCollision(app.bullets[j].getPos(),
            app.bullets[j].getSize())):
                if(app.bullets[i] in newBullets):
                    app.bullets[i].destroyBullet()
                    newBullets.remove(app.bullets[i])
                if(app.bullets[j] in newBullets):
                    app.bullets[j].destroyBullet()
                    newBullets.remove(app.bullets[j])
        for tank in app.enemyTanks:
            if (app.bullets[i].checkCollision(tank.getPos(),tank.getSize())):
                if(app.bullets[i] in newBullets):
                    app.bullets[i].destroyBullet()
                    newBullets.remove(app.bullets[i])
                app.enemyTanks.remove(tank)
        if(app.bullets[i].checkCollision(app.player.getPos(),app.player.getSize())):
            if(app.bullets[i] in newBullets):
                app.bullets[i].destroyBullet()
                newBullets.remove(app.bullets[i])
            hitTaken(app)
    app.bullets = copy.copy(newBullets)

def doWallRicochet(app,bullet):
    cell = locationToCell(bullet.getPos())
    if(cell in app.currentLayoutSet):
        wx,wy = cellToLocation(cell)
        if(bullet.checkCollision((wx,wy),(40,40))):
            x,y = bullet.getPos()
            dx,dy = bullet.getVelocity()
            dx *= (bullet.getSpeed() * app.timeConstant)
            dy *= (bullet.getSpeed() * app.timeConstant)
            while True:
                x-= dx/5
                y-= dy/5
                if((y>wy+20 or y<wy-20) or (x>wx+20 or x<wx-20)):
                    break
            if(y>wy+20 or y<wy-20):
                bullet.dy = -bullet.dy
                if(bullet.ricochet() and bullet in app.bullets):
                    app.bullets.remove(bullet)
                return None
            elif(x>wx+20 or x<wx-20):
                bullet.dx = -bullet.dx
                if(bullet.ricochet() and bullet in app.bullets):
                    app.bullets.remove(bullet)
                return None

def doRicochet(app):
    for bullet in app.bullets:
        x,y = bullet.getPos()
        if x < 0+45 or x>app.width-45:
            bullet.dx = -bullet.dx
            if(bullet.ricochet()):
                app.bullets.remove(bullet)
        elif y < 0+45 or y > app.height-45:
            bullet.dy = -bullet.dy
            if(bullet.ricochet()):
                app.bullets.remove(bullet)
        else:
            doWallRicochet(app,bullet)

def doMove(app):
    for bullet in app.bullets:
        bullet.move(bullet.getSpeed()*app.timeConstant)
    calcPlayerMove(app)
    if(app.player.dx != 0 or app.player.dy != 0):
        app.player.rotateImage()
    app.player.move(app.player.getSpeed()*app.timeConstant, app.currentTotalSet)
    for enemy in app.enemyTanks:
        enemy.followPath(app)
        if(enemy.dx != 0 or enemy.dy != 0):
            enemy.rotateImage()
        tempBullet = enemy.moveAim(app)
        if(tempBullet != None):
            tempBullet.initImage(app)
            app.bullets.append(tempBullet)

runApp(width=960, height=720)