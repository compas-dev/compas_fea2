import unittest
from compas_fea2.model.parts import _Part, DeformablePart, RigidPart
from compas_fea2.model import Node, BeamElement, _BeamEndRelease

class TestPart(unittest.TestCase):
    def test_add_node(self):
        part = _Part()
        node = Node([0, 0, 0])
        part.add_node(node)
        self.assertIn(node, part.nodes)

    def test_add_element(self):
        part = _Part()
        node1 = Node([0, 0, 0])
        node2 = Node([1, 0, 0])
        part.add_node(node1)
        part.add_node(node2)
        element = BeamElement(nodes=[node1, node2], section=None)
        part.add_element(element)
        self.assertIn(element, part.elements)

class TestDeformablePart(unittest.TestCase):
    def test_add_material(self):
        part = DeformablePart()
        material = object()  # Replace with actual material class
        part.add_material(material)
        self.assertIn(material, part.materials)

    def test_add_section(self):
        part = DeformablePart()
        section = object()  # Replace with actual section class
        part.add_section(section)
        self.assertIn(section, part.sections)

    def test_add_beam_release(self):
        part = DeformablePart()
        element = BeamElement(nodes=[], section=None)
        release = _BeamEndRelease()
        part.add_beam_release(element, "start", release)
        self.assertIn(release, part.releases)

class TestRigidPart(unittest.TestCase):
    def test_reference_point(self):
        part = RigidPart()
        node = Node([0, 0, 0])
        part.reference_point = node
        self.assertEqual(part.reference_point, node)

if __name__ == "__main__":
    unittest.main()
