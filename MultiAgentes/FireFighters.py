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

    def reveal_point(self):
        x, y = self.pos
        self.model.points[y][x] = 0
        if self.model.points[y][x] == 1:
            print(f"Se encontro víctima en ({x}, {y})")
        elif self.model.points[y][x] == 2:
            print(f"Se encontro falsa alarma en ({x}, {y})")

    def open_door(self):
        self.action_points -= 1
        x, y = self.pos

    def take_person(self):
        self.carrying_victim = True
        x, y = self.pos
        self.model.points[y][x] = 0
        self.action_points -= 1
        print(f"Bombero {self.unique_id} ha tomado una persona en ({x}, {y})")

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
        respawn_points_of_interest(self.model)

    def find_target(self):
        points = []
        for i in range(self.model.height):
            for j in range(self.model.width):
                if self.model.points[i][j] == 1:
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

        # Reconstrucción del camino desde el nodo final
        path = []
        step = end
        while step is not None:
            path.append(step)
            step = predecessors[step]
        
        # Devuelve el camino en orden correcto (de inicio a fin)
        path.reverse()
        return path

    def step(self):
        self.otherTargets = self.getTargets()
        while self.action_points > 0:
            if self.unique_id <= 2:
                self.target = self.find_target()
                self.dijkstra(self.model.graph, self.pos, self.target)
            else:
                pass