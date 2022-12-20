import timeit
print(timeit.timeit('locationToCell((100,100))',number=10000, globals=globals()))

def locationToCell(location):
    x,y = location
    i = int((x-20)/40 +.499)
    j = int((y-20)/40 +.499)
    return (i-1,j-1)

def doShit():
    tankPos = set()
    for tank in enemyTanks:
        tankPos.add(locationToCell(tank.getPos()))