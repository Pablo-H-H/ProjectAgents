from ReadLevel import ReadLevel
from FireModel import fireModel
from toList import toList

file = "./TestLevel.txt"

model = fireModel(file,8,6,5)

# print(model.smoke)

for i in range(10):
    model.step()
    # print(model.smoke)

dict = {
    "Grids" : model.combineGrids,
    "Index" : toList(model.index),
    "Size"  : model.size,
    "ID"    : model.ID
}

print(dict)
