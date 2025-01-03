import pytest
from compas_fea2.model.sections import RectangularSection, CircularSection, ISection
from compas_fea2.model import Steel

@pytest.fixture
def material():
    return Steel.S355()

def test_rectangular_section(material):
    section = RectangularSection(w=100, h=50, material=material)
    assert section.shape.w == 100
    assert section.shape.h == 50
    assert pytest.approx(section.A) == 5000
    assert section.material == material

def test_circular_section(material):
    section = CircularSection(r=10, material=material)
    assert section.shape.radius == 10
    assert pytest.approx(section.A, 0.001) == 314.159
    assert section.material == material

def test_isection(material):
    section = ISection(w=100, h=200, tw=10, tf=20, material=material)
    assert section.shape.w == 100
    assert section.shape.h == 200
    assert section.shape.tw == 10
    assert section.shape.tbf == 20
    assert section.shape.ttf == 20
    assert section.material == material
