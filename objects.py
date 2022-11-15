class baseObject():
    def __init__(self,height,width) -> None:
        self.collider = (width,height)

    def getCollider(self):
        return self.collider

    def draw(self):
        pass
class tank(baseObject):
    def __init__(self, height, width) -> None:
        super().__init__(height, width)
    def fire():
        pass
    def layMine():
        pass
    def move():
        pass

class bullet(baseObject):
    pass
