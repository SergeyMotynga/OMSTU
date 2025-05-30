import unittest
from world import World
from plants import Plant, Lumiere, Obscurite, Demi
from animals import Animal, Pauvre, Malheureux
from time_manager import TimeManager
from registry import registry

class TestEcosystem(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 10)
        self.world.time_manager = TimeManager()

    def test_registry(self):
        self.assertIn('Lumiere', registry['plants'])
        self.assertIn('Obscurite', registry['plants'])
        self.assertIn('Demi', registry['plants'])
        self.assertIn('Pauvre', registry['animals'])
        self.assertIn('Malheureux', registry['animals'])

    def test_plant_methods(self):
        plant = Lumiere(0, 0)
        self.assertTrue(hasattr(plant, 'spread'))
        self.assertTrue(hasattr(plant, 'can_grow'))
        self.world.time_manager.time_of_day = 'day'
        self.assertTrue(plant.can_grow(self.world))
        self.world.time_manager.time_of_day = 'night'
        self.assertFalse(plant.can_grow(self.world))

    def test_animal_methods(self):
        animal = Pauvre(0, 0)
        self.assertTrue(hasattr(animal, 'eat'))
        self.assertTrue(hasattr(animal, 'move'))
        self.assertTrue(hasattr(animal, 'reproduce'))
        self.assertTrue(hasattr(animal, 'interact'))

    def test_pauvre_behavior(self):
        pauvre = Pauvre(0, 0)
        self.world.time_manager.time_of_day = 'morning'
        self.world.grid[0][1] = Lumiere(1, 0)
        self.world.entities.append(self.world.grid[0][1])
        pauvre.hunger = 3
        pauvre.eat(self.world)
        self.assertLessEqual(pauvre.hunger, 3)

    def test_malheureux_behavior(self):
        mal = Malheureux(0, 0)
        self.world.time_manager.time_of_day = 'morning'
        self.world.grid[0][1] = Demi(1, 0)
        self.world.entities.append(self.world.grid[0][1])
        mal.hunger = 3
        mal.eat(self.world)
        self.assertLessEqual(mal.hunger, 3)

if __name__ == '__main__':
    unittest.main()