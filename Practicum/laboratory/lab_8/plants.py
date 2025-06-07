import random
from registry import registry

class EvalPlantMeta(type):
    def __new__(cls, name, bases, attrs):
        if name != 'Plant':
            registry['plants'][name] = cls
            growth_conditions = attrs.get('growth_conditions', {})
            def spread(self, world):
                if self.can_grow(world):  # Убрали random.random() для тестов
                    self.growth += 1
                    if self.growth >= self.max_growth:
                        neighbors = world.get_neighbors(self.x, self.y)
                        empty_cells = [(nx, ny) for nx, ny, entity in neighbors if entity is None]
                        if empty_cells:
                            nx, ny = random.choice(empty_cells)
                            new_plant = type(self)(nx, ny)
                            world.grid[ny][nx] = new_plant
                            world.entities.append(new_plant)
                        for nx, ny, entity in neighbors:
                            if entity and isinstance(entity, Plant) and not entity.can_grow(world) and random.random() < 0.2:
                                world.grid[ny][nx] = type(self)(nx, ny)
                                world.entities.append(world.grid[ny][nx])
                                entity.alive = False
                                world.entities.remove(entity)  # Удаляем вытесненное растение
            def can_grow(self, world):
                return world.time_manager.time_of_day in growth_conditions.get('active_times', [])
            attrs['spread'] = spread
            attrs['can_grow'] = can_grow
        return super().__new__(cls, name, bases, attrs)

class Plant(metaclass=EvalPlantMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.growth = 0
        self.max_growth = 10

    def update(self, world):
        self.spread(world)

    def get_offspring(self, world):
        return []

class Lumiere(Plant):
    growth_conditions = {'active_times': ['day']}

class Obscurite(Plant):
    growth_conditions = {'active_times': ['night']}

class Demi(Plant):
    growth_conditions = {'active_times': ['morning', 'evening']}