import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *
from MultiAgentes.RespawnPoints import respawn_points_of_interest
import heapq

class FireFighter(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.action_points = 4
        self.saved_ap = 0
        self.endTurn = False
        self.carrying_victim = False
        self.target = None
        self.otherTargets = []
        self.way = []

    def start_turn(self):
        self.endTurn = False
        self.action_points = min(4 + self.saved_ap, 8)
        self.saved_ap = 0

    def add_points(self, remaining_ap):
        # Guarda los puntos de acción restantes, hasta un máximo de 8.
        self.saved_ap = remaining_ap
    
    def deductAP(self, points):
        self.action_points = max(self.action_points - points, 0)
        if self.action_points == 0:
            self.endTurn = True

    def getTargets(self):
        otherTargets = []
        for agent in self.model.schedule.agents:
            if agent.unique_id != self.unique_id:
                otherTargets.append(agent.target)
        return otherTargets

    def find_target(self): #### Fix this function
        if self.carrying_victim:
            return self.find_nearest_exit() # Busca la salida más cercana
        else:
            points = []
            for i in range(self.model.height):
                for j in range(self.model.width):
                    if self.model.points[i][j] == 1 or self.model.points[i][j] == 2:
                        points.append((j, i))
            points = [_ for _ in points if _ not in self.otherTargets]

            if not points:
                print(f"NO TARGETS FOUND")
                return None

            point = random.choice(points)
            return point
    
    def dijkstra(self, graph, start, end):  #### Check this function for correctness
        if start == end:
            return [start]
        
        queue = []
        heapq.heappush(queue, (0, start))
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        predecessors = {node: None for node in graph}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node].items():
                if neighbor not in distances:
                    continue  # Skip if neighbor is not in graph

                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        path = []
        step = end
        while step is not None:
            path.append(step)
            step = predecessors[step]

        if not path or distances[end] == float('inf'):
            print(f"No se encontró un camino hacia {end}")
            return []
        
        return path[::-1]

    def find_nearest_smoke_or_fire(self):
        nearest_fire = None
        min_distance = float('inf')
        current_position = self.pos

        # Iterar sobre toda la grid para encontrar humo (1) o fuego (2)
        for i in range(self.model.height):
            for j in range(self.model.width):
                if self.model.smoke[i][j] == 1 or self.model.smoke[i][j] == 2:
                    distance = abs(current_position[0] - j) + abs(current_position[1] - i)  # Distancia Manhattan
                    if distance < min_distance:
                        min_distance = distance
                        nearest_fire = (j, i)
        return nearest_fire

# La función devuelva si hay una pared o puerta cerrada y que tipo de elemento en paredes hay
    def is_wall_in_direction(self, current, dir):
        x, y = current
        if self.model.walls[y][x][dir] in [1,2,4]:
            return True, self.model.walls[y][x][dir]

        return False, 0
    
    def find_nearest_exit(self):    #### Check this function for correctness
        exits = []
        for i in range(self.model.height):
            for j in range(self.model.width):
                # Usar np.any() para verificar si alguno de los valores en la celda es 6 (la salida)
                if any(self.model.walls[i][j] == 6):  # Supongamos que la salida tiene un valor de 6
                    exits.append((j, i))
        
        if not exits:
            print(f"NO EXITS")
            return None

        # Usar Dijkstra para encontrar la salida más cercana
        nearest_exit = None
        min_distance = float('inf')
        for exit in exits:
            path = self.dijkstra(self.model.graph, self.pos, exit)
            if path and len(path) < min_distance:
                nearest_exit = exit
                min_distance = len(path)
        
        if nearest_exit is None:
            print(f"NO EXITS FOUND")

        return nearest_exit

    def extinguish(self, fireX, fireY):
        if (self.model.smoke[fireY][fireX] == 1) and (self.action_points >= 1):
            self.deductAP(1)
            self.model.smoke[fireY][fireX] = 0
            print(f"Extinguishing smoke at ({fireX},{fireY}), now with fire as {self.model.smoke[fireY][fireX]}")

            self.model.index.append([fireX,fireY])
            self.model.size.append(2)
            self.model.ID.append(3)

        elif (self.model.smoke[fireY][fireX] == 2) and (self.action_points >= 2):
            self.deductAP(2)
            self.model.smoke[fireY][fireX] = 0
            print(f"Extinguishing fire at ({fireX},{fireY}), now with fire as {self.model.smoke[fireY][fireX]}")

            self.model.index.append([fireX,fireY])
            self.model.size.append(2)
            self.model.ID.append(3)

        else:
            self.endTurn = True
            print(f"Not enough AP to extinguish ({self.action_points})")

    def chopWall(self, posX, posY, dir):
        wall = self.model.walls[posY][posX][dir]
        if wall == 1 and (self.action_points >= 4):
            self.deductAP(4)
            self.model.walls[posY][posX][dir] = 3
            print(f"Destroying wall at ({posX},{posY}) in direction {dir}")

            self.model.damage_markers += 2

            self.model.index.append(self.unique_id)
            self.model.size.append(1)
            self.model.ID.append(6)

            self.model.index.append([posX, posY, dir, 3])
            self.model.size.append(4)
            self.model.ID.append(4)
        elif wall == 2 and (self.action_points >= 2):
            self.deductAP(2)
            self.model.walls[posY][posX][dir] = 3
            print(f"Destroying damaged wall at ({posX},{posY}) in direction {dir}")
            
            self.model.damage_markers += 1

            self.model.index.append(self.unique_id)
            self.model.size.append(1)
            self.model.ID.append(6)

            self.model.index.append([posX, posY, dir, 3])
            self.model.size.append(4)
            self.model.ID.append(4)

        else:
            self.endTurn = True
            print(f"Not enough AP to chop wall ({self.action_points})")
    
    def openDoor(self, posX, posY, dir):
        if self.action_points >= 1:
            self.deductAP(1)
            self.model.walls[posY][posX][dir] = 5
            print(f"Opening door at ({posX},{posY}) in direction {dir}")

            self.model.index.append(self.unique_id)
            self.model.size.append(1)
            self.model.ID.append(6)

            self.model.index.append([posX, posY, dir, 5])
            self.model.size.append(4)
            self.model.ID.append(4)
        else:
            self.endTurn = True
            print(f"Not enough AP to open door ({self.action_points})")

    def interact(self, current, next, dir):
        wallInDir, wallStatus = self.is_wall_in_direction(current, dir)

        if wallInDir:
            if ((wallStatus == 1) and (self.action_points >= 4)) or ((wallStatus == 2) and (self.action_points >= 2)):
                self.chopWall(current[0], current[1], dir)
                return True

            elif (wallStatus == 4) and (self.action_points >= 1):
                self.openDoor(current[0], current[1], dir)
                return True
            else:
                self.endTurn = True
                return False

        if ((self.model.smoke[next[1]][next[0]] == 1) and (self.action_points >= 1)) or ((self.model.smoke[next[1]][next[0]] == 2) and (self.action_points >= 2)):
            self.extinguish(next[0], next[1])
            return True
        else:
            return False
    
    def moveToNext(self, current, next):
        print(f"Firefighter {self.unique_id} moved from {self.pos} to ({next[0]}, {next[1]})")
        self.model.grid.move_agent(self,next)
        self.deductAP(1)

        # Update movement tracking for Unity
        self.model.index.append([next[0], next[1], self.unique_id])
        self.model.size.append(3)
        self.model.ID.append(2)

    def move(self, current, next):
        if current == next:
            print(f"Firefighter {self.unique_id} tried moving in own cell")
            return

        dir = 0 # Up direction
        if current[0] > next[0]: # Left direction
            dir = 1
        elif current[1] < next[1]: # Down direction
            dir = 2
        elif current[0] < next[0]: # Right direction
            dir = 3

        if self.interact(current, next, dir):
            if self.action_points > 0:
                self.moveToNext(current, next)
        elif not self.endTurn:
            self.moveToNext(current, next)
        else:
            self.endTurn = True
            print(f"Firefighter ending turn")

        if self.action_points <= 0: # End turn if action points are 0 or lower (shouldn't be lower but just in case)
            self.action_points = 0
            self.endTurn = True
            print(f"Firefighter {self.unique_id} has no more AP. Turn ending.")
    
    def step(self):
        self.start_turn()
        self.otherTargets = self.getTargets()

        # Check if target is still there before start of turn
        if self.target != None:
            if (not self.carrying_victim) and (self.model.points[self.target[1]][self.target[0]] == 0):
                self.target = None
        
        if self.unique_id <= 2: # These agents will save victims in the map
            if self.target == None:
                self.target = self.find_target()
            self.way = self.dijkstra(self.model.graph, self.pos, self.target)

            print(f"Firefighter {self.unique_id} at ({self.pos[0]},{self.pos[1]}) headed to ({self.target[0]},{self.target[1]})")
            print(f"Route: {self.way}")
            print(f"AP: {self.action_points}")

            while not self.endTurn: # Move around and save victims while model is running
                if not self.way:
                    if self.target == None:
                        self.target = self.find_target()
                    self.way = self.dijkstra(self.model.graph, self.pos, self.target)
                    print(f"Path for firefighter {self.unique_id} recalculated as {self.way}")
                
                next = self.way.pop(0)
                self.move(self.pos, next)

                # Condition that if the agent reaches target
                if self.pos == self.target:
                    if self.carrying_victim: # If agent is at the exit, drop victim
                        self.carrying_victim = False
                        self.model.saved_victims += 1
                        print(f"Firefighter {self.unique_id} has saved someone! Current saved is {self.model.saved_victims}")
                        self.model.points_marker -= 1
                        respawn_points_of_interest(self.model)

                        # Dejar de cargar la victima
                        self.model.index.append(self.unique_id)
                        self.model.size.append(1)
                        self.model.ID.append(5)
                
                    # Else interact with a PoI
                    elif not self.carrying_victim:
                        if self.model.points[self.pos[1]][self.pos[0]] == 1: # If is a victim carry
                            print(f"Firefighter {self.unique_id} has picked up a victim at {self.pos}")
                            self.carrying_victim = True
                            self.model.points[self.pos[1]][self.pos[0]] = 0
                            
                            # Descrubir punto de interes
                            self.model.index.append([self.pos[0],self.pos[1]])
                            self.model.size.append(2)
                            self.model.ID.append(9)

                            # Eliminar el punto en el modelo UNITY
                            self.model.index.append(self.unique_id)
                            self.model.size.append(1)
                            self.model.ID.append(5)

                            # Cargar a la victima
                            self.model.index.append(self.unique_id)
                            self.model.size.append(1)
                            self.model.ID.append(5)

                        elif self.model.points[self.pos[1]][self.pos[0]] == 2: # Otherwise FA and replenish
                            self.model.points[self.pos[1]][self.pos[0]] = 0
                            self.model.points_marker -= 1
                            respawn_points_of_interest(self.model)

                            # Eliminar el punto en el modelo UNITY
                            self.model.index.append(self.unique_id)
                            self.model.size.append(1)
                            self.model.ID.append(5)

                    self.target = None
                    self.way = []

                if not self.way:
                    if self.target == None:
                        self.target = self.find_target()
                    self.way = self.dijkstra(self.model.graph, self.pos, self.target)
            
            # When finishing the turn add points and make the agent clear it's current status
            self.add_points(self.action_points)
            self.way = []
            print(f"Turn of firefighter {self.unique_id} ended")

        else: # These agents will only extinguish fire
            self.target = self.find_nearest_smoke_or_fire()
            self.way = self.dijkstra(self.model.graph, self.pos, self.target)
            print(f"Firefighter {self.unique_id} at ({self.pos[0]},{self.pos[1]}) headed to ({self.target[0]},{self.target[1]})")
            print(f"Route: {self.way}")
            print(f"AP: {self.action_points}")

            while not self.endTurn:
                if not self.way:
                    self.target = self.find_nearest_smoke_or_fire()
                    self.way = self.dijkstra(self.model.graph, self.pos, self.target)
                    print(f"Path for firefigher {self.unique_id} recalculated is {self.way}")

                next = self.way.pop(0)

                if (next[0], next[1]) == (self.target[0], self.target[1]):
                    self.extinguish(next[0], next[1])
                    if self.action_points > 0:
                        self.target = self.find_nearest_smoke_or_fire()
                        self.way = self.dijkstra(self.model.graph, self.pos, self.target)
                    else:
                        self.action_points = 0
                        self.endTurn = True
                else:
                    self.move(self.pos, next)
                
                if self.action_points <= 0:
                    self.action_points = 0
                    self.endTurn = True

            # Finish turn of firefighter
            self.add_points(self.action_points)
            self.target = None
            self.way = []
            print(f"Turn of firefighter {self.unique_id} ended")