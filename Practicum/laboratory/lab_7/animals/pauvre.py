from animals.base_animal import BaseAnimal
import random

class Pauvre(BaseAnimal):
    def __init__(self):
        super().__init__()
        self.symbol = "P"
        self.group_size = 1
        self.aggression = 0  # зависит от голода и численности группы

    def adapt_to_time(self, time_of_day):
        # Спят ночью
        self.active = (time_of_day != "night")

        # Агрессия растет с голодом
        self.aggression = min(1.0, self.hunger / 10)

        # Питаются по-разному в утро и вечер
        self.eating_factor = 1.0 if time_of_day == "morning" else 0.2 if time_of_day == "evening" else 0.5

    def try_eat(self, world, x, y):
        cell = world.grid[y][x]
        # Едят только Lumiere
        if cell.plant and cell.plant.symbol == "L":
            # Едят — уменьшают голод и уничтожают растение
            cell.plant = None
            self.hunger = max(0, self.hunger - 5)
            return

        # Ищут в соседних клетках Lumiere
        neighbors = world.neighbors(x, y)
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            ncell = world.grid[ny][nx]
            if ncell.plant and ncell.plant.symbol == "L":
                # Перемещаются туда и едят
                if world.move_animal(x, y, nx, ny):
                    ncell.plant = None
                    self.hunger = max(0, self.hunger - 5)
                break

    def act(self, world, x, y):
        if not self.active:
            return

        self.hunger += 1
        self.try_eat(world, x, y)

        # Агрессия и формирование групп — упрощенно
        neighbors = world.neighbors(x, y)
        nearby_pauvre = 0
        for nx, ny in neighbors:
            a = world.grid[ny][nx].animal
            if a and isinstance(a, Pauvre):
                nearby_pauvre += 1

        if nearby_pauvre < 2:
            # Формируем группы (увеличиваем group_size)
            self.group_size = min(5, self.group_size + 1)
        else:
            # При перенаселении — агрессия повышается, группа распадается
            if random.random() < self.aggression:
                # Агрессивное поведение — например, убегает
                self.move(world, x, y)
                self.group_size = 1

        # Двигаемся
        self.move(world, x, y)
        # Размножаемся (упрощенно)
        self.try_reproduce(world, x, y)

    def try_reproduce(self, world, x, y):
        if self.group_size > 1 and self.hunger < 5:
            neighbors = world.neighbors(x, y)
            random.shuffle(neighbors)
            for nx, ny in neighbors:
                cell = world.grid[ny][nx]
                if cell.animal is None and cell.plant is None:
                    # Рождаем нового Pauvre
                    cell.animal = Pauvre()
                    self.group_size -= 1
                    break
