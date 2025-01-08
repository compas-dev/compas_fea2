import unittest
from compas_fea2.model.bcs import FixedBC, PinnedBC, RollerBCX

class TestBCs(unittest.TestCase):

    def test_fixed_bc(self):
        bc = FixedBC()
        self.assertTrue(bc.x)
        self.assertTrue(bc.y)
        self.assertTrue(bc.z)
        self.assertTrue(bc.xx)
        self.assertTrue(bc.yy)
        self.assertTrue(bc.zz)

    def test_pinned_bc(self):
        bc = PinnedBC()
        self.assertTrue(bc.x)
        self.assertTrue(bc.y)
        self.assertTrue(bc.z)
        self.assertFalse(bc.xx)
        self.assertFalse(bc.yy)
        self.assertFalse(bc.zz)

    def test_roller_bc_x(self):
        bc = RollerBCX()
        self.assertFalse(bc.x)
        self.assertTrue(bc.y)
        self.assertTrue(bc.z)
        self.assertFalse(bc.xx)
        self.assertFalse(bc.yy)
        self.assertFalse(bc.zz)

if __name__ == "__main__":
    unittest.main()
