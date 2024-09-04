import MultiAgentes.imports_to_use as imports_to_use
from MultiAgentes.imports_to_use import *
def respawn_points_of_interest(model):
    points_count = np.sum(model.points == 1) + np.sum(model.points == 2)

    while points_count < 3:
        available_positions = [(x, y) for x in range(model.width) for y in range(model.height) if model.smoke[y][x] == 0 and model.points[y][x] == 0]
        
        if available_positions:
            new_x, new_y = random.choice(available_positions)
            # Decide aleatoriamente si es una víctima real o una falsa alarma
            model.points[new_y][new_x] = random.choice([1, 2])
            points_count += 1
            print(f"Nuevo punto de interés en ({new_x}, {new_y})")
        else:
            # Si no hay lugares sin fuego, coloca en lugares con fuego
            available_positions = [(x, y) for x in range(model.width) for y in range(model.height) if model.points[y][x] == 0]
            if available_positions:
                new_x, new_y = random.choice(available_positions)
                model.points[new_y][new_x] = random.choice([1, 2])
                points_count += 1
                print(f"Nuevo punto de interés en un lugar con fuego en ({new_x}, {new_y})")
            else:
                print("No hay espacios disponibles para colocar un nuevo punto de interés.")
                break