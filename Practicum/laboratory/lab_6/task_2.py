

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError(f"Ожидалось неотрицательное число, получили {n}")
    
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


def fibonachi(n: int) -> int:
    if n in (0, 1):
        return 1
    return fibonachi(n-2) + fibonachi(n-1)

def reverse_str(s: str, i: int = None) -> str:
    if i is None:
        i = len(s) - 1
    if i < 0:
        return ""
    return s[i] + reverse_str(s, i - 1)