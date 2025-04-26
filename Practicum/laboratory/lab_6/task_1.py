import numpy as np
import string


def analyze_numbers(lst: list) -> tuple:
    smallest, largest, total, avg = [None for _ in range(4)]
    if len(lst) > 0:
        smallest = min(lst)
        largest = max(lst)
        total = sum(lst)
        avg = np.mean(lst)
    return (smallest, largest, total, avg)


def char_frequency(text: str) -> dict:
    freq = {}
    lower_text = text.lower()
    punctuation = set(string.punctuation)
    
    for ch in lower_text:
        if ch.isspace() or ch in punctuation:
            continue
        freq[ch] = freq.get(ch, 0) + 1
    
    return freq


def filter_long_words(words: list, min_length: int=5) -> list:
    result = []
    for word in words:
        if len(word) > min_length:
            result.append(word)

    return result