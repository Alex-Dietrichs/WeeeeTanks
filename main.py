from cmu_112_graphics import *
import levels
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
    app.currentDestroyableWalls = set()
    app.currentTotalSet = set()
    app.currentMines = []
    app.currentExplosions = dict()
    app.levels = initLevels()
    app.currentLevel = 0
    app.missionLoading = False
    app.lives = 3
    app.wallSize = 50
    #image from https://www.textures-resource.com/fullview/12548/
    app.background = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\background.png'),1/1.8))
    app.wall = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\wall2.1.png'),1/3.75))
    app.hole = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\hole.png'),1/3.75))
    app.destroyableWall = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\destroyableWall.png'),1/3.75))

    #image from wii tanks game
    app.mineImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\mine.png'),1/4.5))
    app.activeMineImage = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\activeMine.png'),1/4.5))

    #self made images
    app.bulletPNG = app.scaleImage(app.loadImage('images\\bullet.png'),1/2.5)
    app.fastBulletPNG = app.scaleImage(app.loadImage('images\\fastBullet.png'),1/2.5)
    app.explosion = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\explosion.png'),1/4))
    app.mineExplosion = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\explosion.png'),1/2.5))
    app.bulletExplosion = ImageTk.PhotoImage(app.scaleImage(app.loadImage('images\\explosion.png'),1/8))
    app.time0 = time.time()
    app.mode = 'home'

    app.timerDelay = 25
    app.timeConstant = app.timerDelay/1000

    app.paused = False
    app.hitPause = False
    app.winPause = False
    app.dir = controls.controller()
    app.homePress = False
#Game
def game_timerFired(app):
    if not app.paused:
        app.time2 = time.time()
        doCollisions(app)
        doRicochet(app)
        doMove(app)
        doExplosions(app)
        app.player.timeSinceLastFire += app.timeConstant
        app.player.timeSinceLastMine += app.timeConstant
        if(len(app.enemyTanks) == 0):
            app.paused = True
            app.winPause = True
            app.time0 = time.time()
    if(app.hitPause and time.time() - app.time0 > 3):
        resetLevel(app)
    if(app.winPause and time.time() - app.time0 > 1):
        app.winPause = False
        app.paused = False
        completeLevel(app)
    
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
    key = event.key.lower()
    if(app.dir.up and key == 'w'):
        app.dir.up = False
    elif(app.dir.down and key == 's'):
        app.dir.down = False
    elif(app.dir.left and key == 'a'):
        app.dir.left = False
    elif(app.dir.right and key == 'd'):
        app.dir.right = False
    elif(key == 'p' and not app.hitPause and not app.winPause):
        app.paused = not app.paused
    elif(key == 'space' and not app.paused):
        tempMine = app.player.layMine(app)
        if(tempMine != None):
            tempMine.initImage(app)
            app.currentMines.append(tempMine)

def game_mouseReleased(app, event):
    if(app.player.timeSinceLastFire > app.player.fireDelay and not app.paused):
        tempBullet = app.player.fire(event.x-app.player.x,event.y-app.player.y)
        if(tempBullet != None):
            tempBullet.initImage(app)
            app.bullets.append(tempBullet)
            app.player.timeSinceLastFire = 0

def game_mouseMoved(app,event):
    theta = atan2(event.x-app.player.x,event.y-app.player.y)+pi
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
#level format is list of tuple (Player,EnemyList,WallTupleList,HoleTupleList,DestroyableWallTupleList)
def initLevels():
    gameLevels = []
    for i in range(levels.totalLevels):
        tempPlayer = copy.copy(levels.playerList[i])
        tempEnemies = copy.copy(levels.enemyList[i])
        tempLayout = copy.copy(toTupleList(levels.layoutList[i],1))
        tempHoles = copy.copy(toTupleList(levels.layoutList[i],2))
        tempDestroyable = copy.copy(toTupleList(levels.layoutList[i],3))
        gameLevels.append((tempPlayer,tempEnemies,tempLayout,tempHoles,tempDestroyable))
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
    app.currentDestroyableWalls = set(app.levels[app.currentLevel-1][4])
    app.currentTotalSet = set(app.currentLayout + app.currentHoles + list(app.currentDestroyableWalls))
    app.currentMines = []
    app.currentExplosions = dict()
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
    newBullets = set(app.bullets)
    for i in range(len(app.bullets)):
        bullet = app.bullets[i]
        for j in range(i+1,len(app.bullets)):
            if (bullet.checkCollision(app.bullets[j].getPos(),
            bullet.getSize())):
                if(bullet in newBullets):
                    bullet.destroyBullet()
                    newBullets.remove(bullet)
                if(app.bullets[j] in newBullets):
                    app.bullets[j].destroyBullet()
                    newBullets.remove(app.bullets[j])
                bullet.explode(app)
        for tank in app.enemyTanks:
            if (bullet.checkCollision(tank.getPos(),tank.getSize())):
                if(bullet in newBullets):
                    bullet.destroyBullet()
                    newBullets.remove(bullet)
                app.enemyTanks.remove(tank)
                tank.explode(app)
        for mine in app.currentMines:
            if(mine.active and bullet.checkCollision(mine.getPos(),mine.getSize())):
                if(bullet in newBullets):
                    bullet.destroyBullet()
                    newBullets.remove(bullet)
                mine.explode(app)
        if(bullet.checkCollision(app.player.getPos(),app.player.getSize())):
            if(bullet in newBullets):
                bullet.destroyBullet()
                newBullets.remove(bullet)
            hitTaken(app)
    app.bullets = list(newBullets)
    for mine in app.currentMines:
        if mine.active:
            for tank in app.enemyTanks:
                if (mine.checkCollision(tank.getPos(),tank.getSize())):
                    mine.explode(app)
            if(mine.checkCollision(app.player.getPos(),app.player.getSize())):
                mine.explode()
                hitTaken(app)

def doWallRicochet(app,bullet):
    cell = locationToCell(bullet.getPos())
    if(cell in app.currentLayoutSet or cell in app.currentDestroyableWalls):
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
                    bullet.explode(app)
                return None
            elif(x>wx+20 or x<wx-20):
                bullet.dx = -bullet.dx
                if(bullet.ricochet() and bullet in app.bullets):
                    app.bullets.remove(bullet)
                    bullet.explode(app)
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
                bullet.explode(app)
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
        tempMine = enemy.layMine(app)
        if(tempMine != None):
            tempMine.initImage(app)
            app.currentMines.append(tempMine)
            enemy.findPath(app)
    for mine in app.currentMines:
        if(not mine.active):
            mine.activateMine()
        else:
            mine.checkMineLife(app)

def doExplosions(app):
    newDict = copy.copy(app.currentExplosions)
    for key in newDict:
        exTime,image = app.currentExplosions[key]
        if(exTime >.25):
            app.currentExplosions.pop(key)
        else:
            app.currentExplosions[key] = (exTime + app.timeConstant,image)
runApp(width=960, height=720)