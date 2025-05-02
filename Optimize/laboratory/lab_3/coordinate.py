import numpy as np
from dichotomy_search import dichotomy




# Метод покоординатного спуска (Гаусса-Зейделя)
def coordinate_descent(f, x0, tol=1e-3, max_iters=500, search_range=5):
    x, y = x0
    for k in range(max_iters):
        x_old, y_old = x, y
        
        # Поиск по x при фиксированном y
        f_x = lambda xx: f(xx, y)
        x = dichotomy(f_x, x - search_range, x + search_range, tol=1e-2)
        
        # Поиск по y при фиксированном x
        f_y = lambda yy: f(x, yy)
        y = dichotomy(f_y, y - search_range, y + search_range, tol=1e-2)
        
        # Условие остановки
        if np.hypot(x - x_old, y - y_old) < tol:
            break
    return (x, y, f(x,y))

