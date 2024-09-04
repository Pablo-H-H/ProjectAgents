import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *
from MultiAgentes.RespawnPoints import respawn_points_of_interest
import heapq
class FireFighter(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.action_points = 4
        self.carrying_victim = False
        self.saved_ap = 0
        self.target = None
        self.otherTargets = []
        self.way = []

    def start_turn(self):
        self.action_points = min(self.action_points + self.saved_ap, 8)
        self.saved_ap = 0

    def find_target(self):
        if self.carrying_victim:
            # Busca la salida más cercana
            return self.find_nearest_exit()
        else:
            points = []
            for i in range(self.model.height):
                for j in range(self.model.width):
                    if self.model.points[i][j] == 1 or self.model.points[i][j] == 2:
                        points.append((j, i))
            points = [_ for _ in points if _ not in self.otherTargets]
            point = random.choice(points)

            return point
    
    def getTargets(self):
        otherTargets = []
        for agent in self.model.schedule.agents:
            if agent.unique_id != self.unique_id:
                otherTargets.append(agent.target)
        return otherTargets
    
    def dijkstra(self, graph, start, end):
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


    def is_wall_in_direction(self, current, next):
        x1, y1 = current
        x2, y2 = next

        # Direcciones de movimiento
        if x1 < x2:  # Movimiento a la derecha
            return np.any(self.model.walls[y1][x1 + 1] == 1)
        elif x1 > x2:  # Movimiento a la izquierda
            return np.any(self.model.walls[y1][x1 - 1] == 1)
        elif y1 < y2:  # Movimiento hacia abajo
            return np.any(self.model.walls[y1 + 1][x1] == 1)
        elif y1 > y2:  # Movimiento hacia arriba
            return np.any(self.model.walls[y1 - 1][x1] == 1)

        return False

    
    def add_points(self, remaining_ap):
        """Guarda los puntos de acción restantes, hasta un máximo de 8."""
        self.saved_ap = remaining_ap
        if self.action_points < 8:
            self.action_points += self.saved_ap
            if self.action_points > 8:
                self.action_points = 8  # Límite superior de AP


    def is_a_damage_wall(self, current, next):
        x1, y1 = current
        x2, y2 = next
        
        if x1 < x2:  # Movement to the right
            if np.any(self.model.walls[y1][x1 + 1] == 3):
                return True
        elif x1 > x2:  # Movement to the left
            if np.any(self.model.walls[y1][x1 - 1] == 3):
                return True
        elif y1 < y2:  # Movement down
            if np.any(self.model.walls[y1 + 1][x1] == 3):
                return True
        elif y1 > y2:  # Movement up
            if np.any(self.model.walls[y1 - 1][x1] == 3):
                return True

        return False

    def is_a_closed_door(self, current, next):
        x1, y1 = current
        x2, y2 = next
        if x1 < x2:  # Movement to the right
            if np.any(self.model.walls[y1][x1 + 1] == 4):
                return True
        elif x1 > x2:  # Movement to the left
            if np.any(self.model.walls[y1][x1 - 1] == 4):
                return True
        elif y1 < y2:  # Movement down
            if np.any(self.model.walls[y1 + 1][x1] == 4):
                return True
        elif y1 > y2:  # Movement up
            if np.any(self.model.walls[y1 - 1][x1] == 4):
                return True

        return False
    
    def find_nearest_exit(self):
        exits = []
        for i in range(self.model.height):
            for j in range(self.model.width):
                # Usar np.any() para verificar si alguno de los valores en la celda es 6 (la salida)
                if np.any(self.model.walls[i][j] == 6):  # Supongamos que la salida tiene un valor de 6
                    exits.append((j, i))
        
        # Usar Dijkstra para encontrar la salida más cercana
        nearest_exit = None
        min_distance = float('inf')
        for exit in exits:
            path = self.dijkstra(self.model.graph, self.pos, exit)
            if path and len(path) < min_distance:
                nearest_exit = exit
                min_distance = len(path)
        
        return nearest_exit

    
    def move(self, current, next):
        # Verificar si hay una pared en la dirección del movimiento
        if self.is_wall_in_direction(current, next):
            # Si tiene suficientes puntos de acción para romper la pared
            if self.action_points >= 4:
                self.model.damage_markers += 2
                self.model.walls[current[1]][current[0]] = 0  # Romper la pared
                self.action_points -= 4
                print(f"Bombero {self.unique_id} ha roto una pared en ({current[0]}, {current[1]})")
            elif self.action_points >= 2:
                self.model.damage_markers += 1
                self.model.walls[current[1]][current[0]] = 3  # Dañar la pared
                self.action_points -= 2
                print(f"Bombero {self.unique_id} ha dañado una pared en ({current[0]}, {current[1]})")
            else:
                # No tiene suficientes puntos, guarda AP y termina el turno
                self.add_points(self.action_points)
                print(f"Bombero {self.unique_id} no tiene suficientes puntos de acción para romper la pared en ({current[0]}, {current[1]})")
                return False  # No pudo moverse

        # Si hay una puerta cerrada
        elif self.is_a_closed_door(current, next):
            if self.action_points >= 2:
                self.model.walls[current[1]][current[0]] = 5  # Abrir la puerta
                self.action_points -= 2
                print(f"Bombero {self.unique_id} ha abierto una puerta en ({current[0]}, {current[1]})")
                self.model.grid.move_agent(self, next)
            elif self.action_points >= 1:
                self.model.walls[current[1]][current[0]] = 5  # Abrir la puerta parcialmente
                self.action_points -= 1
                print(f"Bombero {self.unique_id} ha abierto parcialmente una puerta en ({current[0]}, {current[1]})")
            else:
                # No tiene suficientes puntos, guarda AP y termina el turno
                self.add_points(self.action_points)
                print(f"Bombero {self.unique_id} no tiene suficientes puntos de acción para abrir la puerta en ({current[0]}, {current[1]})")
                return False  # No pudo moverse
        
        # Si hay fuego
        if self.model.smoke[next[1]][next[0]] == 2:
            if self.action_points >= 3:
                self.model.grid.move_agent(self, next)  # Mover al bombero
                self.model.smoke[next[1]][next[0]] = 0  # Extinguir el fuego
                self.action_points -= 3
                print(f"Bombero {self.unique_id} ha apagado fuego en ({next[0]}, {next[1]})")
            else:
                self.add_points(self.action_points)
                return False  # No pudo moverse

        # Si hay humo
        elif self.model.smoke[next[1]][next[0]] == 1:
            if self.action_points >= 2:
                self.model.grid.move_agent(self, next)  # Mover al bombero
                self.model.smoke[next[1]][next[0]] = 0  # Eliminar el humo
                self.action_points -= 2
                print(f"Bombero {self.unique_id} ha eliminado humo en ({next[0]}, {next[1]})")
            else:
                self.add_points(self.action_points)
                return False  # No pudo moverse

        # Movimiento normal sin obstáculos
        else:
            self.model.grid.move_agent(self, next)  # Mover al bombero
            self.action_points -= 1  # Restar puntos de acción por moverse
        
        # Detectar si ha llegado a un punto de interés
        x, y = next
        if not self.carrying_victim and self.model.points[y][x] in [1, 2]:
            # Es un punto de interés
            if self.model.points[y][x] == 1:  # Es una víctima
                self.carrying_victim = True
                self.model.points[y][x] = 0  # Se elimina la víctima del mapa
                print(f"Bombero {self.unique_id} ha encontrado una víctima en ({x}, {y})")
            else:  # Es una falsa alarma
                self.model.points[y][x] = 0  # Se elimina la falsa alarma del mapa
                print(f"Bombero {self.unique_id} ha encontrado una falsa alarma en ({x}, {y})")
                respawn_points_of_interest(self.model)  # Generar un nuevo punto de interés
            return True

        # Detectar si ha llegado a una salida con una víctima
        if self.carrying_victim and self.model.walls[y][x] == 6:  # Suponemos que la salida es el valor 6
            self.carrying_victim = False
            self.model.saved_victims += 1
            print(f"Bombero {self.unique_id} ha rescatado una víctima en la salida ({x}, {y})")
            respawn_points_of_interest(self.model)  # Generar un nuevo punto de interés
            return True

        return True


    def find_nearest_smoke_or_fire(self):
        nearest_point = None
        min_distance = float('inf')
        current_position = self.pos

        # Iterar sobre toda la grid para encontrar humo (1) o fuego (2)
        for i in range(self.model.height):
            for j in range(self.model.width):
                if self.model.smoke[i][j] == 1 or self.model.smoke[i][j] == 2:
                    distance = abs(current_position[0] - j) + abs(current_position[1] - i)  # Distancia Manhattan
                    if distance < min_distance:
                        min_distance = distance
                        nearest_point = (j, i)
        
        return nearest_point

    def step(self):
        self.start_turn()
        print("El bombero este comenzando su turno en ({}, {})".format(self.pos[0], self.pos[1]))
        self.otherTargets = self.getTargets()
        if self.unique_id <= 2:
            self.target = self.find_target()
            self.way = self.dijkstra(self.model.graph, self.pos, self.target)
            print(f"Bombero {self.unique_id} se dirige a {self.target}")
            print(f"Camino: {self.way}")
            while self.action_points > 0 and self.way:
                current = self.pos
                next = self.way.pop(0)
                if not self.move(current, next):
                    break
            print(f"Ha terminado su turno en ({self.pos[0]}, {self.pos[1]})")       
        else:
            if self.action_points > 0:
                x, y = self.pos
                possible_moves = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                for move in possible_moves:
                    if self.is_wall_in_direction(self.pos, move):
                    # Si hay una pared, verifica si puede romperla o dañarla
                        if self.is_a_damage_wall(self.pos, move):
                            print(f"Bombero {self.unique_id} detectó una pared dañada en {move}")
                            continue  # Saltar el movimiento si es un muro dañado
                        elif self.is_a_closed_door(self.pos, move):
                            print(f"Bombero {self.unique_id} detectó una puerta cerrada en {move}")
                            continue  # Saltar si hay una puerta cerrada
                    else:
                        # Si no hay paredes, ni puertas cerradas
                        if self.action_points >= 3:  # Si tiene al menos 3 puntos de acción
                            if self.model.smoke[move[1]][move[0]] == 2:
                                # Si hay fuego, apaga el fuego
                                self.move(self.pos, move)  # Mover y apagar fuego
                                self.action_points -= 2
                                print(f"Bombero {self.unique_id} apagó fuego en {move}")
                            elif self.model.smoke[move[1]][move[0]] == 1:
                                # Si hay humo, elimina el humo
                                self.move(self.pos, move)  # Mover y eliminar humo
                                self.action_points -= 1
                                print(f"Bombero {self.unique_id} eliminó humo en {move}")
                            else:
                                # Movimiento normal sin obstáculos
                                self.move(self.pos, move)
                                self.action_points -= 1
                                print(f"Bombero {self.unique_id} se movió a {move}")

                    if self.action_points <= 0:
                        break  # Terminar el turno si no tiene más puntos de acción

            print(f"Ha terminado su turno en ({self.pos[0]}, {self.pos[1]})")
        if self.action_points > 0:
            self.add_points(self.action_points)