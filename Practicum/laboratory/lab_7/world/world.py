from plants.lumiere import Lumiere
from plants.obscurite import Obscurite
from plants.demi import Demi

from animals.pauvre import Pauvre
from animals.malheureux import Malheureux

import random

class Cell:
    def __init__(self):
        self.plant = None
        self.animal = None

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

        self.populate_initial()

    def populate_initial(self):
        # Заполним начальное состояние мира растениями и животными с небольшой плотностью
        for y in range(self.height):
            for x in range(self.width):
                r = random.random()
                if r < 0.1:
                    self.grid[y][x].plant = random.choice([Lumiere(), Obscurite(), Demi()])
                elif r < 0.15:
                    self.grid[y][x].animal = random.choice([Pauvre(), Malheureux()])

    def neighbors(self, x, y):
        # Возвращает координаты соседних клеток (вверх, вниз, влево, вправо)
        results = []
        if x > 0:
            results.append((x-1, y))
        if x < self.width - 1:
            results.append((x+1, y))
        if y > 0:
            results.append((x, y-1))
        if y < self.height - 1:
            results.append((x, y+1))
        return results

    def move_animal(self, from_x, from_y, to_x, to_y):
        from_cell = self.grid[from_y][from_x]
        to_cell = self.grid[to_y][to_x]

        if to_cell.animal is None:
            to_cell.animal = from_cell.animal
            from_cell.animal = None
            return True
        return False

    def update(self, current_time):
        # Обновляем растения — сначала адаптация к времени и рост
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.plant:
                    cell.plant.adapt_to_time(current_time)
        # Растения пытаются расти
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                