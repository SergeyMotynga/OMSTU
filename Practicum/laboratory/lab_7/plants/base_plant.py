import random

class BasePlant:
    def __init__(self):
        self.active = False  # Активен ли рост сейчас
        self.symbol = "?"

    def adapt_to_time(self, time_of_day):
        """
        Обновляет активность растения в зависимости от времени суток.
        """
        raise NotImplementedError

    def growth_chance(self):
        """
        Вероятность успешно занять соседнюю клетку (если конкуренция позволяет).
        """
        return 0.5  # базовая вероятность

    def grow(self, world, x, y):
        """
        Попытка распространения на соседние клетки.
        """
        if not self.active:
            return

        neighbors = world.neighbors(x, y)
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            neighbor_cell = world.grid[ny][nx]
            if neighbor_cell.plant is None:
                # Занять пустую клетку
                if random.random() < self.growth_chance():
                    neighbor_cell.plant = self.__class__()  # новый экземпляр
            else:
                # Конкуренция с другим растением
                other = neighbor_cell.plant
                if not other.active:
                    # Активное растение может вытеснить пассивное с вероятностью 0.7
                    if random.random() < 0.7:
                        neighbor_cell.plant = self.__class__()
                else:
                    # Если оба активны, случайно решаем кто останется
                    if random.random() < 0.5:
                        neighbor_cell.plant = self.__class__()
