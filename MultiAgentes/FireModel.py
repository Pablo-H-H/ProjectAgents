import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *

from MultiAgentes.ReadLevel import ReadLevel
from MultiAgentes.FireBehaviours import smokePlace
from MultiAgentes.FireFighters import FireFighter
from MultiAgentes.toList import toList

from MultiAgentes.Graph import create_graph

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

        self.saved_victims = 0
        self.lost_victims = 0
        self.damage_markers = 0
        self.model_is_running = True
        self.points_marker = 3

        # Initialize array of walls for UNITY
        self.combineGrids.append(self.walls.tolist())
        self.index.append([6, 8, 4])
        self.size.append(3)
        self.ID.append(-1)
        self.cost_dict = {
            0: 0,  # No hay obstáculo
            1: 4,  # Pared
            2: 2,  # Pared dañada
            4: 3,  # Puerta cerrada
            5: 0,   # Puerta abierta
            6: 4   # Entrada
        }

        # self.combineGrids.append(self.grid)
        # self.index.append([6, 8])
        # self.size.append(2)
        # self.ID.append(-2)

        self.combineGrids = toList(self.combineGrids)

        # print(f"Grids: {self.combineGrids}")
        # print(f"Index: {self.index}")
        # print(f"Size: {self.size}")
        # print(f"ID: {self.ID}")

        self.mapCoords = [(x,y) for x in range(self.width) for y in range(self.height)]

        for i in range(numAgents):
            start = [cell for cell in self.mapCoords if np.any(self.walls[cell[1]][cell[0]] == 6)]
            agent = FireFighter(i, self)
            self.grid.place_agent(agent,random.choice(start))
            self.schedule.add(agent)

    def get_wall_direction(self, current_node, neighbor):
            x, y = current_node
            nx, ny = neighbor

            if nx > x: return 3  # Derecha
            if nx < x: return 1  # Izquierda
            if ny > y: return 2  # Abajo
            if ny < y: return 0  # Arriba
    def step(self):
        print(f"\n--- Step {self.schedule.steps + 1} ---")
        for agent in self.schedule.agents:
            agent.step()  # Cada bombero realiza su turno completo
            #create_graph(self.walls)
            if not self.model_is_running:
                break

            # Después de cada turno de un bombero, el mapa se actualiza
            smokePlace(self)
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

    def create_graph(walls):
        h, w = walls.shape[:2]
        graph = {}

        # Iterar sobre cada celda de la cuadrícula
        for i in range(h):
            for j in range(w):
                current_node = (i, j)
                graph[current_node] = {}

                # Revisar las celdas adyacentes (arriba, abajo, izquierda, derecha)
                if i > 0:  # Arriba
                    cost = cost_dict[walls[i][j][0]]
                    graph[current_node][(i-1, j)] = cost
                if i < h - 1:  # Abajo
                    cost = cost_dict[walls[i][j][2]]
                    graph[current_node][(i+1, j)] = cost
                if j > 0:  # Izquierda
                    cost = cost_dict[walls[i][j][3]]
                    graph[current_node][(i, j-1)] = cost
                if j < w - 1:  # Derecha
                    cost = cost_dict[walls[i][j][1]]
                    graph[current_node][(i, j+1)] = cost

        return graph


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
