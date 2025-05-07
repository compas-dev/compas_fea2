import unittest
from compas_fea2.model.parts import Part, RigidPart
from compas_fea2.model import Node, BeamElement
from compas_fea2.model import Steel
from compas_fea2.model import RectangularSection


class TestPart(unittest.TestCase):
    def test_add_node(self):
        part = Part()
        node = Node([0, 0, 0])
        part.add_node(node)
        self.assertIn(node, part.nodes)

    def test_add_element(self):
        part = Part()
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        part.add_node(node1)
        part.add_node(node2)
        section = RectangularSection(w=1, h=1, material=Steel.S355())
        element = BeamElement(nodes=[node1, node2], section=section, frame=[0, 0, 1])
        part.add_element(element)
        self.assertIn(element, part.elements)

    def test_add_material(self):
        part = Part()
        material = Steel.S355()
        part.add_material(material)
        self.assertIn(material, part.materials)

    def test_add_section(self):
        part = Part()
        material = Steel.S355()
        section = RectangularSection(w=1, h=1, material=material)
        part.add_section(section)
        self.assertIn(section, part.sections)


class TestRigidPart(unittest.TestCase):
    def test_reference_point(self):
        part = RigidPart()
        node = Node([0, 0, 0])
        part.reference_point = node
        self.assertEqual(part.reference_point, node)


if __name__ == "__main__":
    unittest.main()
