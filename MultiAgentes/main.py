from MultiAgentes.ReadLevel import ReadLevel
from MultiAgentes.FireModel import fireModel
from MultiAgentes.toList import toList

file = "./TestLevel.txt"

model = fireModel(file,8,6,6)

# print(model.smoke)

while model.model_is_running:
    model.step()

dict = {
    "Grids" : model.combineGrids,
    "Index" : toList(model.index),
    "Size"  : model.size,
    "ID"    : model.ID
}

print(dict)
