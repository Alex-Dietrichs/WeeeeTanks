import objects
import random
import math
from helperFunc import *
class Enemy(objects.tank):
    def __init__(self, x, y, speed, maxBullets, imagePath, turretImagePath) -> None:
        super().__init__(x, y, speed,maxBullets, imagePath,turretImagePath)
        self.target = (x,y)
        self.startx = x
        self.starty = y
        self.targetAngle = 0
        self.currentAngle = math.pi/2
        self.timeSinceLastAim = 5
        self.path = []
        self.timeSinceLastFire = 1.5
        self.timeSinceFind = 2
        #Changeable
        self.aimSpeed = math.pi/2
        self.fireDelay = 1
        self.aimDelay = .5
        self.time0 = 0
    #idea from https://en.wikipedia.org/wiki/A*_search_algorithm
    def findPath(self,app):
        self.timeSinceFind = 0
        self.time0 = time.time()
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
                if(k>=0 and k< 22 and p>=0 and p < 16 and nextPos not in app.currentTotalSet):
                    tempgScore = gScore[current] + math.sqrt((nextPos[0]-i)**2+(nextPos[1]-j)**2)
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
        print(f'Path finding time: {time.time()-self.time0}')
        print(self.path)
        return path

    def heuristicAlgo(self,current,target):
        i,j = current
        l,m = target
        cost = math.sqrt((i-l)**2+(j-m)**2)
        return cost

    def pickMoveTarget(self,app):
        n=0
        while n<10:
            iDif = random.randint(-5,5)
            jDif = random.randint(-5,5)
            i,j = locationToCell((self.x,self.y))
            tI,tJ = i+iDif,j+jDif
            if(tI,tJ) not in app.currentLayout and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16: 
                break
            n+=1
        return (tI,tJ)
    
    def pickMoveTargetDefensive(self,app):
        n=0
        while n<20:
            iDif = random.randint(-8,8)
            jDif = random.randint(-8,8)
            i,j = locationToCell((self.x,self.y))
            tI,tJ = i+iDif,j+jDif
            if((tI,tJ) not in app.currentLayout and tI>=0 and tI <=22 and tJ >= 0 and tJ <=16): 
                canSee = self.canSeePlayer(app,cellToLocation((i,j)))
                if self.fireDelay > self.timeSinceLastFire and not canSee:
                    break
                elif self.fireDelay < self.timeSinceLastFire and canSee:
                    break
            n+=1
        return (tI,tJ)
    def pickMoveTargetNone(self,app):
        return None
    
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
        if(self.currentAngle < 0): self.currentAngle += 2*math.pi
        if(self.targetAngle < 0): self.targetAngle += 2*math.pi
        self.currentAngle = self.currentAngle % (math.pi*2)
        mag = abs((self.targetAngle-self.currentAngle))
        if(mag < abs(angleChange)):
            self.currentAngle = self.targetAngle
        else:
            dir = (self.targetAngle-self.currentAngle)/mag
            if mag>math.pi: dir=-dir
            self.currentAngle += angleChange*dir
        self.rotateTurretImage(-self.currentAngle-math.pi/2)

        #fire
        if((self.timeSinceLastFire >= self.fireDelay and 
                self.currentAngle == self.targetAngle)):
            if(self.canSeePlayer(app,self.getPos())):
                dx = math.cos(self.currentAngle)
                dy = math.sin(self.currentAngle)
                bullet = self.fire(dx,dy)
                self.timeSinceLastFire = 0
                self.path = self.findPath(app)
        
        self.timeSinceLastFire += app.timeConstant
        self.pickAimTarget(app)
        return bullet

    def followPath(self,app):
        efdsqr = self.efdx**2+self.efdy**2
        if(self.path == None or (self.timeSinceFind > .1 and (len(self.path) == 0 or efdsqr < .05))):
            self.path = self.findPath(app)
        else:
            self.getMovementDir()
            self.move(self.speed*app.timeConstant,app.currentTotalSet)
            if(locationToCell((self.x,self.y)) == self.path[0]):
                self.path.pop(0)
            self.timeSinceFind += app.timeConstant

    
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

    def canSeePlayer(self,app,pos):
        pX,pY = app.player.getPos()
        x,y = pos
        iCheck,jCheck = locationToCell((x,y))
        iFinal,jFinal = locationToCell((pX,pY))
        dx = (iFinal-iCheck)
        dy = (jFinal-jCheck)
        if(dx!=dy):
            if(abs(dx)>abs(dy)):
                dy /= abs(dx)
                dx /= abs(dx)
                while(iCheck != iFinal):
                    iCheck+=dx
                    jCheck += dy
                    if((int(iCheck),round(jCheck)) in app.currentLayoutSet):
                        return False
            else:
                dx /= abs(dy)
                dy /= abs(dy)
                while(jCheck != jFinal):
                    iCheck+=dx
                    jCheck+=dy
                    if((int(round(iCheck)),int(jCheck)) in app.currentLayoutSet):
                        return False
        return True

class brownEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y,0,1,'images\\brownTank.png','images\\brownTurret.png')
        self.aimDelay = 5
        self.aimSpeed = math.pi/4
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        picker = random.randint(0,1)
        if(self.timeSinceLastAim > self.aimDelay):
            if(picker == 0):
                self.targetAngle = random.randint(0,359)*math.pi/180
            else:
                xp,yp = app.player.getPos()
                xPart = xp-self.x
                yPart = yp-self.y
                self.targetAngle = math.atan2(yPart,xPart)
            self.timeSinceLastAim = 0
    def followPath(self,app):
        pass
    def pickMoveTarget(self, app):
        return self.pickMoveTargetNone(self,app)


class greyEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,1,'images\\greyTank.png','images\\greyTurret.png')
    def pickMoveTarget(self, app): #Defensive
       return self.pickMoveTargetDefensive(app)

class tealEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,1,'images\\tealTank.png','images\\tealTurret.png')
        self.aimSpeed = math.pi/2
        self.fireDelay = 1.5
        self.aimDelay = .25
    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            magnitude = math.sqrt(dx**2+dy**2)
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
        super().__init__(x, y, 100,1,'images\\yellowTank.png','images\\yellowTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = 1.5
        self.aimDelay = .5
class redEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,3,'images\\redTank.png','images\\redTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = .5
        self.aimDelay = .5
class greenEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,2,'images\\greenTank.png','images\\greenTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = .5
        self.aimDelay = .5
    def followPath(self,app):
        pass
    def pickMoveTarget(self, app):
        return self.pickMoveTargetNone(self,app)
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
            xPart = xp-self.x
            yPart = yp-self.y
            self.targetAngle = math.atan2(yPart,xPart)
            self.timeSinceLastAim = 0

class purpleEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100,5,'images\\purpleTank.png','images\\purpleTurret.png')
        self.aimSpeed = math.pi/8
        self.fireDelay = .5
        self.aimDelay = .5