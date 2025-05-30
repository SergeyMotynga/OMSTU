import random

class BaseAnimal:
    def __init__(self):
        self.hunger = 0  # уровень голода, растет со временем
        self.group = None  # ссылка на группу/стая (можно расширить)
        self.symbol = "A"
        self.active = True  # активность (спит или нет)

    def adapt_to_time(self, time_of_day):
        """
        Меняет поведение животного в зависимости от времени суток.
        В базовом классе — просто активность.
        """
        self.active = True

    def act(self, world, x, y):
        """
        Основной метод действия животного за тик.
        """
        if not self.active:
            return  # спит — не действует

        self.hunger += 1  # голод растет

        self.try_eat(world, x, y)
        self.move(world, x, y)
        self.try_reproduce(world, x, y)

    def try_eat(self, world, x, y):
        """
        Пытается поесть в текущей или соседних клетках.
        """
        pass

    def move(self, world, x, y):
        """
        Двигается в соседнюю клетку (если пусто).
        """
        neighbors = world.neighbors(x, y)
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            if world.grid[ny][nx].animal is None:
                if world.move_animal(x, y, nx, ny):
                    break

    def try_reproduce(self, world, x, y):
        """
        Попытка размножения при подходящих условиях.
        """
        pass
