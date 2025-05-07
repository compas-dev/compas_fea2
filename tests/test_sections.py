import unittest
from compas_fea2.model.sections import RectangularSection, CircularSection, ISection
from compas_fea2.model.materials.steel import Steel


class TestSections(unittest.TestCase):
    def setUp(self):
        self.material = Steel.S355()

    def test_rectangular_section(self):
        section = RectangularSection(w=100, h=50, material=self.material)
        self.assertEqual(section.shape.w, 100)
        self.assertEqual(section.shape.h, 50)
        self.assertAlmostEqual(section.A, 5000)
        self.assertEqual(section.material, self.material)

    def test_circular_section(self):
        section = CircularSection(r=10, material=self.material)
        self.assertEqual(section.shape.radius, 10)
        self.assertAlmostEqual(section.A, 314.14, places=2)
        self.assertEqual(section.material, self.material)

    def test_isection(self):
        section = ISection(w=100, h=200, tw=10, ttf=20, tbf=20, material=self.material)
        self.assertEqual(section.shape.w, 100)
        self.assertEqual(section.shape.h, 200)
        self.assertEqual(section.shape.tw, 10)
        self.assertEqual(section.shape.tbf, 20)
        self.assertEqual(section.shape.ttf, 20)
        self.assertEqual(section.material, self.material)


if __name__ == "__main__":
    unittest.main()
