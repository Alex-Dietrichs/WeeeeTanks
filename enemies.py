import objects
from random import randint
from math import cos,sin
from helperFunc import *
import platform

if (platform.system() == "Windows"):
    imagePrefix = "images\\"
else:
    imagePrefix = "images/"


class Enemy(objects.tank):
    def __init__(self, x, y, speed, maxBullets, imagePath, turretImagePath) -> None:
        super().__init__(x, y, speed,maxBullets, imagePath,turretImagePath)
        self.target = (x,y)
        self.startx = x
        self.starty = y
        self.targetAngle = 0
        self.currentAngle = pi/2
        self.timeSinceLastAim = 5
        self.path = []
        self.timeSinceFind = 2
        #Changeable
        self.aimSpeed = pi/2
        self.fireDelay = 1.5
        self.aimDelay = .1
        self.canLayMine = False
    #idea from https://en.wikipedia.org/wiki/A*_search_algorithm
    def findPath(self,app):
        self.timeSinceFind = 0
        startPos = locationToCell((self.x,self.y))
        targetPos = self.pickMoveTarget(app)
        if(targetPos == None):
            return None
        found = {startPos}
        previous = dict()
        gScore = dict()
        gScore[startPos] = 0
        fScore = dict()
        fScore[startPos] = self.heuristicAlgo(startPos,targetPos)

        while len(found) != 0:
            current = None
            bestScore = 10000
            for key in fScore:
                curScore = fScore[key]
                if key in found and curScore < bestScore:
                    current = key
                    bestScore = curScore
            if current == targetPos:
                return self.buildPath(previous,current)
            found.remove(current)
            i,j = current
            next = [(i+1,j),(i-1,j),(i,j+1),(i,j-1),(i+1,j+1),(i+1,j-1),(i-1,j-1),(i-1,j+1)]
            for nextPos in next:
                (k,p) = nextPos
                if(k>=0 and k < 22 and p>=0 and p < 16 and 
                nextPos not in app.currentTotalSet and self.checkMines(app,nextPos)):
                    tempgScore = gScore[current] + sqrt((nextPos[0]-i)**2+(nextPos[1]-j)**2)
                    if(tempgScore < gScore.get(nextPos,10000)):
                        previous[nextPos] = current
                        gScore[nextPos] = tempgScore
                        fScore[nextPos] = tempgScore + self.heuristicAlgo(nextPos,targetPos)
                        if nextPos not in found:
                            found.add(nextPos)
        return None
    
    def buildPath(self,past,current):
        path = [current]
        while current in past:
            current = past[current]
            path.insert(0,current)
        return path

    def heuristicAlgo(self,current,target):
        i,j = current
        l,m = target
        cost = sqrt((i-l)**2+(j-m)**2)
        return cost

    def pickMoveTarget(self,app):
        n=0
        goodFind = True
        while n<10:
            iDif = randint(-5,5)
            jDif = randint(-5,5)
            i,j = locationToCell((self.x,self.y))
            tI,tJ = i+iDif,j+jDif
            if((tI,tJ) not in app.currentLayout and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16
                and self.checkMines(app, (tI,tJ))):
                goodFind = True
                break
            n+=1
        if(goodFind):
            return (tI,tJ)
        else:
            return self.backupPickMoveTarget(app)
    def pickMoveTargetDefensive(self,app):
        n=0
        goodFind = False
        while n<10:
            iDif = randint(-5,5)
            jDif = randint(-5,5)
            i,j = locationToCell((self.x,self.y))
            tI,tJ = i+iDif,j+jDif
            if((tI,tJ) not in app.currentTotalSet and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16 
            and self.checkMines(app, (tI,tJ))): 
                canSee = canSeeSpace(app,cellToLocation((tI,tJ)),app.player.getPos())
                if self.fireDelay > self.timeSinceLastFire and not canSee:
                    goodFind = True
                    break
                elif self.fireDelay < self.timeSinceLastFire and canSee:
                    goodFind = True
                    break
            else:
                n-=1
            n+=1
        if(goodFind):
            return (tI,tJ)
        else:
            return self.backupPickMoveTarget(app)
    def pickMoveTargetNone(self,app):
        return None
    def pickMoveTargetAggressive(self,app):
        n=0
        goodFind = False
        while n<10:
            iDif = randint(-5,5)
            jDif = randint(-5,5)
            i,j = locationToCell((self.x,self.y))
            tI,tJ = i+iDif,j+jDif
            if((tI,tJ) not in app.currentLayout and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16
            and self.checkMines(app, (tI,tJ))): 
                canSee = canSeeSpace(app,cellToLocation((tI,tJ)),app.player.getPos())
                if canSee:
                    goodFind = True
                    break
            else:
                n-=1
            n+=1
        if(goodFind):
            return (tI,tJ)
        else:
            return self.backupPickMoveTarget(app)
    def pickMoveTargetInter(self,app):
        n=0
        goodFind = False
        while n<20:
            iDif = randint(-5,5)
            jDif = randint(-5,5)
            i,j = locationToCell((app.player.x,app.player.y))
            tI,tJ = i+iDif,j+jDif
            if((tI,tJ) not in app.currentLayout and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16
            and self.checkMines(app, (tI,tJ))): 
                goodFind = True
                break
            else:
                n-=1
            n+=1
        if(goodFind):
            return (tI,tJ)
        else:
            return self.backupPickMoveTarget(app)
    
    def backupPickMoveTarget(self,app):
        n=0
        while n<10:
            iDif = randint(-8,8)
            jDif = randint(-8,8)
            i,j = locationToCell((app.player.x,app.player.y))
            tI,tJ = i+iDif,j+jDif
            if((tI,tJ) not in app.currentLayout and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16
            and self.checkMines(app, (tI,tJ))): 
                break
            else:
                n-=1
            n+=1
        return (tI,tJ)
    
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            xp,yp = app.player.getPos()
            xPart = xp-self.x
            yPart = yp-self.y
            self.targetAngle = atan2(yPart,xPart)
            self.timeSinceLastAim = 0

    def moveAim(self,app):
        angleChange = self.aimSpeed*app.timeConstant
        bullet = None
        if(self.currentAngle < 0): self.currentAngle += 2*pi
        if(self.targetAngle < 0): self.targetAngle += 2*pi
        self.currentAngle = self.currentAngle % (pi*2)
        mag = abs((self.targetAngle-self.currentAngle))
        if(mag < abs(angleChange)):
            self.currentAngle = self.targetAngle
        else:
            dir = (self.targetAngle-self.currentAngle)/mag
            if mag>pi: dir=-dir
            self.currentAngle += angleChange*dir
        self.rotateTurretImage(-self.currentAngle-pi/2)

        return self.checkFire(app)

    def checkFire(self,app):
        bullet = None
        if((self.timeSinceLastFire >= self.fireDelay and 
                self.currentAngle == self.targetAngle)):
            if(canSeeSpace(app,self.getPos(),app.player.getPos())):
                dx = cos(self.currentAngle)
                dy = sin(self.currentAngle)
                bullet = self.fire(dx,dy)
                self.timeSinceLastFire = 0
                self.path = self.findPath(app)
        self.timeSinceLastFire += app.timeConstant
        self.pickAimTarget(app)
        return bullet

    def followPath(self,app):
        efdsqr = self.efdx**2+self.efdy**2
        if(self.path == None or len(self.path) == 0 or (self.timeSinceFind > .1 and ( efdsqr < .1))):
            self.path = self.findPath(app)
        else:
            self.getMovementDir()
            self.move(self.speed*app.timeConstant,app.currentTotalSet)
            if(locationToCell((self.x,self.y)) == self.path[0]):
                pX,pY = cellToLocation(self.path[0])
                distance = sqrt((self.x-pX)**2+(self.y-pY)**2)
                if (distance < 5):
                    self.path.pop(0)
            self.timeSinceFind += app.timeConstant
            self.timeSinceLastMine += app.timeConstant

    def getMovementDir(self):
        if(len(self.path)>0):
            targetX,targetY = cellToLocation(self.path[0])
            xVec = targetX - self.x
            yVec = targetY - self.y
            if(xVec == 0 and yVec == 0):
                self.dx,self.dy = 0,0
            else:
                magnitude = sqrt(xVec**2 + yVec**2)
                self.dx = xVec/magnitude
                self.dy = yVec/magnitude
        else:
            self.dx,self.dy = 0,0

    def checkMines(self,app,pos):
        for mine in app.currentMines:
            if pos == locationToCell(mine.getPos()):
                return False
        return True

    def layMine(self,app):
        if(self.canLayMine and self.timeSinceLastMine > self.mineDelay):
            distance = sqrt((self.x-app.player.x)**2+(self.y-app.player.y)**2)
            if distance < 400:
                return super().layMine(app)

class brownEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y,0,1,imagePrefix + 'brownTank.png',imagePrefix + 'brownTurret.png')
        self.aimDelay = 1
        self.aimSpeed = pi/4
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        picker = randint(0,1)
        if(self.timeSinceLastAim > self.aimDelay):
            if(picker == 0):
                self.targetAngle = randint(0,359)*pi/180
            else:
                xp,yp = app.player.getPos()
                xPart = xp-self.x
                yPart = yp-self.y
                self.targetAngle = atan2(yPart,xPart)
            self.timeSinceLastAim = 0
    def followPath(self,app):
        pass
    def pickMoveTarget(self, app):
        return self.pickMoveTargetNone(app)

class greyEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,1,imagePrefix + 'greyTank.png',imagePrefix + 'greyTurret.png')
    def pickMoveTarget(self, app): #Defensive
       return self.pickMoveTargetDefensive(app)

class tealEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,1,imagePrefix + 'tealTank.png',imagePrefix + 'tealTurret.png')
        self.aimSpeed = pi
    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            magnitude = sqrt(dx**2+dy**2)
            dx/=magnitude
            dy/=magnitude
            newBullet = objects.fastBullet(self.x+dx*40,self.y+dy*40,dx,dy,self)
            self.currentBullets += 1
            return newBullet
        return None
    def pickMoveTarget(self, app):
        return self.pickMoveTargetDefensive(app)

class yellowEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 200,1,imagePrefix + 'yellowTank.png',imagePrefix + 'yellowTurret.png')
        self.aimSpeed = pi
        self.mineDelay = 2
        self.maxMines = 4
        self.canLayMine = True
        self.timeSinceLastMine = randint(0,9)/3
    
    def checkMines(self,app,pos):
        for mine in app.currentMines:
            if locationToCell(mine.getPos()) == locationToCell(self.getPos()):
                return True
        for mine in app.currentMines:
            
            i,j = locationToCell(mine.getPos())
            around = set([(i,j),(i+1,j),(i-1,j),(i,j+1),(i,j-1),(i+1,j+1),(i+1,j-1),(i-1,j-1),(i-1,j+1)])
            if pos in around:
                return False
        return True
    def pickMoveTarget(self, app):
        return super().pickMoveTargetInter(app)

class redEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,3,imagePrefix + 'redTank.png',imagePrefix + 'redTurret.png')
        self.aimSpeed = pi
        self.fireDelay = .5
    def pickMoveTarget(self, app):
        return super().pickMoveTargetAggressive(app)

class greenEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 0,2,imagePrefix + 'greenTank.png',imagePrefix + 'greenTurret.png')
        self.aimSpeed = pi
        self.fireDelay = .5
    def followPath(self,app):
        pass
    def pickMoveTarget(self, app):
        return self.pickMoveTargetNone(app)

    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            magnitude = sqrt(dx**2+dy**2)
            dx/=magnitude
            dy/=magnitude
            newBullet = objects.fastBullet(self.x+dx*40,self.y+dy*40,dx,dy,self)
            newBullet.ricochetCount = -1
            self.currentBullets += 1
            return newBullet
        return None
    
    def pickAimTarget(self, app):#should be able to use richochets
        self.timeSinceLastAim += app.timeConstant
        cell = None
        if(self.timeSinceLastAim > self.aimDelay):
            if(not canSeeSpace(app,self.getPos(),app.player.getPos())):
                cell = canSeeSpaceWithRich(app,self.getPos(),app.player.getPos())
                if cell != None:
                    xp,yp = cellToLocation(cell)
                    xPart = xp-self.x
                    yPart = yp-self.y
            if(cell == None):
                xp,yp = app.player.getPos()
                dx,dy = app.player.getVelocity()
                xp += dx * 10
                yp += dy * 10
                xPart = xp-self.x
                yPart = yp-self.y
            self.targetAngle = atan2(yPart,xPart)
            self.timeSinceLastAim = 0


    def checkFire(self,app):
        bullet = None
        if((self.timeSinceLastFire >= self.fireDelay and 
                self.currentAngle == self.targetAngle)):
            if(canSeeSpace(app,self.getPos(),app.player.getPos())
                or canSeeSpaceWithRich(app,self.getPos(),app.player.getPos()) != None):
                dx = cos(self.currentAngle)
                dy = sin(self.currentAngle)
                bullet = self.fire(dx,dy)
                self.timeSinceLastFire = 0
                self.path = self.findPath(app)
        self.timeSinceLastFire += app.timeConstant
        self.pickAimTarget(app)
        return bullet



class purpleEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,5,imagePrefix + 'purpleTank.png',imagePrefix + 'purpleTurret.png')
        self.aimSpeed = pi/8
        self.fireDelay = .5
        self.aimDelay = .5