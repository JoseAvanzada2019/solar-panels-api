import itertools
from ortools.sat.python import cp_model

def fit_panels_in_rectangular_roof(
        big_rectangle_width: int, 
        big_rectangle_height: int,
        small_rectangle_width: int, 
        small_rectangle_height: int
    ):
    
    model = cp_model.CpModel()

    # Variables de decisión
    x_vars = {}
    y_vars = {}
    for i in range(big_rectangle_width):
        for j in range(big_rectangle_height):
            x_vars[(i, j)] = model.NewBoolVar(f'x_{i}_{j}') #existe un vértice superior izquierdo de rectangulo horizontal
            y_vars[(i, j)] = model.NewBoolVar(f'y_{i}_{j}') #existe un vértice superior izquierdo de rectangulo vertical

    for i in range(big_rectangle_width):
        for j in range(big_rectangle_height):
            if i + small_rectangle_width <= big_rectangle_width and j + small_rectangle_height <= big_rectangle_height:
                model.Add(sum(x_vars[(i + di, j + dj)] for di in range(small_rectangle_width) for dj in range(small_rectangle_height)) +
                        sum(y_vars[(i + dj, j + di)] for di in range(small_rectangle_height) for dj in range(small_rectangle_width)) <= 1)
    # Constraint to ensure no rectangles extend beyond the boundaries of the big rectangle
    for i in range(big_rectangle_width):
        for j in range(big_rectangle_height):
            if i + small_rectangle_width > big_rectangle_width or j + small_rectangle_height > big_rectangle_height:
                model.Add(x_vars[(i, j)] == 0)
            if i + small_rectangle_height > big_rectangle_width or j + small_rectangle_width > big_rectangle_height:
                model.Add(y_vars[(i, j)] == 0)

    
    # Función objetivo: Maximizar el número total de rectángulos colocados
    objective = sum(x_vars[(i, j)] for i in range(big_rectangle_width) for j in range(big_rectangle_height)) \
          + sum(y_vars[(i, k)] for i in range(big_rectangle_width) for k in range(big_rectangle_height))
    model.Maximize(objective)

    # Resolver el modelo
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Obtener la disposición óptima de los rectángulos pequeños
    arrangement = []
    if status == cp_model.OPTIMAL:
        for i in range(big_rectangle_width):
            for j in range(big_rectangle_height):
                if solver.Value(y_vars[(i, j)]):
                    arrangement.append({'x': i, 'y': j, 'width': small_rectangle_height, 'height': small_rectangle_width})
                if solver.Value(x_vars[(i, j)]):
                    arrangement.append({'x': i, 'y': j, 'width': small_rectangle_width, 'height': small_rectangle_height})
        return len(arrangement), arrangement
    else:
        return None, None