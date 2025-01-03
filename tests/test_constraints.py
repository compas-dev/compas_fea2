import unittest
from compas_fea2.model.constraints import TieMPC, BeamMPC
from compas_fea2.model import Node

class TestTieMPC(unittest.TestCase):
    def test_initialization(self):
        master = Node([0, 0, 0])
        slave = Node([1, 0, 0])
        constraint = TieMPC(constraint_type="tie", master=master, slaves=[slave], tol=0.1)
        self.assertEqual(constraint.master, master)
        self.assertIn(slave, constraint.slaves)

class TestBeamMPC(unittest.TestCase):
    def test_initialization(self):
        master = Node([0, 0, 0])
        slave = Node([1, 0, 0])
        constraint = BeamMPC(constraint_type="beam", master=master, slaves=[slave], tol=0.1)
        self.assertEqual(constraint.master, master)
        self.assertIn(slave, constraint.slaves)

if __name__ == "__main__":
    unittest.main()
