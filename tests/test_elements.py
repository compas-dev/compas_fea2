import unittest
from compas_fea2.model.elements import BeamElement, ShellElement, TetrahedronElement
from compas_fea2.model import Node, Steel, RectangularSection


class TestBeamElement(unittest.TestCase):
    def test_initialization(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        mat = Steel.S355()
        section = RectangularSection(w=1, h=2, material=mat)
        element = BeamElement(nodes=[node1, node2], section=section, frame=[0, 0, 1])
        self.assertEqual(element.nodes, [node1, node2])


class TestShellElement(unittest.TestCase):
    def test_initialization(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        node3 = Node([1, 1, 0])
        element = ShellElement(nodes=[node1, node2, node3], section=None)
        self.assertEqual(element.nodes, [node1, node2, node3])


class TestTetrahedronElement(unittest.TestCase):
    def test_initialization(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        node3 = Node([1, 1, 0])
        node4 = Node([0, 1, 1])
        element = TetrahedronElement(nodes=[node1, node2, node3, node4], section=None)
        self.assertEqual(element.nodes, [node1, node2, node3, node4])


if __name__ == "__main__":
    unittest.main()
