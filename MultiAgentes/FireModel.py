import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *

from MultiAgentes.ReadLevel import ReadLevel
from MultiAgentes.FireBehaviours import smokePlace
from MultiAgentes.FireFighters import FireFighter
from MultiAgentes.toList import toList

class fireModel(Model):
    def __init__(self,file,W,H,numAgents):
        super().__init__()
        self.height = H
        self.width = W
        self.grid = MultiGrid(self.width,self.height,torus=False)
        self.schedule = BaseScheduler(self)
        self.walls, self.points, self.smoke = ReadLevel(filename=file)
        self.datacollector = DataCollector(model_reporters={"Grid":get_grid})
        self.combineGrids = []
        self.index = []
        self.size = []
        self.ID = []
        self.cost_dict = {
            0: 0,  # No hay obstáculo
            1: 4,  # Pared
            2: 2,  # Pared dañada
            3: 0,  # Pared o puerta rota
            4: 1,  # Puerta cerrada
            5: 0,   # Puerta abierta
            6: 0   # Entrada
        }
        self.graph = []

        self.saved_victims = 0
        self.lost_victims = 0
        self.damage_markers = 0
        self.model_is_running = True
        self.points_marker = 3

        self.mapCoords = [(x,y) for x in range(self.width) for y in range(self.height)]


        for i in range(numAgents):
            start = [cell for cell in self.mapCoords if np.any(self.walls[cell[1]][cell[0]] == 6)]
            agent = FireFighter(i, self)
            self.grid.place_agent(agent,random.choice(start))
            self.schedule.add(agent)

        # Initialize array of walls for UNITY
        self.combineGrids.append(self.walls.tolist())
        self.index.append([6, 8, 4])
        self.size.append(3)
        self.ID.append(-1)

        # Initialize grid for UNITY
        self.combineGrids.append(get_grid(self).tolist())
        self.index.append([6, 8])
        self.size.append(2)
        self.ID.append(-2)

        self.combineGrids = toList(self.combineGrids)

    def get_wall_direction(self, current_node, neighbor):
            x, y = current_node
            nx, ny = neighbor

            if nx > x: return 3  # Derecha
            if nx < x: return 1  # Izquierda
            if ny > y: return 2  # Abajo
            if ny < y: return 0  # Arriba

    def create_graph(self):
        h, w = self.walls.shape[:2]  # Alto y ancho del modelo
        graph = {}

        for j in range(h):
            for i in range(w):
                current_node = (i, j)
                graph[current_node] = {}  # Initialize every node in the graph

                # Check neighbors and assign costs based on wall configuration
                if j > 0:  # Arriba (Up)
                    cost = self.cost_dict[self.walls[j][i][0]]  # Wall status at the top
                    if cost != float('inf'):
                        graph[current_node][(i, j - 1)] = cost
                if j < h - 1:  # Abajo (Down)
                    cost = self.cost_dict[self.walls[j][i][2]]  # Wall status at the bottom
                    if cost != float('inf'):
                        graph[current_node][(i, j + 1)] = cost
                if i > 0:  # Izquierda (Left)
                    cost = self.cost_dict[self.walls[j][i][1]]  # Wall status on the left
                    if cost != float('inf'):
                        graph[current_node][(i - 1, j)] = cost
                if i < w - 1:  # Derecha (Right)
                    cost = self.cost_dict[self.walls[j][i][3]]  # Wall status on the right
                    if cost != float('inf'):
                        graph[current_node][(i + 1, j)] = cost

        return graph

    
    
    def step(self):
        print(f"\n--- Step {self.schedule.steps + 1} ---")

        self.graph = self.create_graph()
        for agent in self.schedule.agents:
            agent.step()  # Cada bombero realiza su turno completo
            # Después de cada turno de un bombero, el mapa se actualiza
            smokePlace(self)
            self.graph = self.create_graph()
            # Verificar condiciones de victoria y derrota
            if self.saved_victims >= 7:
                print("¡Victoria! Se han rescatado suficientes víctimas.")
                self.model_is_running = False
                break 
            elif self.lost_victims >= 4 or self.damage_markers >= 24:
                print("Derrota. El edificio ha colapsado o se han perdido demasiadas víctimas.")
                self.model_is_running = False
                break

        print(f"Estado después del Step {self.schedule.steps + 1}:")
        print(f"Víctimas rescatadas: {self.saved_victims}")
        print(f"Víctimas perdidas: {self.lost_victims}")
        print(f"Marcadores de daño: {self.damage_markers}")

        self.schedule.steps += 1


def get_grid(model):
    grid = np.zeros((model.height, model.width), dtype=int)

    for y in range(model.height):
        for x in range(model.width):
            if model.smoke[y][x] == 1:
                grid[y][x] = 1  # Smoke
            elif model.smoke[y][x] == 2:
                grid[y][x] = 2  # Fire

    for agent in model.schedule.agents:
        x, y = agent.pos
        grid[y][x] = 3  # Bombero

    for y in range(model.height):
        for x in range(model.width):
            if model.points[y][x] == 1:
                grid[y][x] = 4  # Victim
            elif model.points[y][x] == 2:
                grid[y][x] = 5  # False Alarm

    return grid

file = "./TestLevel.txt"
