import objects
import random
import math
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
    def locationToCell(self,location):
        x,y = location
        i = (x-20)//22
        j = (y-20)//16
        return (i-1,j-1)
    def findPath(self,app, ):
        startPos = self.locationToCell((self.x,self.y))
        target = self.pickMoveTarget(app)
        self.path = self.findPathHelper(app,startPos,target)
    def findPathHelper(self,app,startPos,targetPos):
        found = startPos
        previous = dict()
        return []
    def buildPath(self,past,current):
        path = [current]
        while current in past:
            current = past[current]
            path.insert(0,current)
        return path
    def pickMoveTarget(self,app):
        pass
    def pickAimTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            self.targetAngle = random.randint(0,359)*math.pi/180
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
        print(self.timeSinceLastFire, self.targetAngle)
        self.pickAimTarget(app)
        return bullet

    def followPath(self,app,layout):
        if(len(self.path) > 0):
            self.move(self.speed*app.timeConstant,layout)
        else:
            #self.findPath(app)
            pass

class brownEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y,0)
    def draw(self,canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2, fill = 'brown3', width = 0)


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