from functools import reduce
import math
from sympy import isprime

def process_numbers(numbers):
    primes = filter(isprime, numbers)
    squares = map(lambda x: x * x, primes)
    return reduce(lambda acc, el: acc * el, squares, 1)


def find_palindromes(words):
    return list(filter(lambda w: w.lower() == w.lower()[::-1], words))