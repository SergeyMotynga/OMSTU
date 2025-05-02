from math import sqrt


def golden_search(f, a, b, tol):
    tau = (sqrt(5) - 1) / 2
    x1 = b - tau * (b - a)
    x2 = a + tau * (b - a)
    f1, f2 = f(x1), f(x2)
    
    while (b - a) > tol:
        if f1 > f2:
            a = x1
            x1, f1 = x2, f2
            x2 = a + tau * (b - a)
            f2 = f(x2)
        else:
            b = x2
            x2, f2 = x1, f1
            x1 = b - tau * (b - a)
            f1 = f(x1)
    
    return (a + b) / 2