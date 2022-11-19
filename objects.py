import math
class baseObject():
    def __init__(self,x,y,height,width,speed) -> None:
        self.width = width
        self.height = height
        self.dx = 0
        self.dy = 0
        self.speed = speed
        self.x = x
        self.y = y
    def getSize(self):
        return (self.width,self.height)
    def getPos(self):
        return (self.x,self.y)
    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2)
    def getSpeed(self):
        return self.speed
    def getVelocity(self):
        return (self.dx,self.dy)
    def move(self,relativeSpeed):
        #Causes issues with player movement
        #if(self.dx > 0 or self.dy > 0):
         #   magnitude = math.sqrt(self.dx**2+self.dy**2)
          #  self.dx,self.dy = self.dx/magnitude,self.dy/magnitude
        self.x += self.dx * relativeSpeed
        self.y += self.dy * relativeSpeed
    def checkCollision(self,pos,size):
        x2,y2 = pos
        w2,h2 = size
        ul1x = self.x - self.width/2
        ul1y = self.y - self.height/2
        br1x = self.x + self.width/2
        br1y = self.y + self.height/2
        ul2x = x2 - w2/2
        ul2y = y2 - h2/2
        br2x = x2 + w2/2
        br2y = y2 + h2/2
        if ul1x > br2x or ul2x > br1x:
            return False

        if br1y < ul2y or br2y < ul1y:
            return False
        return True

class tank(baseObject):
    def __init__(self, x, y, speed) -> None:
        super().__init__(x,y,50, 50, speed)
        self.maxBullets = 2
        self.currentBullets = 0
    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            magnitude = math.sqrt(dx**2+dy**2)
            dx/=magnitude
            dy/=magnitude
            newBullet = bullet(self.x+dx*40,self.y+dy*40,dx,dy,self)
            self.currentBullets += 1
            return newBullet
        return None
    def bulletDestroyed(self):
        self.currentBullets -= 1
    def layMine(self):
        pass
    def move(self,relativeSpeed,layout):
        if((self.x>65 or self.dx > 0) and (self.x<880-65 or self.dx < 0) and self.layoutOkayX(relativeSpeed,layout)):
            self.x += self.dx * relativeSpeed
        if((self.y>65 or self.dy > 0) and (self.y<640-65 or self.dy < 0) and self.layoutOkayY(relativeSpeed,layout)):
            self.y += self.dy * relativeSpeed
    def layoutOkayX(self,relativeSpeed,layout):
        return True
    def layoutOkayY(self,relativeSpeed,layout):
        return True


class bullet(baseObject):
    def __init__(self, x, y,dx,dy,creator) -> None:
        super().__init__(x,y,5,5,speed=500)
        magnitude = math.sqrt(dx**2+dy**2)
        self.dx,self.dy = dx/magnitude,dy/magnitude
        self.creator = creator
        self.ricochetCount = 0
    def destroyBullet(self):
        self.creator.bulletDestroyed()
    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2, fill = 'black')
    def ricochet(self):
        self.ricochetCount += 1
        if(self.ricochetCount > 1):
            self.destroyBullet()
            return True
        return False