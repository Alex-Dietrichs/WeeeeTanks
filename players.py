import objects
class player(objects.tank):
    def __init__(self, x, y) -> None:
        super().__init__(x,y,100)
        self.maxBullets = 5
    def draw(self,canvas):
        canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,
        self.x+self.width/2,self.y+self.height/2, fill = "blue", width = 0)