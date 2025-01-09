import unittest
from compas_fea2.model.groups import NodesGroup, ElementsGroup, FacesGroup, PartsGroup
from compas_fea2.model import Node, BeamElement, DeformablePart, ShellElement, ShellSection, Steel


class TestNodesGroup(unittest.TestCase):
    def test_add_node(self):
        node = Node([0, 0, 0])
        group = NodesGroup(nodes=[node])
        self.assertIn(node, group.nodes)


class TestElementsGroup(unittest.TestCase):
    def test_add_element(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        mat = Steel.S355()
        section = ShellSection(0.1, material=mat)
        element = BeamElement(nodes=[node1, node2], section=section, frame=[0, 0, 1])
        group = ElementsGroup(elements=[element])
        self.assertIn(element, group.elements)


class TestFacesGroup(unittest.TestCase):
    def test_add_face(self):
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        node3 = Node([1, 1, 0])
        nodes = [node1, node2, node3]
        mat = Steel.S355()
        section = ShellSection(0.1, material=mat)
        element = ShellElement(nodes=nodes, section=section)
        face = element.faces[0]
        group = FacesGroup(faces=element.faces)
        self.assertIn(face, group.faces)


class TestPartsGroup(unittest.TestCase):
    def test_add_part(self):
        part = DeformablePart()
        group = PartsGroup(parts=[part])
        self.assertIn(part, group.parts)


if __name__ == "__main__":
    unittest.main()
