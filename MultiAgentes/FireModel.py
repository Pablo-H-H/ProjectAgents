import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *

from MultiAgentes.ReadLevel import ReadLevel
from MultiAgentes.FireBehaviours import smokePlace
from MultiAgentes.FireFighters import FireFighter
from MultiAgentes.toList import toList

class fireModel(Model):
    def __init__(self,file,W,H,numAgents):
        super().__init__()
        self.height = H
        self.width = W
        self.grid = MultiGrid(self.width,self.height,torus=False)
        self.schedule = BaseScheduler(self)
        self.walls, self.points, self.smoke = ReadLevel(filename=file)
        self.datacollector = DataCollector(model_reporters={"Grid":get_grid})
        self.combineGrids = []
        self.index = []
        self.size = []
        self.ID = []

        # Initialize array of walls for UNITY
        self.combineGrids.append(self.walls.tolist())
        self.index.append([6, 8, 4])
        self.size.append(3)
        self.ID.append(-1)

        # self.combineGrids.append(self.grid)
        # self.index.append([6, 8])
        # self.size.append(2)
        # self.ID.append(-2)

        self.combineGrids = toList(self.combineGrids)

        # print(f"Grids: {self.combineGrids}")
        # print(f"Index: {self.index}")
        # print(f"Size: {self.size}")
        # print(f"ID: {self.ID}")

        self.mapCoords = [(x,y) for x in range(self.width) for y in range(self.height)]

        for i in range(numAgents):
            start = [cell for cell in self.mapCoords if np.any(self.walls[cell[1]][cell[0]] == 6)]
            pos = random.choice(start)
            agent = FireFighter(i,self,pos)
            self.schedule.add(agent)


    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
        smokePlace(self)
        # self.index = toList(self.index)
        # print(f"Index: {self.index}")
        # print(f"Size: {self.size}")
        # print(f"ID: {self.ID}")


def get_grid():
    grid = []

file = "./TestLevel.txt"
