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
    def getCollider(self):
        return (self.width,self.height)

    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2)
    def getSpeed(self):
        return self.speed
    def move(self,relativeSpeed):
        self.x += self.dx * relativeSpeed
        self.y += self.dy * relativeSpeed
        print(self.x,self.y)
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
        super().__init__(x,y,10,5,speed=100)
        magnitude = math.sqrt(dx**2+dy**2)
        self.dx,self.dy = dx/magnitude,dy/magnitude
        self.creator = creator
    def destroyBullet(self):
        self.creator.bulletDestroyed()
    def draw(self, canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2, fill = 'black')
