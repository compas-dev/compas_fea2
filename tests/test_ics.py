import unittest
from compas_fea2.model.ics import InitialTemperatureField, InitialStressField

class TestInitialTemperatureField(unittest.TestCase):
    def test_initialization(self):
        ic = InitialTemperatureField(temperature=100)
        self.assertEqual(ic.temperature, 100)

    def test_temperature_setter(self):
        ic = InitialTemperatureField(temperature=100)
        ic.temperature = 200
        self.assertEqual(ic.temperature, 200)

class TestInitialStressField(unittest.TestCase):
    def test_initialization(self):
        ic = InitialStressField(stress=(10, 20, 30))
        self.assertEqual(ic.stress, (10, 20, 30))

    def test_stress_setter(self):
        ic = InitialStressField(stress=(10, 20, 30))
        ic.stress = (40, 50, 60)
        self.assertEqual(ic.stress, (40, 50, 60))

if __name__ == "__main__":
    unittest.main()
