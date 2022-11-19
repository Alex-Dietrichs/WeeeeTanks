from cmu_112_graphics import *
import time
import levels
import math

def appStarted(app): 
    app.enemyTanks = []
    app.bullets = []
    app.currentLayout = []
    app.levels = initLevels()
    app.currentLevel = 0
    app.missionLoading = False
    app.lives = 3
    app.wallSize = 50
    #image from https://www.textures-resource.com/fullview/12548/
    app.background = app.scaleImage(app.loadImage('images\\background.png'),1/2)
    app.time0 = time.time()
    app.mode = 'home'
    app.timerDelay = 25
    app.timeConstant = app.timerDelay/1000
    app.paused = False
    app.hitPause = False
    app.time2 = 0
    app.frames = 0

def game_timerFired(app):
    if not app.paused:
        doCollisions(app)
        doRicochet(app)
        doMove(app)
        if(len(app.enemyTanks) == 0):
            completeLevel(app)
    if(app.hitPause and time.time() - app.time0 > 3):
        resetLevel(app)

def loading_timerFired(app):
    if(time.time() - app.time0 > 2):
        startLevel(app)

def won_timerFired(app):
    if(time.time() - app.time0 > 5):
        app.mode = 'home'
        appStarted(app)

def lost_timerFired(app):
    if(time.time() - app.time0 > 5):
        app.mode = 'home'
        appStarted(app)

def game_keyPressed(app, event):
    if(event.key == 'w'):
        app.player.dy -= 1
    if(event.key == 's'):
        app.player.dy += 1
    if(event.key == 'a'):
        app.player.dx -=1
    if(event.key == 'd'):
        app.player.dx +=1
    app.player.dy = limit(app.player.dy,-1,1)
    app.player.dx = limit(app.player.dx,-1,1)

def game_keyReleased(app, event):
    if(event.key.lower() == 'w'):
        app.player.dy +=1
    if(event.key.lower() == 's'):
        app.player.dy -=1
    if(event.key.lower() == 'a'):
        app.player.dx +=1
    if(event.key.lower() == 'd'):
        app.player.dx -=1
    app.player.dy = limit(app.player.dy,-1,1)
    app.player.dx = limit(app.player.dx,-1,1)
    if(event.key.lower() == 'p' and not app.hitPause):
        app.paused = not app.paused

def limit(n, minn,maxn):
    return min(max(n,minn),maxn)

def home_mouseReleased(app, event):
    if(event.x > 240 and event.x < 640
     and event.y > 220 and event.y < 420):
        completeLevel(app)

def game_mouseReleased(app, event):
    temp = app.player.fire(event.x-app.player.x,event.y-app.player.y)
    if(temp != None):
        app.bullets.append(temp)


def loading_redrawAll(app, canvas):
    drawMissionLoad(app,canvas)

def home_redrawAll(app, canvas):
    drawHomeScreen(app,canvas)

def game_redrawAll(app, canvas):
    #countFrames(app)
    drawLevel(app,canvas)
    drawObjects(app,canvas)
    if(app.hitPause):
        drawMissionFailed(app,canvas)
    elif(app.paused):
        drawPauseScreen(app,canvas)

def countFrames(app):
    app.frames += 1
    if(time.time() - app.time2 >= 1):
        print(f'{app.frames} per second')
        app.time2 = time.time()
        app.frames = 0

def won_redrawAll(app,canvas):
    drawGameWon(app,canvas)

def lost_redrawAll(app,canvas):
    drawGameLost(app,canvas)

def drawHomeScreen(app,canvas):
    canvas.create_rectangle(240,220,640,420,fill = 'grey')
    canvas.create_text(440,320,text = 'Start', font = 'Arial 40 bold')

def drawGameWon(app,canvas):
    canvas.create_text(440,320,text = 'You Beat the Game!', font = 'Arial 40 bold')

def drawGameLost(app,canvas):
    canvas.create_text(440,320,text = 'You Lost!', font = 'Arial 40 bold')

def drawLevel(app,canvas):
    canvas.create_image(app.width/2,app.height/2,image = ImageTk.PhotoImage(app.background))
    for (row,col) in app.currentLayout:
        drawWall(canvas,row,col)
    drawOutsideWalls(app,canvas)

def drawOutsideWalls(app,canvas):
    for i in range(22):
        drawWall(canvas,i-1,0-1)
        drawWall(canvas,i-1,15-1)
    for j in range(16):
        drawWall(canvas,0-1,j-1)
        drawWall(canvas,21-1,j-1)

def drawWall(canvas,row,col):
    cx,cy = cellToLocation((row,col))
    canvas.create_rectangle(cx-20,cy-20,cx+20,cy+20,fill = 'tan4')

def drawObjects(app,canvas):
    for tank in app.enemyTanks:
        tank.draw(canvas)
    for bullet in app.bullets:
        bullet.draw(canvas)
    if not app.hitPause:
        app.player.draw(canvas)

def drawMissionLoad(app,canvas):
    canvas.create_text(app.width/2,app.height/3,text = f'Mission {app.currentLevel}', font = 'Arial 40 bold')
    canvas.create_text(app.width/2,app.height/2,
    text = f'Enemy Tanks: {len(app.levels[app.currentLevel-1][1])}', font = 'Arial 40 bold')
    cx,cy = app.width*7/16,app.height*3/4
    canvas.create_rectangle(cx-25,cy-25,cx+25,cy+25,fill = 'blue')
    canvas.create_text(app.width/2,app.height*3/4,text = f'    X {app.lives}', font = 'Arial 40 bold',
    fill = 'blue')

def drawMissionFailed(app,canvas):
    canvas.create_rectangle(0,app.height*5/8,880,app.height*3/8,fill = 'white')
    canvas.create_text(app.width/2,app.height/2,text = 'Mission Failed', font = 'Arial 40 bold')

def drawPauseScreen(app,canvas):
    canvas.create_rectangle(0,app.height*5/8,880,app.height*3/8,fill = 'white')
    canvas.create_text(app.width/2,app.height/2,text = 'Paused, press p to start', font = 'Arial 40 bold')

#level format is list of tuple (Player,EnemyList,WallTupleList)
def initLevels():
    gameLevels = []
    for i in range(levels.totalLevels):
        tempPlayer = copy.copy(levels.playerList[i])
        tempEnemies = copy.copy(levels.enemyList[i])
        tempLayout = copy.copy(toTupleList(levels.layoutList[i]))
        gameLevels.append((tempPlayer,tempEnemies,tempLayout))
    return gameLevels

def startLevel(app):
    app.player = app.levels[app.currentLevel-1][0]
    app.enemyTanks = app.levels[app.currentLevel-1][1]
    for tank in app.enemyTanks:
        tank.x = tank.startx
        tank.y - tank.starty
    app.currentLayout = app.levels[app.currentLevel-1][2]
    app.bullets = []
    app.mode = 'game'

def doCollisions(app):
    newBullets = copy.copy(app.bullets)
    for i in range(len(app.bullets)):
        for j in range(i+1,len(app.bullets)):
            if (app.bullets[i].checkCollision(app.bullets[j].getPos(),
            app.bullets[j].getSize())):
                app.bullets[i].destroyBullet()
                app.bullets[j].destroyBullet()
                if(app.bullets[i] in newBullets):
                    newBullets.remove(app.bullets[i])
                if(app.bullets[j] in newBullets):
                    newBullets.remove(app.bullets[j])
        for tank in app.enemyTanks:
            if (app.bullets[i].checkCollision(tank.getPos(),tank.getSize())):
                app.bullets[i].destroyBullet()
                if(app.bullets[i] in newBullets):
                    newBullets.remove(app.bullets[i])
                app.enemyTanks.remove(tank)
        if(app.bullets[i].checkCollision(app.player.getPos(),app.player.getSize())):
            if(app.bullets[i] in newBullets):
                newBullets.remove(app.bullets[i])
            hitTaken(app)
    app.bullets = copy.copy(newBullets)

def hitTaken(app):
    app.paused = True
    app.hitPause = True
    app.time0 = time.time()

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
        
def doWallRicochet(app,bullet):
    for wallCell in app.currentLayout:
        i,j = wallCell
        wx,wy = cellToLocation((i,j))
        if(bullet.checkCollision((wx,wy),(40,40))):
            x,y = bullet.getPos()
            dx,dy = bullet.getVelocity()
            dx *= (bullet.getSpeed() * app.timeConstant)
            dy *= (bullet.getSpeed() * app.timeConstant)
            x-=dx
            y-= dy
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
        if x < 0+42.5 or x>app.width-42.5:
            bullet.dx = -bullet.dx
            if(bullet.ricochet()):
                app.bullets.remove(bullet)
        elif y < 0+42.5 or y > app.height-42.5:
            bullet.dy = -bullet.dy
            if(bullet.ricochet()):
                app.bullets.remove(bullet)
        else:
            doWallRicochet(app,bullet)

def doMove(app):
    for bullet in app.bullets:
        bullet.move(bullet.getSpeed()*app.timeConstant)
    app.player.move(app.player.getSpeed()*app.timeConstant, app.currentLayout)
    for enemy in app.enemyTanks:
        enemy.followPath(app,app.currentLayout)
        temp = enemy.moveAim(app)
        if(temp != None):
            app.bullets.append(temp)

def completeLevel(app):
    app.currentLevel += 1
    if(app.currentLevel > levels.totalLevels):
        wonGame(app)
    else:
        app.mode = 'loading'
    app.time0 = time.time()    

def wonGame(app):
    app.mode = 'won'
    app.currentLevel = 0

def toTupleList(level):
    tupleList = []
    for i in range(len(level)):
        for j in range(len(level[0])):
            if level[i][j] == 1:
                tupleList.append((j,i))
    return tupleList

def cellToLocation(cell):
    i,j = cell
    x = 20+40*(i+1)
    y = 20+40*(j+1)
    return (x,y)

def locationToCell(location):
    x,y = location
    i = (x-20)//22
    j = (y-20)//16
    return (i-1,j-1)

runApp(width=880, height=640)