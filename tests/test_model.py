import unittest
from compas_fea2.model.model import Model
from compas_fea2.model.parts import Part
from compas_fea2.problem import Problem


class TestModel(unittest.TestCase):
    def test_add_part(self):
        model = Model()
        part = Part()
        model.add_part(part)
        self.assertIn(part, model.parts)

    def test_find_part_by_name(self):
        model = Model()
        part = Part(name="test_part")
        model.add_part(part)
        found_part = model.find_part_by_name("test_part")
        self.assertEqual(found_part, part)

    def test_add_problem(self):
        model = Model()
        problem = Problem()  # Replace with actual problem class
        model.add_problem(problem)
        self.assertIn(problem, model.problems)


if __name__ == "__main__":
    unittest.main()
