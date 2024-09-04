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

    def find_target(self):
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
        # Inicialización
        queue = []
        heapq.heappush(queue, (0, start))
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        predecessors = {node: None for node in graph}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            # Si llegamos al nodo final, terminamos
            if current_node == end:
                break

            # Si la distancia actual es mayor que la registrada, salte
            if current_distance > distances[current_node]:
                continue

            # Relajación de aristas
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                # Si encontramos un camino más corto al vecino
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # Si no se puede llegar al nodo final
        if end not in predecessors or predecessors[end] is None:
            print(f"No se puede encontrar un camino al nodo {end}")
            return []

        # Reconstrucción del camino desde el nodo final
        path = []
        step = end
        while step is not None:
            path.append(step)
            step = predecessors[step]

        # Devuelve el camino en orden correcto (de inicio a fin)
        path.reverse()
        return path

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
        """Guarda los puntos de acción restantes."""
        if self.action_points < 8:  # Máximo de AP permitidos
            self.action_points += remaining_ap
            if self.action_points > 8:  # Límite superior de AP
                self.action_points = 8


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
        elif self.model.smoke[next[1]][next[0]] == 2:
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
            return True  # Se movió correctamente

        return True  # Si se movió exitosamente



    def step(self):
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
                self.move(current, next)
            print(f"Bombero {self.unique_id} ha terminado su turno")
            print(f"Ha terminado su turno en ({self.pos[0]}, {self.pos[1]})")        
        else:
            pass