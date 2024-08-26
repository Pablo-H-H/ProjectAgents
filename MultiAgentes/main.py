from ReadLevel import ReadLevel
from FireModel import fireModel

file = "./TestLevel.txt"
walls, PoI, smoke = ReadLevel(file)
print(PoI)