import objects

class Enemy(objects.tank):
    def __init__(self, x, y,  height, width, speed) -> None:
        super().__init__(height, width, speed)
        self.target = (x,y)
    def fire():
        pass
    
    def findPath():
        pass