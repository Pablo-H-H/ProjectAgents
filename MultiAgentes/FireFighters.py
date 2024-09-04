import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *
class FireFighter(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.action_points = 4
        self.carrying_victim = False
        self.saved_ap = 0

    def reveal_point(self):
        pass

    def open_door(self):
        self.action_points -= 1

    def take_person(self):
        self.action_points -= 1
        self.carrying_victim = True

    def remove_smoke(self):
        x, y = self.pos
        self.model.smoke[y][x] = 0
        self.action_points -= 1
        print(f"Bombero {self.unique_id} eliminó humo en ({x}, {y})")

    def flip_fire_to_smoke(self):
        x, y = self.pos
        self.model.smoke[y][x] = 1
        self.action_points -= 1
        print(f"Bombero {self.unique_id} convirtió fuego a humo en ({x}, {y})")

    def extinguish_fire(self):
        x, y = self.pos
        self.model.smoke[y][x] = 0
        self.action_points -= 2
        print(f"Bombero {self.unique_id} apagó fuego en ({x}, {y})")

    def damage_wall(self):
        x, y = self.pos
        self.model.damage_markers += 1
        self.action_points -= 2

    def break_wall(self):
        x, y = self.pos
        self.model.damage_markers += 2
        self.action_points -= 2

    def save_person(self):
        x, y = self.pos
        self.carrying_victim = False
        print(f"Bombero {self.unique_id} a salvado a una persona ({x}, {y})")
        self.model.saved_victims += 1

    def move(self, new_position):
        pass

    def step(self):
      pass
        ##if self.carrying_victim
          #while self.action_points > 0:

        #elif self.carrying_victim:
          #while self.action_points > 0:
