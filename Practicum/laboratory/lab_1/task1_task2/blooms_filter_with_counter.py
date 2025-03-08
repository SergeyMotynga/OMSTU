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
        for i in self._hash(item):
            if self.array[i] > 0:
                self.array[i] -= 1

    def __contains__(self, item: object) -> bool:
        """
        Элемент считается присутствующим, если на всех позициях, полученных хэш-функциями,
        значение счётчика больше нуля.
        """
        return all(self.array[i] > 0 for i in self._hash(item))
