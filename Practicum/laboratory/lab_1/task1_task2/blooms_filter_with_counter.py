from collections import Counter
from blooms_filter import BloomsFilter

class CountingBloomsFilter(BloomsFilter):
    def __init__(self, m: int, k: int) -> None:
        self.m = m
        self.k = k
        self.array = [0] * m

    def add(self, item: object) -> None:
        """
        Добавляет элемент в фильтр, увеличивая счётчик для каждой позиции.
        """
        for i in self._hash(item):
            self.array[i] += 1

    def remove(self, item: object) -> None:
        """
        Удаляет элемент из фильтра, уменьшая счётчик для каждой позиции.
        """
        indices = self._hash(item)
        counts = Counter(indices)
        if all(self.array[i] >= count for i, count in counts.items()):
            for i, count in counts.items():
                self.array[i] -= count

    def __contains__(self, item: object) -> bool:
        """
        Элемент считается присутствующим, если на всех позициях, полученных хэш-функциями,
        значение счётчика больше или равно количеству раз, которое индекс встречается.
        """
        indices = self._hash(item)
        counts = Counter(indices)
        return all(self.array[i] >= count for i, count in counts.items())