import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *
class FireFighter(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.action_points = 4
        self.carryng_victim = False
    def reveal_point():
        pass

    def open_door(self):
        self.action_points -= 1

    def save_people(self):
        self.action_points -= 2
        self.carryngvictim = True

    def remove_smoke(self):
        self.action_points -= 1

    def flip_fire_to_smoke(self):
        self.action_points -= 1

    def extinguish_fire(self):
        self.action_points -= 2

    def damage_wall(self):
        self.action_points -= 1

    #Add 1 damage market 
    def chop_wall(self):
        self.action_points -= 2

    def move(self):
        x, y = self.pos
        possible_movement = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

    def step(self):
        pass