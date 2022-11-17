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
    def move(self,relativeSpeed):
        #Causes issues with player movement
        #if(self.dx > 0 or self.dy > 0):
         #   magnitude = math.sqrt(self.dx**2+self.dy**2)
          #  self.dx,self.dy = self.dx/magnitude,self.dy/magnitude
        self.x += self.dx * relativeSpeed
        self.y += self.dy * relativeSpeed
    def checkCollision(self,baseObject):
        x2,y2 = baseObject.getPos()
        w2,h2 = baseObject.getSize()
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
        print(f"collision between {self} and {baseObject}")
        return True

class tank(baseObject):
    def __init__(self, x, y, speed) -> None:
        super().__init__(x,y,50, 50, speed)
        self.maxBullets = 2
        self.currentBullets = 0
    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            newBullet = bullet(self.x,self.y,dx,dy,self)
            self.currentBullets += 1
            return newBullet
        return None
    def bulletDestroyed(self):
        self.currentBullets -= 1
    def layMine(self):
        pass

class bullet(baseObject):
    def __init__(self, x, y,dx,dy,creator) -> None:
        super().__init__(x,y,5,5,speed=500)
        magnitude = math.sqrt(dx**2+dy**2)
        self.dx,self.dy = dx/magnitude,dy/magnitude
        self.creator = creator
    def destroyBullet(self):
        self.creator.bulletDestroyed()
    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2, fill = 'black')
