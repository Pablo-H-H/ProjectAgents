from ReadLevel import ReadLevel
from FireModel import fireModel

file = "./TestLevel.txt"

model = fireModel(file,8,6,5)

print(model.smoke)

for i in range(10):
    model.step()
    print(model.smoke)
