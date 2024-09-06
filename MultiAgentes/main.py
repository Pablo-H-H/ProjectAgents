from MultiAgentes.ReadLevel import ReadLevel
from MultiAgentes.FireModel import fireModel
from MultiAgentes.toList import toList
from MultiAgentes.imports_to_use import *

file = "./TestLevel.txt"

FRAMES = 0
model = fireModel(file,8,6,6)

while model.model_is_running:
    model.step()
    print(f"PoI:\n {model.points}")
    FRAMES += 1

dict = {
    "Grids" : model.combineGrids,
    "Index" : toList(model.index),
    "Size"  : model.size,
    "ID"    : model.ID
}

model_grids = model.datacollector.get_model_vars_dataframe()

fig, axs = plt.subplots(figsize = (3,3))
axs.set_xticks([])
axs.set_yticks([])
AgentLoc = plt.imshow(model_grids.iloc[0][0],cmap = plt.cm.tab20)

def animate(i):
    AgentLoc.set_data(model_grids.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames = FRAMES)

anim.save("Visualization.gif")
