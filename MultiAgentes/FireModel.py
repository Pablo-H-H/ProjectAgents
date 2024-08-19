from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid

from ReadLevel import ReadLevel

class FireModel(Model):
    def __init__(self,file):
        super().__init__()
        self.height = 6
        self.width = 8
        self.grid = SingleGrid(self.width,self.height,torus=False)
        self.walls, self.points, self.smoke = ReadLevel(filename=file)

file = "./TestLevel.txt"
