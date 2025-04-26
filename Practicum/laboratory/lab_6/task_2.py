

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError(f"Ожидалось неотрицательное число, получили {n}")
    
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
