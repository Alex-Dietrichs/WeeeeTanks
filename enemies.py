import objects

class Enemy(objects.tank):
    def __init__(self, x, y, speed) -> None:
        super().__init__(x, y, speed)
        self.target = (x,y)
    
    def findPath():
        pass
    def targetPlayer():
        pass
class tanEnemy(Enemy):
    def __init__(self, x, y) -> None:
        super().__init__(x, y,0)