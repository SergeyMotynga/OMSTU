import random
from plants import Plant, Lumiere, Obscurite, Demi
from registry import registry

class EvalAnimalMeta(type):
    def __new__(cls, name, bases, attrs):
        if name != 'Animal':
            registry['animals'][name] = cls
            behavior = attrs.get('behavior', {})
            def eat(self, world):
                food_types = behavior.get('food', [])
                eat_amount = behavior.get('eat_amount', {}).get(world.time_manager.time_of_day, 0)
                neighbors = world.get_neighbors(self.x, self.y)
                for nx, ny, entity in neighbors:
                    if isinstance(entity, tuple(food_types)) and random.random() < 0.5:
                        self.hunger = max(0, self.hunger - eat_amount)
                        entity.alive = False
                        world.grid[ny][nx] = None
                        break
            def move(self, world):
                speed = behavior.get('speed', {}).get(self.hunger < 5, 1)
                if random.random() < speed:
                    neighbors = world.get_neighbors(self.x, self.y)
                    empty_cells = [(nx, ny) for nx, ny, entity in neighbors if entity is None]
                    if empty_cells:
                        nx, ny = random.choice(empty_cells)
                        world.grid[self.y][self.x] = None
                        self.x, self.y = nx, ny
                        world.grid[ny][nx] = self
            def reproduce(self, world):
                repro_chance = behavior.get('repro_chance', 0.1)
                repro_condition = behavior.get('repro_condition', lambda self: True)
                if repro_condition(self) and random.random() < repro_chance:
                    x, y = world.get_random_empty_position()
                    if x is not None:
                        offspring = type(self)(x, y)
                        offspring.group = self.group if 'group' in behavior and behavior['group'] == 'same' else random.choice([a.group for a in world.entities if isinstance(a, type(self)) and a.group != self.group])
                        return [offspring]
                return []
            def interact(self, world):
                aggression = behavior.get('aggression', lambda self: 0)
                if aggression(self) > 0.7:
                    neighbors = world.get_neighbors(self.x, self.y)
                    for nx, ny, entity in neighbors:
                        if isinstance(entity, type(self)) and entity.group != self.group and random.random() < 0.2:
                            entity.alive = False
                            world.grid[ny][nx] = None
                elif 'group_size' in behavior and len(self.group) < behavior['group_size']:
                    neighbors = world.get_neighbors(self.x, self.y)
                    for nx, ny, entity in neighbors:
                        if isinstance(entity, type(self)) and entity.group != self.group and len(self.group) < behavior['group_size']:
                            self.group.extend(entity.group)
                            for animal in entity.group:
                                animal.group = self.group
            attrs['eat'] = eat
            attrs['move'] = move
            attrs['reproduce'] = reproduce
            attrs['interact'] = interact
        return super().__new__(cls, name, bases, attrs)

class Animal(metaclass=EvalAnimalMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.hunger = 0
        self.max_hunger = 10
        self.group = [self]

    def update(self, world):
        self.hunger += 0.5
        if self.hunger >= self.max_hunger:
            self.alive = False
            return
        self.move(world)
        self.eat(world)
        self.interact(world)

    def get_offspring(self, world):
        return self.reproduce(world)

class Pauvre(Animal):
    behavior = {
        'food': [Lumiere],
        'eat_amount': {'morning': 3, 'evening': 1, 'night': 0, 'day': 0},
        'repro_chance': 0.1,
        'repro_condition': lambda self: len(self.group) > 1,
        'group': 'same',
        'group_size': 5,
        'aggression': lambda self: self.hunger / self.max_hunger if len(self.group) > 5 else 0,
        'speed': {True: 1, False: 1}
    }

    def update(self, world):
        self.world = world
        if world.time_manager.time_of_day == "night":
            return
        super().update(world)
        if len(self.group) > 5 and random.random() < 0.1:
            self.group = self.group[:len(self.group)//2]
            new_group = self.group[len(self.group)//2:]
            for animal in new_group:
                animal.group = new_group

class Malheureux(Animal):
    behavior = {
        'food': [Demi, Obscurite, Pauvre],
        'eat_amount': {'morning': 3, 'evening': 3, 'night': 0, 'day': 0},
        'repro_chance': 0.1,
        'repro_condition': lambda self: any(a.group != self.group for a in self.world.entities if isinstance(a, Malheureux)),
        'group': 'other',
        'group_size': 5,
        'aggression': lambda self: 1 if len(self.group) > 3 else 0,
        'speed': {True: 1, False: 0.5}
    }

    def update(self, world):
        self.world = world
        if world.time_manager.time_of_day not in ['morning', 'evening']:
            return
        super().update(world)
        if len(self.group) > 5 and random.random() < 0.1:
            self.group = self.group[:len(self.group)//2]
            new_group = self.group[len(self.group)//2:]
            for animal in new_group:
                animal.group = new_group