import numpy as np


def dichotomy(f, a: float=None, b: float=None, tol: float=1e-2):
    if np.abs(a - b) <= 2 * tol:
        return (a + b) / 2
    
    x_mid = (a + b) / 2
    x_1 = x_mid - tol / 2
    x_2 = x_mid + tol / 2

    f_1 = f(x_1)
    f_2 = f(x_2)

    if f_1 > f_2:
        return dichotomy(f, x_1, b, tol)
    else:
        return dichotomy(f, a, x_2, tol)