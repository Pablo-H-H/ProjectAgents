import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *

def smokePlace(model):
    placement = [place for place in model.mapCoords if model.mapCoords <= 2]
    loc = random.choice(placement)
    model.smoke[loc] += 1
    neighbor = 0

    # If smoke gets to 2 initiate possible flashpoint
    if model.smoke[loc] == 2 and model.smoke[neighbor] == 1:
        flashOver(model,loc)
    # Otherwise if the neighbor is already a fire change to fire and initiate possible flashpoint
    elif model.smoke[loc] == 1 and model.smoke[neighbor] == 2:
        model.smoke[loc] = 2    # Update to regular fire value
        flashOver(model,loc)

    # If smoke gets to 3 initiate explosion/shockwave
    if model.smoke[loc] >= 3:
        shockWave(model,loc)
        model.smoke[loc] = 2    # Update to regular fire value


def shockWave(model,loc):
    # All possible directions for fire to travel in
    directions = 4
    directionsX = [0, -1, 0, 1]
    directionsY = [1, 0, -1, 0]
    

    if model.smoke == 3:
        for i in range(directions):
            if model.walls[loc[0]][loc[1]][i] > 0 or model.walls[loc[0]][loc[1]][i] <= 2:
                model.walls[loc[0]][loc[1]][i] += 1 # Damage or break walls around original explosion
                directions -= 1
                directionsX.pop(i)
                directionsY.pop(i)

            elif model.walls[loc[0]][loc[1]][i] == 4:
                model.walls[loc[0]][loc[1]][i] = 3  # Destroy a closed door
                directions -= 1
                directionsX.pop(i)
                directionsY.pop(i)
            
            elif model.walls[loc[0]][loc[1]][i] == 5:
                model.walls[loc[0]][loc[1]][i] = 3  # Destroy an open door but do not remove from explosion direction
            
        for i in range(directions):
            if model.smoke[loc + (directionsX[i], directionsY[i])] == 2:
                shockAdvance(model,loc,(directionsX[i], directionsY[i]))    # Continue shockwave if fire
            else:
                model.smoke[loc + (directionsX[i], directionsY[i])] = 2

def shockAdvance(model,origin,dir): # This should be approx the same as above
    return 0

def flashOver(model,loc):
    # Probably best to use a simple BFS to target all the cells that are connected
    visited = [[False for x in range(model.width)] for y in range(model.height)]
    startX, startY = loc[0], loc[1]
    q = [(startX,startY)]
    group = []
    dirH = [1, 0, 0, -1]
    dirV = [0, 1, -1, 0]

    while q:
        x,y = q.pop(0)
        if visited[x][y]:
            continue

        visited[x][y] = True