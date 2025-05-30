import random

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.growth = 0
        self.max_growth = 10

    def can_grow(self, world):
        return False

    def update(self, world):
        if self.can_grow(world) and random.random() < 0.5:
            self.growth += 1
            if self.growth >= self.max_growth:
                self.try_spread(world)

    def try_spread(self, world):
        neighbors = world.get_neighbors(self.x, self.y)
        empty_cells = [(nx, ny) for nx, ny, entity in neighbors if entity is None]
        if empty_cells:
            nx, ny = random.choice(empty_cells)
            world.grid[ny][nx] = type(self)(nx, ny)
            world.entities.append(world.grid[ny][nx])
        for nx, ny, entity in neighbors:
            if entity and isinstance(entity, Plant) and not entity.can_grow(world) and random.random() < 0.2:
                world.grid[ny][nx] = type(self)(nx, ny)
                world.entities.append(world.grid[ny][nx])
                entity.alive = False

    def get_offspring(self, world):
        return []

class Lumiere(Plant):
    def can_grow(self, world):
        return world.time_manager.time_of_day == "day"

class Obscurite(Plant):
    def can_grow(self, world):
        return world.time_manager.time_of_day == "night"

class Demi(Plant):
    def can_grow(self, world):
        return world.time_manager.time_of_day in ["morning", "evening"]