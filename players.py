import objects
class player(objects.tank):
    def __init__(self, x, y) -> None:
        super().__init__(x,y,100)