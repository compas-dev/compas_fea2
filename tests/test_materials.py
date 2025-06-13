import unittest
from compas_fea2.model import Concrete

# Concrete properties based on Eurocode 2 (EN 1992-1-1:2004)
concrete_properties = {
    "C12/15": {"fck": 12, "fck_cube": 15, "fcm": 20, "fctm": 1.57, "Ecm": 27085},
    "C16/20": {"fck": 16, "fck_cube": 20, "fcm": 24, "fctm": 1.90, "Ecm": 28608},
    "C20/25": {"fck": 20, "fck_cube": 25, "fcm": 28, "fctm": 2.21, "Ecm": 29962},
    "C25/30": {"fck": 25, "fck_cube": 30, "fcm": 33, "fctm": 2.56, "Ecm": 31476},
    "C30/37": {"fck": 30, "fck_cube": 37, "fcm": 38, "fctm": 2.90, "Ecm": 32837},
    "C35/45": {"fck": 35, "fck_cube": 45, "fcm": 43, "fctm": 3.21, "Ecm": 34077},
    "C40/50": {"fck": 40, "fck_cube": 50, "fcm": 48, "fctm": 3.51, "Ecm": 35220},
    "C45/55": {"fck": 45, "fck_cube": 55, "fcm": 53, "fctm": 3.80, "Ecm": 36283},
    "C50/60": {"fck": 50, "fck_cube": 60, "fcm": 58, "fctm": 4.07, "Ecm": 37278},
    "C55/67": {"fck": 55, "fck_cube": 67, "fcm": 63, "fctm": 4.21, "Ecm": 38214},
    "C60/75": {"fck": 60, "fck_cube": 75, "fcm": 68, "fctm": 4.35, "Ecm": 39100},
    "C70/85": {"fck": 70, "fck_cube": 85, "fcm": 78, "fctm": 4.61, "Ecm": 40743},
    "C80/95": {"fck": 80, "fck_cube": 95, "fcm": 88, "fctm": 4.84, "Ecm": 42244},
    "C90/105": {"fck": 90, "fck_cube": 105, "fcm": 98, "fctm": 5.04, "Ecm": 43631},
}


class TestConcrete(unittest.TestCase):
    def test_C20_25(self):
        properties = concrete_properties["C20/25"]
        c20 = Concrete.C20_25()
        self.assertEqual(c20.fck, properties["fck"])
        self.assertEqual(c20.fcd, properties["fcd"])
        self.assertEqual(c20.E, properties["Ecm"])
