import random
import numpy as np

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