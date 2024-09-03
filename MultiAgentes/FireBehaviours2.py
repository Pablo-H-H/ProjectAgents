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
    if model.smoke[y][x] == 1:    
        model.index.append([x,y])
        model.size.append(2)
        model.ID.append(0)
    elif model.smoke[y][x] == 2:
        model.index.append([x,y])
        model.size.append(2)
        model.ID.append(1)

    neighbor = findNeighbor(model,x,y)

    # If smoke gets to 2 initiate possible flashpoint
    if model.smoke[y][x] == 2 and any(model.smoke[ny][nx] == 1 for nx, ny in neighbor):
        flashOver(model,x,y)
    # Otherwise if the neighbor is already a fire change to fire and initiate possible flashpoint
    elif model.smoke[y][x] == 1 and any(model.smoke[ny][nx] == 2 for nx, ny in neighbor):
        model.smoke[y][x] = 2    # Update to regular fire value
        model.index.append([x,y])
        model.size.append(2)
        model.ID.append(1)
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
    # print(f"Shockwave initiated at ({x}, {y})")

    dirX, dirY = nX[:], nY[:]
    dir = len(nX)

    # print(f"Wall in cell ({x},{y}) is {model.walls[y][x]}")
    if model.smoke[y][x] >= 2:
        for i in range(dir):
            if (dirX[i] is not None) and (dirY[i] is not None):
                # print(f"Checking direction {i} from ({x}, {y})")            
                wallStatus = model.walls[y][x][i]
                opposite = (i + 2) % 4  # Opposite direction of shockwave

                if wallStatus in [1,2]:
                    model.walls[y][x][i] += 1 # Damage or break walls around original explosion
                    model.index.append([x, y, i, model.walls[y][x][i].item()])
                    model.size.append(4)
                    model.ID.append(4)
                    if (0 <= x + dirX[i] < model.width) and (0 <= y + dirY[i] < model.height):
                        model.walls[y + dirY[i]][x + dirX[i]][opposite] += 1 # Destroy in opposite
                        model.index.append([x + dirX[i], y + dirY[i], opposite, model.walls[y + dirY[i]][x + dirX[i]][opposite].item()])
                        model.size.append(4)
                        model.ID.append(4)
                    #     print(f"{model.walls[y][x]}, {model.walls[y + dirY[i]][x + dirX[i]]}")
                    # print(f"Damaged wall at ({x}, {y}) in direction {i}")
                    dirX[i] = None
                    dirY[i] = None

                elif wallStatus == 4:
                    model.walls[y][x][i] = 3  # Destroy a closed door
                    model.index.append([x, y, i, 3])
                    model.size.append(4)
                    model.ID.append(4)
                    if (0 <= x + dirX[i] < model.width) and (0 <= y + dirY[i] < model.height):
                        model.walls[y + dirY[i]][x + dirX[i]][opposite] = 3 # Destroy in opposite
                        model.index.append([x + dirX[i], y + dirY[i], opposite, 3])
                        model.size.append(4)
                        model.ID.append(4)
                    #     print(f"{model.walls[y][x]}, {model.walls[y + dirY[i]][x + dirX[i]]}")
                    # print(f"Destroyed closed door at ({x}, {y}) in direction {i}")
                    dirX[i] = None
                    dirY[i] = None
                
                elif wallStatus == 5:
                    model.walls[y][x][i] = 3  # Destroy an open door but do not remove from explosion direction
                    model.index.append([x, y, i, 3])
                    model.size.append(4)
                    model.ID.append(4)
                    if (0 <= x + dirX[i] < model.width) and (0 <= y + dirY[i] < model.height):
                        model.walls[y + dirY[i]][x + dirX[i]][opposite] = 3 # Destroy in opposite
                        model.index.append([x + dirX[i], y + dirY[i], opposite, 3])
                        model.size.append(4)
                        model.ID.append(4)
                    #     print(f"{model.walls[y][x]}, {model.walls[y + dirY[i]][x + dirX[i]]}")
                    # print(f"Destroyed open door at ({x}, {y}) in direction {i}")

                if dirX[i] is not None and dirY[i] is not None:
                    newX, newY = x + dirX[i], y + dirY[i]
            
                    if (0 <= newX < model.width) and (0 <= newY < model.height):
                        if model.smoke[newY][newX] == 2:
                            # print(f"Propagating shockwave to ({newX}, {newY})")
                            tempDirX, tempDirY = [None]*4, [None]*4
                            tempDirX[i], tempDirY[i] = dirX[i], dirY[i]
                            # print(f"{tempDirX}, {tempDirY}")
                            shockWave(model, newX, newY, tempDirX, tempDirY)     # Continue shockwave if fire

                        elif model.smoke[newY][newX] in [0, 1]:
                            model.smoke[newY][newX] = 2
                            model.index.append([newX,newY])
                            model.size.append(2)
                            model.ID.append(1)
                            # print(f"Set fire at ({newX}, {newY})")
                            flashOver(model, newX, newY)

                        # else:
                        #     print(f"Out of bounds: ({newX},{newY})")

# Using BFS on the smoke group we 
def flashOver(model,posX,posY):
    # print(f"Initialized flashover at cell ({posX},{posY})")
    visited = [[False for x in range(model.width)] for y in range(model.height)]
    startX, startY = posX,posY
    q = [(startX,startY)]
    while q:
        x,y = q.pop(0)
        if visited[y][x]:
            continue

        visited[y][x] = True

        if model.smoke[y][x] == 1:
            # print(f"Converted smoke at cell ({x},{y}) to fire")
            model.smoke[y][x] = 2
            model.index.append([x,y])
            model.size.append(2)
            model.ID.append(1)

        for i in range(4):
            newX, newY = x + dirH[i], y + dirV[i]
            if (0 <= newX < model.width and 0 <= newY < model.height) and (model.walls[y][x][i] in [0, 3, 5]):
                if model.smoke[y][x] == 1 and not visited[newY][newX]:
                    # print(f"Added cell ({newX},{newY}) to queue")
                    q.append((newX,newY))
            else: continue