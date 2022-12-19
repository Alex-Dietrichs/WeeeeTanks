import objects
from cmu_112_graphics import ImageTk
from helperFunc import locationToCell, getImagePrefix


imagePrefix = getImagePrefix()

class player(objects.tank):
    def __init__(self, x, y) -> None:
        super().__init__(x,y,200,5, imagePath=imagePrefix + 'playerTank.png',turretImagePath=imagePrefix + 'playerTurret.png')
        self.maxMines = 2
        self.fireDelay = .05
    def checkMines(self,app,pos):
        for mine in app.currentMines:
            if pos == locationToCell(mine.getPos()):
                return False
        return True