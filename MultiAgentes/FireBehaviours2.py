import imports_to_use as imports_to_use
from imports_to_use import *

def smokePlace(model):
    global dirH, dirV
    dirH = [0, -1, 0, 1]
    dirV = [1, 0, -1, 0]

    placement = [place for place in model.mapCoords if model.smoke[place[1]][place[0]] <= 2]
    (x,y) = random.choice(placement)
    print((x,y))
    model.smoke[y][x] += 1

    neighbor = findNeighbor(model,x,y)

    # If smoke gets to 2 initiate possible flashpoint
    if model.smoke[y][x] == 2 and np.any(model.smoke[neighbor] == 1):
        flashOver(model,x,y)
    # Otherwise if the neighbor is already a fire change to fire and initiate possible flashpoint
    elif model.smoke[y][x] == 1 and np.any(model.smoke[neighbor] == 2):
        model.smoke[y][x] = 2    # Update to regular fire value
        flashOver(model,x,y)

    # If smoke gets to 3 initiate explosion/shockwave
    if model.smoke[y][x] >= 3:
        shockWave(model,x,y,dirH,dirV)
        model.smoke[y][x] = 2    # Update to regular fire value


def findNeighbor(model,x,y):
    neighbor = []
    for i in range(4):
        newX, newY = x + dirH[i], y + dirV[i]
        if model.walls[newY][newX][i] == 0 or model.walls[newY][newX][i] == 3 or model.walls[newY][newX][i] == 5:
            neighbor.append((newX,newY))
    return neighbor

# Recursive shockwave function.
# For each direction it checks if there is something blocking (wall or closed door) and damages it.
# If there is a direction that has a wall that direction is removed from the list of directions
# Next cell is only passed on one of the directions to continue recursive function.
def shockWave(model,x,y,dirH,dirV):
    dirX = dirH
    dirY = dirV

    dir = len(dirX)

    # I need to do something here that can recognize which direction the wall is even if dir is not of length 4.
    if model.smoke[y][x] == 3:
        for i in range(dir):
            if model.walls[y][x][i] > 0 or model.walls[y][x][i] <= 2:
                model.walls[y][x][i] += 1 # Damage or break walls around original explosion
                dir -= 1
                dirX[i] = None
                dirY[i] = None

            elif model.walls[y][x][i] == 4:
                model.walls[y][x][i] = 3  # Destroy a closed door
                dirX[i] = None
                dirY[i] = None
            
            elif model.walls[y][x][i] == 5:
                model.walls[y][x][i] = 3  # Destroy an open door but do not remove from explosion direction

 
    for i in range(dir):
        if dirX[i] != None and dirY[i] != None:
            newLoc = (x,y) + (dirX[i], dirY[i])
            if model.smoke[newLoc[1]][newLoc[0]] == 2:
                shockWave(model, newLoc[0], newLoc[1], dirX, dirY)     # Continue shockwave if fire
            else:
                model.smoke[newLoc] = 2
    return 0

# Using BFS on the smoke group we 
def flashOver(model,posX,posY):
    visited = [[False for x in range(model.width)] for y in range(model.height)]
    startX, startY = posX,posY
    q = [(startX,startY)]
    smokeGroup = []

    while q:
        x,y = q.pop(0)
        if visited[y][x]:
            continue

        visited[y][x] = True
        smokeGroup.append((x,y))
        if model.smoke[y][x] == 1 and (x,y) != (startX,startY):
            model.smoke[y][x] += 1

        for i in range(4):
            newX, newY = x + dirH[i], y + dirV[i]
            if (model.walls[y][x][i] == 0 or model.walls[y][x][i] == 3 or model.walls[y][x][i] == 5) and model.smoke[y][x] == 1:
                if not visited[newY][newX]:
                    q.append((newX,newY))
            else: continue