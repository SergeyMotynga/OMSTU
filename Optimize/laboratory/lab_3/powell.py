import numpy as np
from dichotomy_search import dichotomy

def powell(f, x0, tol=1e-4, max_iters=100, line_search_range=5.0):
    x = np.array(x0, dtype=float)
    n = x.size
    
    # Начальный набор направлений — стандартный базис
    directions = [np.eye(n)[i] for i in range(n)]
    
    for it in range(max_iters):
        x_start = x.copy()
        
        # 1) Последовательные одномерные минимизации вдоль текущих directions
        for i in range(n):
            d = directions[i]
            phi = lambda λ: f(x + λ*d)
            λ_opt = dichotomy(phi, -line_search_range, +line_search_range, tol)
            x = x + λ_opt * d
        
        # 2) Дополнительный шаг вдоль нового направления
        d_new = x - x_start
        if np.linalg.norm(d_new) < tol:
            break
        
        # одномерный поиск вдоль d_new
        phi = lambda λ: f(x + λ*d_new)
        λ_opt = dichotomy(phi, -line_search_range, +line_search_range, tol)
        x = x + λ_opt * d_new
        
        # 3) Обновляем систему направлений:
        #    выкидываем самое «слабое» (первое) и добавляем d_new в конец
        directions.pop(0)
        directions.append(d_new / np.linalg.norm(d_new))
        
        # 4) Критерий останова: шаг между циклами
        if np.linalg.norm(x - x_start) < tol:
            break
    
    return x, f(x)

# Пример использования на вашей f(x,y):
A, a_, b, c, d, r = 30, 2, 2, 1, 2, 3
def func2d(X):
    x, y = X
    term = ((x - a_)**2 / c**2 - 
            2*r*(x - a_)*(x - b)/(c*d) + 
            (x - b)**2 / d**2)
    return A - np.exp(-term/(10 - r**2))

x0 = (0.0, 0.0)
xmin, fmin = powell(func2d, x0, tol=1e-3, max_iters=50)
print("x* =", xmin, "f(x*) =", fmin)
