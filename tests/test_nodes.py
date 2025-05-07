import unittest
from compas_fea2.model.nodes import Node
from compas.geometry import Point


class TestNode(unittest.TestCase):
    def test_initialization(self):
        node = Node([1, 2, 3])
        self.assertEqual(node.xyz, [1, 2, 3])
        self.assertEqual(node.mass, [None, None, None, None, None, None])
        self.assertIsNone(node.temperature)

    def test_mass_setter(self):
        node = Node([1, 2, 3], mass=[10, 10, 10, 10, 10, 10])
        self.assertEqual(node.mass, [10, 10, 10, 10, 10, 10])
        node.mass = [5, 5, 5, 5, 5, 5]
        self.assertEqual(node.mass, [5, 5, 5, 5, 5, 5])

    def test_temperature_setter(self):
        node = Node([1, 2, 3], temperature=100)
        self.assertEqual(node.temperature, 100)
        node.temperature = 200
        self.assertEqual(node.temperature, 200)

    def test_gkey(self):
        node = Node([1, 2, 3])
        self.assertIsNotNone(node.gkey)

    def test_from_compas_point(self):
        point = Point(1, 2, 3)
        node = Node.from_compas_point(point)
        self.assertEqual(node.xyz, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
