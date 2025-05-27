import unittest
from compas.geometry import Point, Frame
from compas_fea2.model.shapes import Rectangle, Circle, IShape, Shape


class TestShapes(unittest.TestCase):
    def test_rectangle(self):
        rect = Rectangle(w=100, h=50)
        self.assertEqual(rect.w, 100)
        self.assertEqual(rect.h, 50)
        self.assertAlmostEqual(rect.A, 5000)
        self.assertIsInstance(rect.centroid, Point)
        self.assertEqual(rect.centroid.x, 0)
        self.assertEqual(rect.centroid.y, 0)
        self.assertEqual(rect.centroid.z, 0)
        self.assertAlmostEqual(rect.Ixx, 100 * 50**3 / 12, 3)
        self.assertAlmostEqual(rect.Iyy, 100**3 * 50 / 12, 3)
        self.assertAlmostEqual(rect.J, 2_861_002.60, places=2)
        self.assertAlmostEqual(rect.Avx, 4_166.67, places=2)
        self.assertAlmostEqual(rect.Avy, 4_166.67, places=2)

    def test_circle(self):
        circle = Circle(radius=10)
        self.assertEqual(circle.radius, 10)
        self.assertAlmostEqual(circle.A, 314.159, places=0)
        self.assertIsInstance(circle.centroid, Point)
        self.assertAlmostEqual(circle.Ixx, 7853, 0)
        self.assertAlmostEqual(circle.Iyy, 7853, 0)
        self.assertAlmostEqual(circle.J, 15708, places=0)
        self.assertAlmostEqual(circle.Avx, 283, places=0)
        self.assertAlmostEqual(circle.Avy, 283, places=0)

    def test_ishape(self):
        ishape = IShape(w=100, h=200, tw=10, tbf=20, ttf=20)
        self.assertEqual(ishape.w, 100)
        self.assertEqual(ishape.h, 200)
        self.assertEqual(ishape.tw, 10)
        self.assertEqual(ishape.tbf, 20)
        self.assertEqual(ishape.ttf, 20)
        self.assertIsInstance(ishape.centroid, Point)

    def test_shape_translation(self):
        rect = Rectangle(w=100, h=50)
        translated_rect = rect.translated([10, 20, 30])
        self.assertIsInstance(translated_rect, Shape)
        self.assertNotEqual(rect.centroid, translated_rect.centroid)

    def test_shape_orientation(self):
        rect = Rectangle(w=100, h=50)
        new_frame = Frame([0, 0, 1000], [1, 0, 0], [0, 1, 0])
        oriented_rect = rect.oriented(new_frame)
        self.assertIsInstance(oriented_rect, Shape)
        self.assertNotEqual(rect.centroid, oriented_rect.centroid)


if __name__ == "__main__":
    unittest.main()
