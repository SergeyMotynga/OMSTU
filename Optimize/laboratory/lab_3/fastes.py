import numpy as np
from dichotomy_search import dichotomy

def steepest_descent(f, x0, tol=1e-4, max_iters=100, line_search_range=5.0, grad_eps=1e-6):
    def numerical_grad(x):
        # Вычисление градиента методом центральных разностей
        n = x.size
        grad = np.zeros(n, dtype=float)
        for i in range(n):
            x_forward = x.copy()
            x_backward = x.copy()
            x_forward[i] += grad_eps
            x_backward[i] -= grad_eps
            grad[i] = (f(x_forward) - f(x_backward)) / (2 * grad_eps)
        return grad

    x = np.array(x0, dtype=float)
    
    for k in range(max_iters):
        # Вычисляем градиент в текущей точке
        g = numerical_grad(x)
        grad_norm = np.linalg.norm(g)
        
        # Условие остановки
        if grad_norm < tol:
            break
        
        # Направление наискорейшего спуска
        direction = -g
        
        # Одномерный поиск шага
        phi = lambda alpha: f(x + alpha * direction)
        alpha_opt = dichotomy(phi, -line_search_range, line_search_range, tol)
        
        # Обновление точки
        x = x + alpha_opt * direction
    
    return x, f(x)
