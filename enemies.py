import objects
import random
import math
from helperFunc import *
class Enemy(objects.tank):
    def __init__(self, x, y, speed) -> None:
        super().__init__(x, y, speed)
        self.target = (x,y)
        self.startx = x
        self.starty = y
        self.targetAngle = 0
        self.currentAngle = 0
        self.aimSpeed = math.pi/8
        self.timeSinceLastAim = 5
        self.path = []
        self.timeSinceLastFire = 1
        self.fireDelay = 2
        self.aimDelay = 5
        self.findDelay = 10
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
                if(k>=0 and k< 24 and p>=0 and p < 14 and nextPos not in app.currentLayout):
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
            if(tI,tJ) not in app.currentLayout and tI>=0 and tI <=24 and tJ >= 0 and tJ <=14: 
                break
        return (tI,tJ)
    
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            xp,yp = app.player.getPos()
            hyp = ((self.x-xp)**2 + (self.y - yp)**2)**.5
            xPart = xp-self.x
            yPart = yp-self.y
            self.targetAngle = math.atan(yPart/xPart)+math.pi
            if(xPart>0):
                self.targetAngle-=math.pi
            self.timeSinceLastAim = 0

    def moveAim(self,app):
        angleChange = self.aimSpeed*app.timeConstant
        bullet = None
        if(abs(self.currentAngle - self.targetAngle) < abs(angleChange)):
            self.currentAngle = self.targetAngle
        else:
            dir = (self.targetAngle-self.currentAngle)/abs((self.targetAngle-self.currentAngle))
            self.currentAngle += angleChange*dir
        if((self.timeSinceLastFire >= self.fireDelay and 
                self.currentAngle == self.targetAngle) or 
                self.timeSinceLastFire >= 1.5*self.fireDelay):
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
        super().__init__(x, y,0)
    def draw(self,canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2, fill = 'brown3', width = 0)
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            self.targetAngle = random.randint(0,359)*math.pi/180
            self.timeSinceLastAim = 0
    def followPath(self,app,layout):
        pass


class greyEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100)
        self.aimSpeed = math.pi
        self.fireDelay = 2
        self.aimDelay = 3
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            xp,yp = app.player.getPos()
            hyp = ((self.x-xp)**2 + (self.y - yp)**2)**.5
            xPart = xp-self.x
            yPart = yp-self.y
            self.targetAngle = math.atan(yPart/xPart)+math.pi
            if(xPart>0):
                self.targetAngle-=math.pi
            self.timeSinceLastAim = 0