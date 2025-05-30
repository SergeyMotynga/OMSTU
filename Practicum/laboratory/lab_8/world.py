import random
from registry import registry
from time_manager import TimeManager

class World:
    def __init__(self, width, height, plant_density=0.5):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.time_manager = TimeManager()
        self.entities = []
        self.initialize_grid(plant_density)

    def initialize_grid(self, plant_density):
        from plants import Lumiere, Obscurite, Demi
        from animals import Pauvre, Malheureux
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < plant_density:
                    plant_type = random.choice([Lumiere, Obscurite, Demi])
                    self.grid[y][x] = plant_type(x, y)
                    self.entities.append(self.grid[y][x])
        for _ in range(int(self.width * self.height * 0.1)):
            x, y = self.get_random_empty_position()
            if x is not None:
                animal_type = random.choice([Pauvre, Malheureux])
                animal = animal_type(x, y)
                self.grid[y][x] = animal
                self.entities.append(animal)

    def get_random_empty_position(self):
        empty_positions = [(x, y) for y in range(self.height) for x in range(self.width) if self.grid[y][x] is None]
        return random.choice(empty_positions) if empty_positions else (None, None)

    def get_neighbors(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny, self.grid[ny][nx]))
        return neighbors

    def update(self):
        from plants import Plant
        from animals import Pauvre, Malheureux
        self.time_manager.update()
        random.shuffle(self.entities)
        new_entities = []
        for entity in self.entities:
            if entity.alive:
                entity.update(self)
                new_entities.extend(entity.get_offspring(self))
        self.entities.extend(new_entities)
        self.entities = [e for e in self.entities if e.alive]
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] and not self.grid[y][x].alive:
                    self.grid[y][x] = None
        print(f"Tick: {self.time_manager.tick}, Time: {self.time_manager.time_of_day}, "
              f"Plants: {sum(1 for e in self.entities if isinstance(e, Plant))}, "
              f"Pauvre: {sum(1 for e in self.entities if isinstance(e, Pauvre))}, "
              f"Malheureux: {sum(1 for e in self.entities if isinstance(e, Malheureux))}")