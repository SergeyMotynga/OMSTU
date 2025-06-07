import unittest
from world import World
from plants import Plant, Lumiere, Obscurite, Demi
from animals import Animal, Pauvre, Malheureux
from registry import registry

class TestEcosystem(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 10, plant_density=0.0)
        self.world.time_manager.time_of_day = 'day'

    def test_registry(self):
        self.assertIn('Lumiere', registry['plants'])
        self.assertIn('Obscurite', registry['plants'])
        self.assertIn('Demi', registry['plants'])
        self.assertIn('Pauvre', registry['animals'])
        self.assertIn('Malheureux', registry['animals'])

    def test_generated_methods_plant(self):
        plant = Lumiere(0, 0)
        self.assertTrue(hasattr(plant, 'spread'))
        self.assertTrue(hasattr(plant, 'can_grow'))

    def test_generated_methods_animal(self):
        animal = Pauvre(0, 0)
        for method in ['eat', 'move', 'reproduce', 'interact', 'update', 'get_neighbors_in_vision']:
            self.assertTrue(hasattr(animal, method))

    def test_plant_spread_day(self):
        self.world.grid = [[None for _ in range(self.world.width)] for _ in range(self.world.height)]
        self.world.entities = []
        plant = Lumiere(5, 5)
        self.world.grid[5][5] = plant
        self.world.entities.append(plant)
        self.world.time_manager.time_of_day = 'day'
        plant.growth = 9
        plant.update(self.world)
        new_plants = sum(1 for e in self.world.entities if isinstance(e, Lumiere))
        self.assertGreaterEqual(new_plants, 1)

    def test_plant_no_spread_wrong_time(self):
        self.world.grid = [[None for _ in range(self.world.width)] for _ in range(self.world.height)]
        self.world.entities = []
        plant = Lumiere(5, 5)
        self.world.grid[5][5] = plant
        self.world.entities.append(plant)
        self.world.time_manager.time_of_day = 'night'
        plant.growth = 9
        plant.update(self.world)
        new_plants = sum(1 for e in self.world.entities if isinstance(e, Lumiere))
        self.assertEqual(new_plants, 1)

    def test_animal_eat(self):
        self.world.grid = [[None for _ in range(self.world.width)] for _ in range(self.world.height)]
        self.world.entities = []
        animal = Pauvre(5, 5)
        plant = Lumiere(5, 6)
        self.world.grid[5][5] = animal
        self.world.grid[5][6] = plant
        self.world.entities.extend([animal, plant])
        animal.world = self.world
        self.world.time_manager.time_of_day = 'morning'
        animal.hunger = 5
        animal.eat(self.world)
        self.assertLessEqual(animal.hunger, 2)
        self.assertFalse(plant.alive)

    def test_animal_no_eat_wrong_time(self):
        self.world.grid = [[None for _ in range(self.world.width)] for _ in range(self.world.height)]
        self.world.entities = []
        animal = Pauvre(5, 5)
        plant = Lumiere(5, 6)
        self.world.grid[5][5] = animal
        self.world.grid[5][6] = plant
        self.world.entities.extend([animal, plant])
        animal.world = self.world
        self.world.time_manager.time_of_day = 'night'
        animal.hunger = 5
        animal.eat(self.world)
        self.assertEqual(animal.hunger, 5)

    def test_vision_radius(self):
        self.world.grid = [[None for _ in range(self.world.width)] for _ in range(self.world.height)]
        self.world.entities = []
        animal = Pauvre(5, 5)
        neighbor = Lumiere(6, 6)
        self.world.grid[5][5] = animal
        self.world.grid[6][6] = neighbor
        self.world.entities.extend([animal, neighbor])
        animal.world = self.world
        neighbors = animal.get_neighbors_in_vision(self.world)
        self.assertEqual(len(neighbors), 1)  # Pauvre видит Lumiere в радиусе 1
        self.assertEqual(neighbors[0][2], neighbor)

    def test_malheureux_vision_radius(self):
        self.world.grid = [[None for _ in range(self.world.width)] for _ in range(self.world.height)]
        self.world.entities = []
        animal = Malheureux(5, 5)
        neighbor = Lumiere(7, 7)
        self.world.grid[5][5] = animal
        self.world.grid[7][7] = neighbor
        self.world.entities.extend([animal, neighbor])
        animal.world = self.world
        neighbors = animal.get_neighbors_in_vision(self.world)
        self.assertEqual(len(neighbors), 1)  # Malheureux видит Lumiere в радиусе 3

if __name__ == '__main__':
    unittest.main()