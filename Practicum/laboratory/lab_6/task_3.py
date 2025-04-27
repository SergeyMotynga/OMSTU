def apply_twice(f, x: int):
    return f(f(x))

def custom_map(func, iterable):
    result = []
    for item in iterable:
        result.append(func(item))
    return result

def custom_filter(predicate, iterable, invert=False):
    result = []
    for item in iterable:
        keep = predicate(item)
        if invert:
            keep = not keep
        if keep:
            result.append(item)
    return result