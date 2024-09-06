from MultiAgentes.ReadLevel import ReadLevel
from MultiAgentes.FireModel import fireModel
from MultiAgentes.toList import toList
from MultiAgentes.imports_to_use import *
from MultiAgentes.FireModel import Steps_Per_Game, Wins, Losses, Steps_Per_Win, Steps_Per_Loss


file = "./TestLevel.txt"

FRAMES = 0
Steps = []


MAX_ITERATIONS = 20
for i in range(MAX_ITERATIONS):
    model = fireModel(file,8,6,6)
    while model.model_is_running:
        model.step()
        print(f"PoI:\n {model.points}")
Steps_Per_Game2 = Steps_Per_Win
W = Wins
L = Losses
S = Steps_Per_Game
TotalWins = sum(W)
TotalLosses = sum(L)
AvgSteps = sum(S) / MAX_ITERATIONS
print(f"Total Wins: {TotalWins}")
print(f"Total Losses: {TotalLosses}")
print(f"Average Steps per Game: {AvgSteps}")

print("winrate: ", TotalWins / MAX_ITERATIONS)
print("lossrate: ", TotalLosses / MAX_ITERATIONS)
plt.figure(figsize=(15, 6))
plt.plot(range(1, TotalWins+ 1), Steps_Per_Game2, marker='o', label='Steps')
plt.xlabel('Simulación')
plt.ylabel('Número de Steps en Victorias')
plt.title('Steps por simulación')
plt.legend()
plt.grid(True)
plt.show()
plt.clf()