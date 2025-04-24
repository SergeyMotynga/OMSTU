from bitarray import bitarray

class BloomsFilter:
    def __init__(self, m: int, k: int) -> None:
        '''
        m - размер битового массива;
        k - количество хэш-функций.
        '''
        self.m = m
        self.k = k
        self.array = bitarray(self.m)
        self.array.setall(0)
    
    def _hash(self, item: object) -> list:
        '''
        Вычисляет k хэш-функций при помощи двойного хеширования.
        '''
        item_str = str(item)
        h1 = hash(item_str)
        h2 = hash(item_str + item_str[:len(item_str) // 2 + 1])
        return [(h1 + i * h2) % self.m for i in range(self.k)]
    
    def add(self, item: object) -> None:
        '''
        Добавляет элемент в фильтр.
        '''
        for i in self._hash(item):
            self.array[i] = 1

    def __contains__(self, item: object) -> bool:
        '''
        Проверяет, содержит ли элемент в фильтре.
        '''
        return all(self.array[i] for i in self._hash(item))
    
    def union(self, other: "BloomsFilter") -> "BloomsFilter":
        """
        Объединяет два Bloom-фильтра (логическое ИЛИ).
        """
        if self.m != other.m or self.k != other.k:
            raise ValueError("Размеры массивов и количество хеш-функций должны совпадать")
        result = BloomsFilter(self.m, self.k)
        result.array = self.array | other.array
        return result

    def intersection(self, other: "BloomsFilter") -> "BloomsFilter":
        """
        Пересечение двух Bloom-фильтров (логическое И).
        """
        if self.m != other.m or self.k != other.k:
            raise ValueError("Размеры массивов и количество хеш-функций должны совпадать")
        result = BloomsFilter(self.m, self.k)
        result.array = self.array & other.array 
        return result