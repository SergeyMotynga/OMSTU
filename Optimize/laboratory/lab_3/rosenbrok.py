from dichotomy_search import dichotomy
import numpy as np


def line_minimization_dichotomy(func, x, direction, search_range=5.0, tol=1e-2):
    # Одномерная минимизация вдоль direction с помощью метода дихотомии
    f_line = lambda alpha: func(x + alpha * direction)
    alpha_opt = dichotomy(f_line, -search_range, search_range, tol)
    return x + alpha_opt * direction

def rosenbrock_method(func, x0, tol=1e-5, max_iter=100):
    n = len(x0)
    directions = np.eye(n)  # начальный ортонормированный базис
    x = np.copy(x0)

    for _ in range(max_iter):
        x_start = np.copy(x)

        # Проход по всем направлениям
        for i in range(n):
            direction = directions[i]
            x = line_minimization_dichotomy(func, x, direction)

        # Обновление направлений
        delta = x - x_start
        if np.linalg.norm(delta) < tol:
            break

        directions = np.roll(directions, -1, axis=0)
        directions[-1] = delta / np.linalg.norm(delta)
        x = line_minimization_dichotomy(func, x, directions[-1])

        if np.linalg.norm(x - x_start) < tol:
            break

    return x, func(x)