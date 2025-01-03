import unittest
from compas_fea2.model.connectors import SpringConnector, ZeroLengthSpringConnector
from compas_fea2.model import Node

class TestSpringConnector(unittest.TestCase):
    def test_initialization(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        section = object()  # Replace with actual section class
        connector = SpringConnector(nodes=[node1, node2], section=section)
        self.assertEqual(connector.nodes, [node1, node2])

class TestZeroLengthSpringConnector(unittest.TestCase):
    def test_initialization(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        section = object()  # Replace with actual section class
        directions = [1, 0, 0]
        connector = ZeroLengthSpringConnector(nodes=[node1, node2], section=section, directions=directions)
        self.assertEqual(connector.nodes, [node1, node2])
        self.assertEqual(connector.directions, directions)

if __name__ == "__main__":
    unittest.main()
