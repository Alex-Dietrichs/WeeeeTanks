class baseObject():
    def __init__(self,height,width,speed) -> None:
        self.collider = (width,height,speed)
        self.velocity = (0,0)
        self.speed = speed
    def getCollider(self):
        return self.collider

    def draw(self):
        pass
class tank(baseObject):
    def __init__(self, x, y, speed) -> None:
        super().__init__(100, 100, speed)
        self.pos = (x,y)
    def fire():
        newBullet = bullet()

        return newBullet
    def layMine():
        pass
    def move():
        pass

class bullet(baseObject):
    def __init__(self, speed, dx,dy) -> None:
        super().__init__(10, 5,speed)
        self.unitVelocity = (dx,dy)
