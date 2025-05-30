from animals.base_animal import BaseAnimal
from animals.pauvre import Pauvre
import random

class Malheureux(BaseAnimal):
    def __init__(self):
        super().__init__()
        self.symbol = "M"
        self.pack_size = 1

    def adapt_to_time(self, time_of_day):
        # Активны утром и вечером, спят днем и ночью
        self.active = (time_of_day == "morning" or time_of_day == "evening")

        # Медлительны при голоде
        self.speed = 0.5 if self.hunger > 5 else 1.0

    def try_eat(self, world, x, y):
        cell = world.grid[y][x]

        # Едят Demi, Obscurite
        eaten = False
        if cell.plant and cell.plant.symbol in ("D", "O"):
            cell.plant = None
            self.hunger = max(0, self.hunger - 5)
            eaten = True

        if eaten:
            return

        # Ищут еду в соседних клетках
        neighbors = world.neighbors(x, y)
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            ncell = world.grid[ny][nx]
            if ncell.plant and ncell.plant.symbol in ("D", "O"):
                if world.move_animal(x, y, nx, ny):
                    ncell.plant = None
                    self.hunger = max(0, self.hunger - 5)
                break
            elif ncell.animal and isinstance(ncell.animal, Pauvre):
                if world.move_animal(x, y, nx, ny):
                    self.hunger = max(0, self.hunger - 10)
                break

    def move(self, world, x, y):
        if self.speed < 1.0:
            # Медленное движение — ходит через 2 шага
            if hasattr(self, "_skip_move") and self._skip_move:
                self._skip_move = False
                return
            self._skip_move = True

        super().move(world, x, y)

    def act(self, world, x, y):
        if not self.active:
            return

        self.hunger += 1
        self.try_eat(world, x, y)

        # Формирование стай и атаки — упрощённо
        neighbors = world.neighbors(x, y)
        nearby_malheureux = 0
        for nx, ny in neighbors:
            a = world.grid[ny][nx].animal
            if a and isinstance(a, Malheureux):
                nearby_malheureux += 1

        if nearby_malheureux > 3:
            self.pack_size = min(10, self.pack_size + 1)
        else:
            self.pack_size = max(1, self.pack_size - 1)

        self.move(world, x, y)
        self.try_reproduce(world, x, y)

    def try_reproduce(self, world, x, y):
        if self.pack_size > 3 and self.hunger < 5:
            neighbors = world.neighbors(x, y)
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                cell = world.grid[ny][nx]
                if cell.animal is None:
                    cell.animal = Malheureux()
                    self.pack_size -= 1
                    break
