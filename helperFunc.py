def cellToLocation(cell):
    i,j = cell
    x = 20+40*(i+1)
    y = 20+40*(j+1)
    return (x,y)

def locationToCell(location):
    x,y = location
    i = (x-20)//40
    j = (y-20)//40
    return (i-1,j-1)
