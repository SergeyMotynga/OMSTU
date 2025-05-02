


def fibonacci_search(f, a, b, tol):
    L0 = b - a
    # Генерируем числа Фибоначчи
    fib = [0, 1, 1]
    k = 2
    while fib[k] < L0 / tol:
        fib.append(fib[k] + fib[k-1])
        k += 1
    N = k - 1
    # Инициализация
    x1 = a + fib[N-1] / fib[N+1] * L0
    x2 = a + fib[N]   / fib[N+1] * L0
    f1, f2 = f(x1), f(x2)
    # Основной цикл
    for i in range(1, N-1):
        if f1 <= f2:
            b = x2
            x2, f2 = x1, f1
            x1 = a + fib[N-i-1] / fib[N+1] * L0
            f1 = f(x1)
        else:
            a = x1
            x1, f1 = x2, f2
            x2 = a + fib[N-i] / fib[N+1] * L0
            f2 = f(x2)
    x_opt = x1 if f1 < f2 else x2
    return x_opt