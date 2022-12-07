import math
from cmu_112_graphics import *
from helperFunc import *
class baseObject():
    def __init__(self,x,y,height,width,speed,imagePath) -> None:
        self.width = width
        self.height = height
        self.dx = 0
        self.dy = 0
        self.speed = speed
        self.x = x
        self.y = y
        self.image = None
        self.loadedImage = None
        self.imagePath = imagePath
    def getSize(self):
        return (self.width,self.height)
    def getPos(self):
        return (self.x,self.y)
    def setPos(self,pos):
        self.x,self.y = pos
    def draw(self, canvas):
        canvas.create_image(self.x,self.y,image = ImageTk.PhotoImage(self.image))
    def initImage(self,app):
        self.loadedImage = app.scaleImage(app.loadImage(self.imagePath),1/4)
        self.image = self.loadedImage
    def rotateImage(self):
        theta = self.toDegrees(math.atan2(self.dx,self.dy) + math.pi)
        self.image = self.loadedImage.rotate(angle=theta, resample = Image.Resampling.BILINEAR)

    def getSpeed(self):
        return self.speed
    def getVelocity(self):
        return (self.dx,self.dy)
    def move(self,relativeSpeed):
        self.x += self.dx * relativeSpeed
        self.y += self.dy * relativeSpeed
    def checkCollision(self,pos,size):
        x2,y2 = pos
        w2,h2 = size
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
        return True
    @staticmethod
    def toDegrees(angle):
        return angle*180/math.pi

class tank(baseObject):
    def __init__(self, x, y, speed, maxBullets, imagePath,turretImagePath = 'images\\playerTurret.png' ) -> None:
        super().__init__(x,y,40, 40, speed, imagePath)
        self.maxBullets = maxBullets
        self.maxMines = 0
        self.currentMines = 0
        self.currentBullets = 0
        self.turretImage = None
        self.turretLoadedImage = None
        self.turretImagePath = turretImagePath
        self.xOkay = True
        self.yOkay = True
        self.efdx = self.dx
        self.efdy = self.dy
        self.timeSinceLastFire = 1.5
        self.timeSinceLastMine = 1
        self.fireDelay = .1
        self.mineDelay = 1
    def fire(self,dx,dy):
        if(self.currentBullets < self.maxBullets):
            magnitude = math.sqrt(dx**2+dy**2)
            dx/=magnitude
            dy/=magnitude
            newBullet = bullet(self.x+dx*40,self.y+dy*40,dx,dy,self)
            self.currentBullets += 1
            return newBullet
        return None
    def bulletDestroyed(self):
        self.currentBullets -= 1
    def mineDestroyed(self):
        self.currentMines -= 1
    def layMine(self,app):
        if(self.currentMines < self.maxMines and self.timeSinceLastMine > self.mineDelay and self.checkMines(app,self.getPos())):
            x,y = cellToLocation(locationToCell(self.getPos()))
            newMine = mine(x,y,self)
            self.currentMines +=1
            self.timeSinceLastMine = 0
            return newMine
        return None

    def move(self,relativeSpeed,layoutSet):
        self.layoutOkay(layoutSet)
        if((self.x>60 or self.dx > 0) and (self.x<960-60 or self.dx < 0) and self.xOkay):
            self.x += self.dx * relativeSpeed
            self.efdx = self.dx
        else:
            self.efdx = 0
        if((self.y>60 or self.dy > 0) and (self.y<720-60 or self.dy < 0) and self.yOkay):
            self.y += self.dy * relativeSpeed
            self.efdy = self.dy
        else:
            self.efdy = 0
    def layoutOkay(self,layoutSet):
        self.xOkay,self.yOkay = True,True
        i,j = locationToCell(self.getPos())
        check = [(i+1,j),(i-1,j),(i,j+1),(i,j-1),(i+1,j+1),(i+1,j-1),(i-1,j-1),(i-1,j+1)]
        for cell in check:
            if cell in layoutSet:
                wx,wy = cellToLocation(cell)
                if((self.y<wy+35 and self.y > wy-35) and abs(self.x-wx) < 40):#Within Y bounds
                    if (self.x>wx and self.dx < 0) or (self.x<wx and self.dx > 0):
                        self.xOkay = False
                if((self.x<wx+35 and self.x > wx-35) and abs(self.y-wy) < 40):#Within X bounds
                    if (self.y>wy and self.dy < 0) or (self.y<wy and self.dy > 0):
                        self.yOkay = False

    def initImage(self, app):
        self.loadedImage = app.scaleImage(app.loadImage(self.imagePath),1/5.75)
        self.image = self.loadedImage
        self.turretLoadedImage = app.scaleImage(app.loadImage(self.turretImagePath),1/5.75)
        self.turretImage = self.turretLoadedImage
    def rotateTurretImage(self,theta):
        theta = self.toDegrees(theta)
        self.turretImage = self.turretLoadedImage.rotate(angle=theta, resample = Image.Resampling.BILINEAR)
    def rotateImage(self):
        theta = self.toDegrees(math.atan2(self.efdx,self.efdy) + math.pi)
        self.image = self.loadedImage.rotate(angle=theta, resample = Image.Resampling.BILINEAR)
    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_image(self.x,self.y,image = ImageTk.PhotoImage(self.turretImage))
    def explode(self,app):
        app.currentExplosions[self.getPos()] = (0,app.explosion)


class bullet(baseObject):
    def __init__(self, x, y,dx,dy,creator) -> None:
        super().__init__(x,y,8,8,speed=400,imagePath='images\\bullet.png')
        self.hyp = math.sqrt(dx**2+dy**2)
        self.dx,self.dy = dx/self.hyp,dy/self.hyp
        self.creator = creator
        self.ricochetCount = 0
    def destroyBullet(self):
        self.creator.bulletDestroyed()
    def draw(self, canvas):
        canvas.create_image(self.x,self.y,image = ImageTk.PhotoImage(self.image))
    def ricochet(self):
        self.ricochetCount += 1
        if(self.ricochetCount > 1):
            self.destroyBullet()
            return True
        self.rotateImage()
        return False
    def initImage(self,app):
        self.loadedImage = app.bulletPNG
        self.image = self.loadedImage
        self.rotateImage()
    def explode(self,app):
        app.currentExplosions[self.getPos()] = (0,app.bulletExplosion)

class fastBullet(bullet):
    def __init__(self, x, y, dx, dy, creator) -> None:
        super().__init__(x, y, dx, dy, creator)
        self.imagePath = 'images\\fastBullet.png'
        self.speed = 800
        self.ricochetCount = 1
    def initImage(self,app):
        self.loadedImage = app.fastBulletPNG
        self.image = self.loadedImage
        self.rotateImage()


class mine(baseObject):
    def __init__(self, x, y, creator) -> None:
        super().__init__(x, y, 40, 40, 0, '')
        self.creator = creator
        self.active = False
        self.spawnTime = time.time()
        self.timeToActive = 2
        self.lifespan = 12
    def initImage(self,app):
        self.image = app.mineImage
        self.activeImage = app.activeMineImage
    def draw(self, canvas):
        if (self.active):
            canvas.create_image(self.x,self.y,image = self.activeImage)
        else:
            canvas.create_image(self.x,self.y,image = self.image)
    def destroyMine(self,app):
        self.creator.mineDestroyed()
        app.currentMines.remove(self)
    def explode(self,app):
        for tank in app.enemyTanks:
            tX,tY = tank.getPos()
            distance = math.sqrt((self.x-tX)**2+(self.y-tY)**2)
            if distance < 60:
                app.enemyTanks.remove(tank)
                tank.explode(app)
        tX,tY = app.player.getPos()
        distance = math.sqrt((self.x-tX)**2+(self.y-tY)**2)
        if distance < 60:
            hitTaken(app)

        #destroy any destroyable walls around 
        i,j = locationToCell((self.x,self.y))
        around = [(i+1,j),(i-1,j),(i,j+1),(i,j-1),(i+1,j+1),(i+1,j-1),(i-1,j-1),(i-1,j+1)]
        for cell in around:
            if cell in app.currentDestroyableWalls:
                destroyWall(app,cell)

        app.currentExplosions[self.getPos()] = (0,app.mineExplosion)
        self.destroyMine(app)
    def activateMine(self):
        if(time.time() - self.spawnTime > self.timeToActive):
            self.active = True
    def checkMineLife(self,app):
        if time.time()-self.spawnTime > self.lifespan:
            self.explode(app)