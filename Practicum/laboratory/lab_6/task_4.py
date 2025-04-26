import time
from functools import wraps

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function '{func.__name__}' took {end - start:.6f} seconds")
        return result
    return wrapper


def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = args + tuple(sorted(kwargs.items()))
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper