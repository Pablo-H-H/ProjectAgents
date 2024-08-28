import imports_to_use as imports_to_use
from imports_to_use import *

def smokePlace(model):
    global dirH, dirV
    dirH = [0, -1, 0, 1]
    dirV = [1, 0, -1, 0]

    placement = [place for place in model.mapCoords if model.mapCoords <= 2]
    loc = random.choice(placement)
    model.smoke[loc] += 1

    neighbor = findNeighbor(model,loc)

    # If smoke gets to 2 initiate possible flashpoint
    if model.smoke[loc] == 2 and model.smoke[neighbor] == 1:
        flashOver(model,loc)
    # Otherwise if the neighbor is already a fire change to fire and initiate possible flashpoint
    elif model.smoke[loc] == 1 and model.smoke[neighbor] == 2:
        model.smoke[loc] = 2    # Update to regular fire value
        flashOver(model,loc)

    # If smoke gets to 3 initiate explosion/shockwave
    if model.smoke[loc] >= 3:
        shockWave(model,loc,dirH,dirV)
        model.smoke[loc] = 2    # Update to regular fire value


def findNeighbor(model,loc):
    x, y = loc[0], loc[1]
    neighbor = []
    for i in range(4):
        if model.walls[x][y][i] == 0 or model.walls[x][y][i] == 3 or model.walls[x][y][i] == 5:
            neighbor.append((x,y))
    
    return neighbor

# Recursive shockwave function.
# For each direction it checks if there is something blocking (wall or closed door) and damages it.
# If there is a direction that has a wall that direction is removed from the list of directions
# Next cell is only passed on one of the directions to continue recursive function.
def shockWave(model,loc,dirX,dirY):
    x, y = loc[0], loc[1]
    dir = len(dirX)

    # I need to do something here that can recognize which direction the wall is even if dir is not of length 4.
    # if model.smoke == 3:
        # for i in range(4):
        #     if model.walls[x][y][i] > 0 or model.walls[x][y][i] <= 2:
        #         model.walls[x][y][i] += 1 # Damage or break walls around original explosion
        #         dir -= 1
        #         dirX.pop(i)
        #         dirY.pop(i)

        #     elif model.walls[x][y][i] == 4:
        #         model.walls[x][y][i] = 3  # Destroy a closed door
        #         dir -= 1
        #         dirX.pop(i)
        #         dirY.pop(i)
            
        #     elif model.walls[x][y][i] == 5:
        #         model.walls[x][y][i] = 3  # Destroy an open door but do not remove from explosion direction

    if range(dir) != 0:    
        for i in range(dir):
            newLoc = loc + (dirX[i], dirY[i])
            if model.smoke[newLoc] == 2:
                shockWave(model, newLoc, dirX[i], dirY[i])     # Continue shockwave if fire
            else:
                model.smoke[newLoc] = 2
    return 0

# Using BFS on the smoke group we 
def flashOver(model,loc):
    visited = [[False for x in range(model.width)] for y in range(model.height)]
    startX, startY = loc[0], loc[1]
    q = [(startX,startY)]
    smokeGroup = []

    while q:
        x,y = q.pop(0)
        if visited[x][y]:
            continue

        visited[x][y] = True
        smokeGroup.append((x,y))
        model.smokes[x][y] += 1

        for i in range(4):
            newX, newY = x + dirH[i], y + dirV[i]
            if (model.walls[x][y][i] == 0 or model.walls[x][y][i] == 3 or model.walls[x][y][i] == 5) and model.smokes == 1:
                if not visited[newX][newY]:
                    q.append((newX,newY))
            else: continue