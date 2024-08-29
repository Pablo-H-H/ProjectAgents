import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *
class FireFighter(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.action_points = 4
        self.carryng_victim = False
    def reveal_point(self):
        x, y = self.pos
        poi = self.model.PoI[x, y]
        if poi == 1:  # es una víctima
            print("Víctima encontrada en posición:", self.pos)
            self.save_people()
        elif poi == 2:  # es una falsa alarma
            print("Falsa alarma en posición:", self.pos)
            # Remover la falsa alarma del mapa
            self.model.PoI[x, y] = 0

    def open_door(self):
        self.action_points -= 1

    def save_people(self):
        self.action_points -= 2
        self.carryingvictim = True

    def remove_smoke(self):
        x, y = self.pos
        if self.model.smoke[x, y] == 1: 
            self.model.smoke[x, y] = 0
            self.action_points -= 1
            print("Humo removido en", self.pos)

    def flip_fire_to_smoke(self):
        x, y = self.pos
        if self.model.smoke[x, y] == 2:  
            self.model.smoke[x, y] = 1  
            self.action_points -= 1

    def extinguish_fire(self):
        x, y = self.pos
        if self.model.smoke[x, y] == 2: 
            self.model.smoke[x, y] = 0  
            self.action_points -= 2

    def damage_wall(self):
        self.action_points -= 1

    def chop_wall(self):
        self.action_points -= 2

    def move(self):
        dx, dy = direction
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        if self.model.grid.in_bounds(new_pos) and self.action_points > 0:
            self.pos = new_pos
            self.action_points -= 1  
            print("Bombero se movió a", new_pos)

    def step(self):
        # Obtener la posicion de los POI

        # Realizar movimiento hacia el POI mas cercano

        # Si hay un humo en la celda en el camino, removerlo

        # Si hay fuego en la celda en el camino, extinguirlo

        # Si en el camino a la victima es igual de costoso que romper una para para llegar a la victima, romper la pared

        # Revelar la celda

        # Si La celda revelada es una victima, salvarla

        # Si la celda revelada es una falsa alarma, obtener un nuevo POI