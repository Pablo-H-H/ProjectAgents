import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *
class FireFighter(Agent):
    def __init__(self, unique_id, model, pos, energy):
        super().__init__(unique_id, model)
        self.pos = pos
        self.energy = energy
    def reveal_point():
        pass
    def save_people(self):
        self.energy -= 2
    def remove_smoke(self):
        pass
    def extinguish_fire(self):
        pass
    def damage_the_wall(self):
        pass
    def brake_wall(self):
        pass
    def move(self):
        x, y = self.pos
        possible_movement = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        options = (i for i in range(len(possible_movement)))
        
    def step(self):
        #condition to stop the agent

        #condition to move the agent
        if self.energy <= 0:
            self.model.schedule.remove(self)
        else:
            self.move()
            if self.energy <= 4:
                self.save_people()
        #if in the way there is a wall, the agent will brake it

        #if in the way there is a person, the agent will save it