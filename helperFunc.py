from math import sqrt,atan2,pi
import time
import platform
def cellToLocation(cell):
    i,j = cell
    x = 20+40*(i+1)
    y = 20+40*(j+1)
    return (x,y)

def locationToCell(location):
    x,y = location
    i = int((x-20)/40 +.499)
    j = int((y-20)/40 +.499)
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
    app.player.explode(app)
    for bullet in app.bullets:
        bullet.destroyBullet()
    for mine in app.currentMines:
        mine.destroyMine(app)

def logTimes(timeStart, timeEnd, exportFile):
    with open(exportFile,"a") as f:
        f.write("Start of timer fire " + str(timeStart) + "\n")
        f.write("Emd of timer fire " + str(timeEnd) + "\n")
        f.write("Difference between two:" + str(timeEnd - timeStart) + "\n")

def calcPlayerMove(app):
    direc = app.dir
    dx,dy = 0,0
    if direc.up and not direc.down:
        dy = -1
    elif direc.down and not direc.up:
        dy = 1
    else:
        dy = 0

    if direc.left and not direc.right:
        dx = -1
    elif direc.right and not direc.left:
        dx = 1
    else:
        dx = 0

    player = app.player
    if dx != 0 and dy != 0:
        mag = sqrt(dx**2 + dy**2)
        player.dx = dx/mag
        player.dy = dy/mag
    else:
        player.dx = dx
        player.dy = dy

def wonGame(app):
    app.mode = 'won'
    app.currentLevel = 0

def destroyWall(app, wallPos):
    if wallPos in app.currentDestroyableWalls:
        app.currentDestroyableWalls.remove(wallPos)
        app.currentTotalSet.remove(wallPos)

def canSeeSpace(app,pos,lookPos):
    iCheck,jCheck = locationToCell(pos)
    iFinal,jFinal = locationToCell(lookPos)
    di = .01 if (iFinal-iCheck) == 0 else (iFinal-iCheck)
    dj = .01 if (jFinal-jCheck) == 0 else (jFinal-jCheck)
    tankPos = set()
    for tank in app.enemyTanks:
        tankPos.add(locationToCell(tank.getPos()))

    while(int(iCheck+.0001) != iFinal or int(jCheck+.0001) != jFinal):
        if di>0: relDI = abs((int(iCheck + 1) - iCheck)/di)
        else: relDI = abs((int(iCheck-.001) - iCheck)/di)
        if dj > 0: relDJ = abs((int(jCheck + 1) - jCheck)/dj)
        else: relDJ = abs((int(jCheck-.001) - jCheck)/dj)
        relMult = min(relDI,relDJ)
        iCheck += relMult * di
        jCheck += relMult * dj
        checkT = (int(iCheck+.0001),int(jCheck+.0001))
        if(checkT in app.currentLayoutSet or checkT in tankPos 
        or checkT in app.currentDestroyableWalls):
            return False
    return True

def canSeeSpaceWithRich(app,pos,lookPos):
    viableSpots = getViableEdges(app,pos,lookPos)
    for wallPos in viableSpots:
        if (canSeeSpace(app,pos,wallPos) and canSeeSpace(app,wallPos,lookPos)):
            return locationToCell(wallPos)
    return None


#Way too slow
def canSeeSpaceWith2Rich(app,pos,lookPos):
    time0 = time.time()
    maybe = canSeeSpaceWithRich(app,pos,lookPos)
    if maybe != None:
        return maybe
    visEdge = getViableEdges(app,pos)
    for cell in visEdge:
        cellPos = cellToLocation(cell)
        visEdge2 = getViableEdges(app,cellToLocation(cell))
        for cell2 in visEdge2:
            cellPos2 = cellToLocation(cell2)
            if (angleCheck(app,pos,cellPos,cellPos2) and angleCheck(app,cellPos,cellPos2,lookPos) 
            and canSeeSpace(app,cellPos2,lookPos)):
                return cell
    print(time.time() - time0)
    return None

def getViableEdges(app,pos,lookPos):
    viableSpots = []
    x1,y1 = pos
    x2,y2 = lookPos
    #bottom wall
    h = app.height-45
    Xn = (h-y1)*(x2-x1)/(2*h-y2-y1)
    viableSpots.append((x1+Xn,h))
    #top wall
    h = 45
    Xn = (h-y1)*(x2-x1)/(2*h-y2-y1)
    viableSpots.append((x1+Xn,h))
    #left wall
    w = 45
    Yn = (w-x1)*(y2-y1)/(2*w-x2-x1)
    viableSpots.append((w,y1+Yn))
    #right wall
    w = app.width-45
    Yn = (w-x1)*(y2-y1)/(2*w-x2-x1)
    viableSpots.append((w,y1+Yn))
    return viableSpots


def angleCheck(app,pos,cellPos,lookPos):
    x,y = pos
    cX,cY = cellPos
    lX,lY = lookPos
    angle1 = atan2(cY-y,cX-x)
    angle2 = atan2(lY-cY,lX-cX)
    dif = abs(abs(angle1)-abs(angle2))
    if(dif < pi/16):
        return True

def getImagePrefix():
    if (platform.system() == "Windows"):
        imagePrefix = "images\\"
    else:
        imagePrefix = "images/"
    return imagePrefix