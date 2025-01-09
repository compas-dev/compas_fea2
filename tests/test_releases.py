import unittest
from compas_fea2.model.releases import _BeamEndRelease, BeamEndPinRelease, BeamEndSliderRelease


class TestBeamEndRelease(unittest.TestCase):
    def test_initialization(self):
        release = _BeamEndRelease(n=True, v1=True, v2=True, m1=True, m2=True, t=True)
        self.assertTrue(release.n)
        self.assertTrue(release.v1)
        self.assertTrue(release.v2)
        self.assertTrue(release.m1)
        self.assertTrue(release.m2)
        self.assertTrue(release.t)

    def test_element_setter(self):
        pass

    def test_location_setter(self):
        release = _BeamEndRelease()
        with self.assertRaises(TypeError):
            release.location = "middle"
        release.location = "start"
        self.assertEqual(release.location, "start")


class TestBeamEndPinRelease(unittest.TestCase):
    def test_initialization(self):
        release = BeamEndPinRelease(m1=True, m2=True, t=True)
        self.assertTrue(release.m1)
        self.assertTrue(release.m2)
        self.assertTrue(release.t)
        self.assertFalse(release.n)
        self.assertFalse(release.v1)
        self.assertFalse(release.v2)


class TestBeamEndSliderRelease(unittest.TestCase):
    def test_initialization(self):
        release = BeamEndSliderRelease(v1=True, v2=True)
        self.assertTrue(release.v1)
        self.assertTrue(release.v2)
        self.assertFalse(release.n)
        self.assertFalse(release.m1)
        self.assertFalse(release.m2)
        self.assertFalse(release.t)


if __name__ == "__main__":
    unittest.main()
