from MultiAgentes.ReadLevel import ReadLevel
from MultiAgentes.FireModel import fireModel
from MultiAgentes.toList import toList

file = "./TestLevel.txt"

model = fireModel(file,8,6,6)

while model.model_is_running:
    model.step()
    print(f"PoI:\n {model.points}")

dict = {
    "Grids" : model.combineGrids,
    "Index" : toList(model.index),
    "Size"  : model.size,
    "ID"    : model.ID
}

print(dict)
