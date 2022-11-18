import objects
import random
import time
import math
class Enemy(objects.tank):
    def __init__(self, x, y, speed) -> None:
        super().__init__(x, y, speed)
        self.target = (x,y)
        self.startx = x
        self.starty = y
        self.targetAngle = 0
        self.currentAngle = 0
        self.aimSpeed = 10
        self.timeSinceLastAim = 5
        self.path = []
        self.timeSinceLastFire = 1
        self.fireDelay = 2
        self.aimDelay = 5
    def findPath(self,app):
        pass
    def pickTarget(self, app):
        self.timeSinceLastAim += app.timeConstant
        if(self.timeSinceLastAim > self.aimDelay):
            self.targetAngle = random.randint(0,359)
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
        self.pickTarget(app)
        return bullet

    def followPath(self,app,layout):
        if(len(self.path) > 0):
            self.move(self.speed*app.timeConstant,layout)
        else:
            self.findPath(app)

class brownEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y,0)

class greyEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, 100)
        self.aimSpeed = 5
        self.fireDelay = 2
        self.aimDelay = 3