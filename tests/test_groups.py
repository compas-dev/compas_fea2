import unittest
from compas_fea2.model.groups import NodesGroup, ElementsGroup, FacesGroup, PartsGroup
from compas_fea2.model import Node, BeamElement, DeformablePart

class TestNodesGroup(unittest.TestCase):
    def test_add_node(self):
        node = Node([0, 0, 0])
        group = NodesGroup(nodes=[node])
        self.assertIn(node, group.nodes)

class TestElementsGroup(unittest.TestCase):
    def test_add_element(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        element = BeamElement(nodes=[node1, node2], section=None)
        group = ElementsGroup(elements=[element])
        self.assertIn(element, group.elements)

class TestFacesGroup(unittest.TestCase):
    def test_add_face(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        node3 = Node([1, 1, 0])
        face = object()  # Replace with actual face class
        group = FacesGroup(faces=[face])
        self.assertIn(face, group.faces)

class TestPartsGroup(unittest.TestCase):
    def test_add_part(self):
        part = DeformablePart()
        group = PartsGroup(parts=[part])
        self.assertIn(part, group.parts)

if __name__ == "__main__":
    unittest.main()
