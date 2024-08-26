from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import BaseScheduler

import random

from ReadLevel import ReadLevel
from FireBehaviours import smokePlace, fireAdvance

class fireModel(Model):
    def __init__(self,file,W,H,numAgents):
        super().__init__()
        self.height = W
        self.width = H
        self.grid = SingleGrid(self.width,self.height,torus=False)
        self.schedule = BaseScheduler(self)
        self.walls, self.points, self.smoke = ReadLevel(filename=file)
        self.datacollector = DataCollector(model_reporters={"Grid":get_grid})

        self.mapCoords = [(x,y) for x in range(self.width) for y in range(self.height)]

        for i in range(numAgents):
            agent = fireAgent(i,self)
            self.schedule.add(agent)


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        smokePlace(self)
        fireAdvance(self)


def get_grid():
    grid = []

file = "./TestLevel.txt"
