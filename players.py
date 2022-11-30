import objects
from cmu_112_graphics import ImageTk
class player(objects.tank):
    def __init__(self, x, y) -> None:
        super().__init__(x,y,250,5, imagePath='images\\playerTank.png',turretImagePath='images\\playerTurret.png')
