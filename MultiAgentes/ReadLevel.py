""" Function to read a text file for a level
    Returns 3 matrices corresponding to the walls/doors in the level,
    the points of interest, and the fire points (in said order)
 """

import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *

def ReadLevel(filename):
    w, h = 8,6
    gameFile = open(filename,'r')
    content = gameFile.read()
    gameFile.close()

    """ Wall has characteristics:
     0 = No wall at that point
     1 = Wall exists at that point
     2 = Wall is damaged
     3 = Wall or door is broken
     4 = Closed door
     5 = Open door
     6 = Entryway
     Wall uses [top, left, bottom, right] """
    # Walls initialization
    temp = content.splitlines()[0:6]
    for i in range(len(temp)):
        temp[i] = temp[i].split()
        for j in range(len(temp[i])):
            temp[i][j] = [int(x) for x in temp[i][j]]
    walls = np.array(temp)

    # Doors initialization
    temp = content.splitlines()[19:27]
    for i in range(len(temp)):
        temp[i] = temp[i].split()
        coords = [[int(x) for x in pair] for pair in temp[i]]
        x1, y1, x2, y2 = coords[0][0], coords[1][0], coords[2][0], coords[3][0]
        if 0 < x1 <= h and 0 < x2 <= h and 0 < y1 <= w and 0 < y2 <= w:
            if x1 < x2:
                walls[x1-1][y1-1][2] = 4
                walls[x2-1][y2-1][0] = 4
            elif y1 < y2:
                walls[x1-1][y1-1][3] = 4
                walls[x2-1][y2-1][1] = 4

    # Entryways initialization
    temp = content.splitlines()[27:31]
    for i in range(len(temp)):
        temp[i] = temp[i].split()
        x, y = int(temp[i][0][0]), int(temp[i][1][0])
        if y == 1:
            walls[x-1][y-1][1] = 6
        elif y == 8:
            walls[x-1][y-1][3] = 6
        elif x == 1:
            walls[x-1][y-1][0] = 6
        elif x == 6:
            walls[x-1][y-1][2] = 6

    """ PoI has characteristics:
     0 = nothing there
     1 = victim
     2 = false alarm """
    temp = content.splitlines()[6:9]
    PoI = np.zeros((h, w), dtype=int)
    for i in range(len(temp)):
        temp[i] = temp[i].split()
        x, y = int(temp[i][0][0]), int(temp[i][1][0])
        if temp[i][2] == 'v':
            PoI[x-1, y-1] = 1
        else:
            PoI[x-1, y-1] = 2

    """ Fire has characteristics:
     0 = nothing there
     1 = smoke placed on cell
     2 = fire on cell
     3 = initialize flash point explosion """
    temp = content.splitlines()[9:19]
    fires = np.zeros((h, w), dtype=int)
    for i in range(len(temp)):
        temp[i] = temp[i].split()
        x, y = int(temp[i][0][0]), int(temp[i][1][0])
        fires[x-1, y-1] = 2
    
    return walls, PoI, fires