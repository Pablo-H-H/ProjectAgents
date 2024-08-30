import imports_to_use as imports_to_use
from imports_to_use import *
class FireFighter(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.action_points = 4
        self.carrying_victim = False
    def reveal_point(self):
        x, y = self.pos
        # Verifies if the point is a victim or a false alarm
        if self.model.points[x][y] != 0:
            poi = self.model.points[x][y]
            if poi == 1:
                print("Victim found at", self.pos)
            elif poi == 2:
                print("False alarm at", self.pos)
                #Remove the false alarm from the grid
                self.model.points[x][y] = 0

    def open_door(self, door_position):
        if self.action_points >= 1:
            x, y = door_position

            # Determine the direction of the door
            direction = None
            if x == self.pos[0] - 1 and y == self.pos[1]:
                direction = 0  # Door at the north
            elif x == self.pos[0] and y == self.pos[1] - 1:
                direction = 1  # Door at the west
            elif x == self.pos[0] + 1 and y == self.pos[1]:
                direction = 2  # Door at the south
            elif x == self.pos[0] and y == self.pos[1] + 1:
                direction = 3  # Door at the east

            # Verify if the door is in the specified direction
            if direction is not None and self.model.walls[self.pos[0]][self.pos[1]][direction] == 4:
                # Change the state of the door (open/close)
                self.model.walls[self.pos[0]][self.pos[1]][direction] = 5 if self.model.walls[self.pos[0]][self.pos[1]][direction] == 4 else 4
                # Reflected the change in the adjacent cell
                if direction == 0:
                    self.model.walls[x][y][2] = 5 if self.model.walls[x][y][2] == 4 else 4
                elif direction == 1:
                    self.model.walls[x][y][3] = 5 if self.model.walls[x][y][3] == 4 else 4
                elif direction == 2:
                    self.model.walls[x][y][0] = 5 if self.model.walls[x][y][0] == 4 else 4
                elif direction == 3:
                    self.model.walls[x][y][1] = 5 if self.model.walls[x][y][1] == 4 else 4

                self.action_points -= 1  # Open/Close a door costs 1 AP
        

    def save_people(self):
        if self.action_points >= 2 and not self.carrying_victim:
            x, y = self.pos
            if self.model.points[x][y] == 1: # Verify if there is a victim in the cell
                self.model.points[x][y] = 0  # Remove the victim from the grid
                self.carrying_victim = True # Set the carrying_victim to True
                self.action_points -= 2 # Save a victim costs 2 AP
                print("Victim saved at", self.pos)

    def remove_smoke(self):
        if self.action_points >= 1:
            self.action_points -= 1

    def flip_fire_to_smoke(self):
        if self.action_points >= 1:
            self.action_points -= 1

    def extinguish_fire(self):
        if self.action_points >= 2:
            self.action_points -= 2

    def damage_wall(self):
        if self.action_points >= 2:
            self.action_points -=2

    def brake_wall(self):
        if self.action_points >= 4:
            self.action_points -= 4

    def move(self, new_position):
        move_cost = 1  
        
        # The move cost is 2 when there is a fire 
        if self.model.smoke[new_position] == 2:
            move_cost = 2

        if self.carrying_victim:
            # Move to a empty cell while carring_victim is true has the cost of 2 AP
            if self.model.smoke[new_position] == 0:
                move_cost = 2 
            # Move to a smoke cell while carring_victim is true 
            elif self.model.smoke[new_position] == 1:
                move_cost = 2
            # The firefighter can't move to a cell with fire while carring_victim is true
            elif self.model.smoke[new_position] == 2:
                move_cost = float('inf') 

        if self.action_points >= move_cost:
            self.model.grid.move_agent(self, new_position)
            self.action_points -= move_cost

    def step(self):
<<<<<<< HEAD
        pass
=======
        # Obtener la posicion de los POI

        # Realizar movimiento hacia el POI mas cercano

        # Si hay un humo en la celda en el camino, removerlo

        # Si hay fuego en la celda en el camino, extinguirlo

        # Si en el camino a la victima es igual de costoso que romper una para para llegar a la victima, romper la pared

        # Revelar la celda

        # Si La celda revelada es una victima, salvarla

        # Si la celda revelada es una falsa alarma, obtener un nuevo POI
        return 0
>>>>>>> ee4dc63621ae250c207bf8fee48435c8f6a9b7d7
