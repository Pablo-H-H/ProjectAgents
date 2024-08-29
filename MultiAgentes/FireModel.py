import imports_to_use as imports_to_use
from imports_to_use import *

from ReadLevel import ReadLevel
from FireBehaviours import smokePlace
from FireFighters import FireFighter

class fireModel(Model):
    def __init__(self,file,W,H,numAgents):
        super().__init__()
        self.height = W
        self.width = H
        self.grid = MultiGrid(self.width,self.height,torus=False)
        self.schedule = BaseScheduler(self)
        self.walls, self.points, self.smoke = ReadLevel(filename=file)
        self.datacollector = DataCollector(model_reporters={"Grid":get_grid})

        self.mapCoords = [(x,y) for x in range(self.width) for y in range(self.height)]

        for i in range(numAgents):
            agent = FireFighter(i,self)
            self.schedule.add(agent)


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        smokePlace(self)


def get_grid():
    grid = []

file = "./TestLevel.txt"
