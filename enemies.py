import objects
import random
import math
from helperFunc import *
class Enemy(objects.tank):
    def __init__(self, x, y, speed, imagePath, turretImagePath) -> None:
        super().__init__(x, y, speed, imagePath,turretImagePath)
        self.target = (x,y)
        self.startx = x
        self.starty = y
        self.targetAngle = 0
        self.currentAngle = math.pi/2
        self.timeSinceLastAim = 5
        self.path = []
        self.timeSinceLastFire = .5
        #Changeable
        self.aimSpeed = math.pi/4
        self.fireDelay = 1.5
        self.aimDelay = .5
        self.findDelay = 5
    #idea from https://en.wikipedia.org/wiki/A*_search_algorithm
    def findPath(self,app):
        startPos = locationToCell((self.x,self.y))
        targetPos = self.pickMoveTarget(app)
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
            next = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
            for nextPos in next:
                (k,p) = nextPos
                if(k>=0 and k< 22 and p>=0 and p < 16 and nextPos not in app.currentLayout):
                    tempgScore = gScore[current] + 1
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
        cost = abs(i-l)+abs(j-m)
        return cost

    def pickMoveTarget(self,app):
        while True:
            iDif = random.randint(-5,5)
            jDif = random.randint(-5,5)
            i,j = locationToCell((self.x,self.y))
            tI,tJ = i+iDif,j+jDif
            if(tI,tJ) not in app.currentLayout and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16: 
                break
        return (tI,tJ)
    
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            xp,yp = app.player.getPos()
            hyp = ((self.x-xp)**2 + (self.y - yp)**2)**.5
            xPart = xp-self.x
            yPart = yp-self.y
            self.targetAngle = math.atan2(yPart,xPart)
            self.timeSinceLastAim = 0

    def moveAim(self,app):
        angleChange = self.aimSpeed*app.timeConstant
        bullet = None
        if(abs(self.currentAngle - self.targetAngle) < abs(angleChange)):
            self.currentAngle = self.targetAngle
        else:
            mag = abs((self.targetAngle-self.currentAngle))
            dir = (self.targetAngle-self.currentAngle)/mag
            if mag > 180: dir = -dir
            self.currentAngle += angleChange*dir
        self.rotateTurretImage(-self.currentAngle-math.pi/2)

        #fire
        if((self.timeSinceLastFire >= self.fireDelay and 
                self.currentAngle == self.targetAngle) or 
                self.timeSinceLastFire >= 3*self.fireDelay):
            dx = math.cos(self.currentAngle)
            dy = math.sin(self.currentAngle)
            bullet = self.fire(dx,dy)
            self.timeSinceLastFire = 0
        
        self.timeSinceLastFire += app.timeConstant
        self.pickAimTarget(app)
        return bullet

    def followPath(self,app,layout):
        if(self.path != None and len(self.path) > 0):
            self.getMovementDir()
            self.move(self.speed*app.timeConstant,layout)
            if(locationToCell((self.x,self.y)) == self.path[0]):
                self.path.pop(0)
        elif self.findDelay < 3:
            self.findDelay += app.timeConstant
        else: 
            self.path = self.findPath(app)
            print(self.path)
            self.findDelay = 0
    
    def getMovementDir(self):
        if(len(self.path)>0):
            targetX,targetY = cellToLocation(self.path[0])
            xVec = targetX - self.x
            yVec = targetY - self.y
            if(xVec == 0 and yVec == 0):
                self.dx,self.dy = 0,0
            else:
                magnitude = math.sqrt(xVec**2 + yVec**2)
                self.dx = xVec/magnitude
                self.dy = yVec/magnitude
        else:
            self.dx,self.dy = 0,0
            self.findDelay += 3

class brownEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y,0,'images\\brownTank.png','images\\brownTurret.png')
        self.aimDelay = 5
        self.aimSpeed = math.pi/8
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            self.targetAngle = random.randint(0,359)*math.pi/180
            self.timeSinceLastAim = 0
    def followPath(self,app,layout):
        pass


class greyEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,'images\\greyTank.png','images\\greyTurret.png')

class tealEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,'images\\tealTank.png','images\\tealTurret.png')
        #self.aimSpeed = math.pi/8
        self.fireDelay = 1.5
        self.aimDelay = .5
    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            magnitude = math.sqrt(dx**2+dy**2)
            dx/=magnitude
            dy/=magnitude
            newBullet = objects.fastBullet(self.x+dx*40,self.y+dy*40,dx,dy,self)
            self.currentBullets += 1
            return newBullet
        return None
class yellowEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,'images\\yellowTank.png','images\\yellowTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = 1.5
        self.aimDelay = .5
class redEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,'images\\redTank.png','images\\redTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = .5
        self.aimDelay = .5
        self.maxBullets = 3
class greenEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,'images\\greenTank.png','images\\greenTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = .5
        self.aimDelay = .5
        self.maxBullets = 2
    def followPath(self,app,layout):
        pass
    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            magnitude = math.sqrt(dx**2+dy**2)
            dx/=magnitude
            dy/=magnitude
            newBullet = objects.fastBullet(self.x+dx*40,self.y+dy*40,dx,dy,self)
            self.currentBullets += 1
            return newBullet
        return None
    def pickAimTarget(self, app):#Change
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            xp,yp = app.player.getPos()
            hyp = ((self.x-xp)**2 + (self.y - yp)**2)**.5
            xPart = xp-self.x
            yPart = yp-self.y
            self.targetAngle = math.atan2(yPart,xPart)
            self.timeSinceLastAim = 0

class purpleEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,'images\\purpleTank.png','images\\purpleTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = .5
        self.aimDelay = .5
        self.maxBullets = 5 