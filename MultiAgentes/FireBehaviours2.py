import imports_to_use as imports_to_use
from imports_to_use import *

def smokePlace(model):
    global dirH, dirV
    dirH = [0, -1, 0, 1]
    dirV = [-1, 0, 1, 0]

    placement = [place for place in model.mapCoords if model.smoke[place[1]][place[0]] <= 2]
    (x,y) = random.choice(placement)
    print((x,y))
    model.smoke[y][x] += 1

    neighbor = findNeighbor(model,x,y)

    # If smoke gets to 2 initiate possible flashpoint
    if model.smoke[y][x] == 2 and any(model.smoke[ny][nx] == 1 for nx, ny in neighbor):
        flashOver(model,x,y)
    # Otherwise if the neighbor is already a fire change to fire and initiate possible flashpoint
    elif model.smoke[y][x] == 1 and any(model.smoke[ny][nx] == 2 for nx, ny in neighbor):
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
        if (0 <= newX < model.width) and (0 <= newY < model.height):
            if model.walls[newY][newX][i] in [0, 3, 5]:
                neighbor.append((newX,newY))
    return neighbor

# Recursive shockwave function.
# For each direction it checks if there is something blocking (wall or closed door) and damages it.
# If there is a direction that has a wall that direction is removed from the list of directions
# Next cell is only passed on one of the directions to continue recursive function.
def shockWave(model,x,y,nX,nY):
    print(f"Shockwave initiated at ({x}, {y})")

    dirX, dirY = nX, nY
    dir = len(nX)

    print(f"Wall in cell ({x},{y}) is {model.walls[y][x]}")
    # I need to do something here that can recognize which direction the wall is even if dir is not of length 4.
    if model.smoke[y][x] >= 2:
        for i in range(dir):
            if (dirX[i] != None) and (dirY[i] != None):
                print(f"Checking direction {i} from ({x}, {y})")            
                wallStatus = model.walls[y][x][i]
                if wallStatus in [1,2]:
                    model.walls[y][x][i] += 1 # Damage or break walls around original explosion
                    print(f"Damaged wall at ({x}, {y}) in direction {i}")
                    print(model.walls[y][x])
                    dirX[i] = None
                    dirY[i] = None

                elif wallStatus == 4:
                    model.walls[y][x][i] = 3  # Destroy a closed door
                    print(f"Destroyed closed door at ({x}, {y}) in direction {i}")
                    print(model.walls[y][x])
                    dirX[i] = None
                    dirY[i] = None
                
                elif wallStatus == 5:
                    model.walls[y][x][i] = 3  # Destroy an open door but do not remove from explosion direction
                    print(f"Destroyed open door at ({x}, {y}) in direction {i}")
                    print(model.walls[y][x])

                if dirX[i] != None and dirY[i] != None:
                    newX, newY = x + dirX[i], y + dirY[i]
                else:
                    newX, newY = x, y
            
                if (0 <= newX < model.width) and (0 <= newY < model.height) and ((newX, newY) != (x, y)):
                    if model.smoke[newY][newX] == 2:
                        print(f"Propagating shockwave to ({newX}, {newY})")
                        tempDirX, tempDirY = [None]*4, [None]*4
                        tempDirX[i], tempDirY[i] = dirX[i], dirY[i]
                        print(f"{tempDirX}, {tempDirY}")
                        shockWave(model, newX, newY, tempDirX, tempDirY)     # Continue shockwave if fire
                    elif model.smoke[newY][newX] in [0, 1]:
                        model.smoke[newY][newX] = 2
                        print(f"Set fire at ({newX}, {newY})")
                    else:
                        print(f"Out of bounds: ({newX},{newY})")

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