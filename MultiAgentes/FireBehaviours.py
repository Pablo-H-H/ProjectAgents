import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *

def smokePlace(model):
    placement = [place for place in model.mapCoords if model.mapCoords <= 2]
    model.smoke[random.choice(placement)] += 1


def flashPoint(model):
    directions = [1, -1, -1, 1]
    if model.smoke == 3:
        for i in range(len(directions)):
            fireAdvance(model,directions[i])

def fireAdvance(model,dir):
    fire += 1