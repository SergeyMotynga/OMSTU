import random
from plants import Lumiere, Obscurite, Demi

class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.hunger = 0
        self.max_hunger = 10
        self.group = [self]
        self.modify_behavior()

    def modify_behavior(self):
        pass

    def update(self, world):
        self.hunger += 1
        self.modify_behavior()
        if self.hunger >= self.max_hunger:
            self.alive = False
            return
        self.move(world)
        self.eat(world)
        self.interact(world)

    def move(self, world):
        neighbors = world.get_neighbors(self.x, self.y)
        empty_cells = [(nx, ny) for nx, ny, entity in neighbors if entity is None]
        if empty_cells:
            nx, ny = random.choice(empty_cells)
            world.grid[self.y][self.x] = None
            self.x, self.y = nx, ny
            world.grid[ny][nx] = self

    def eat(self, world):
        pass

    def interact(self, world):
        pass

    def get_offspring(self, world):
        return []

class Pauvre(Animal):
    def modify_behavior(self):
        time = self.world.time_manager.time_of_day if hasattr(self, 'world') else "morning"
        self.eat_amount = 3 if time == "morning" else 1 if time == "evening" else 0
        self.aggression = self.hunger / self.max_hunger if len(self.group) > 5 else 0

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

    def eat(self, world):
        neighbors = world.get_neighbors(self.x, self.y)
        for nx, ny, entity in neighbors:
            if isinstance(entity, Lumiere) and random.random() < 0.5:
                self.hunger = max(0, self.hunger - self.eat_amount)
                entity.alive = False
                world.grid[ny][nx] = None
                break

    def interact(self, world):
        if self.aggression > 0.7:
            neighbors = world.get_neighbors(self.x, self.y)
            for nx, ny, entity in neighbors:
                if isinstance(entity, Pauvre) and entity.group != self.group and random.random() < 0.2:
                    entity.alive = False
                    world.grid[ny][nx] = None
        else:
            neighbors = world.get_neighbors(self.x, self.y)
            for nx, ny, entity in neighbors:
                if isinstance(entity, Pauvre) and entity.group != self.group and len(self.group) < 5:
                    self.group.extend(entity.group)
                    for animal in entity.group:
                        animal.group = self.group

    def get_offspring(self, world):
        if len(self.group) > 1 and random.random() < 0.05:
            x, y = world.get_random_empty_position()
            if x is not None:
                offspring = Pauvre(x, y)
                offspring.group = self.group
                return [offspring]
        return []

class Malheureux(Animal):
    def modify_behavior(self):
        time = self.world.time_manager.time_of_day if hasattr(self, 'world') else "morning"
        self.active = time in ["morning", "evening"]
        self.speed = 1 if self.hunger < 5 else 0.5      

    def update(self, world):
        self.world = world
        if not self.active:
            return
        super().update(world)
        if len(self.group) > 5 and random.random() < 0.1:
            self.group = self.group[:len(self.group)//2]
            new_group = self.group[len(self.group)//2:]
            for animal in new_group:
                animal.group = new_group

    def eat(self, world):
        neighbors = world.get_neighbors(self.x, self.y)
        for nx, ny, entity in neighbors:
            if isinstance(entity, (Demi, Obscurite, Pauvre)) and random.random() < 0.5:
                self.hunger = max(0, self.hunger - 3)
                entity.alive = False
                world.grid[ny][nx] = None
                break

    def interact(self, world):
        if len(self.group) > 3:
            neighbors = world.get_neighbors(self.x, self.y)
            for nx, ny, entity in neighbors:
                if isinstance(entity, Malheureux) and entity.group != self.group and len(entity.group) < len(self.group):
                    entity.alive = False
                    world.grid[ny][nx] = None

    def get_offspring(self, world):
        other_groups = [a.group for a in world.entities if isinstance(a, Malheureux) and a.group != self.group]
        if other_groups and random.random() < 0.05:
            x, y = world.get_random_empty_position()
            if x is not None:
                offspring = Malheureux(x, y)
                offspring.group = random.choice(other_groups)
                return [offspring]
        return []