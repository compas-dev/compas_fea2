import pytest
from compas.geometry import Point, Frame
from compas_fea2.model.shapes import Rectangle, Circle, IShape, Shape

def test_rectangle():
    rect = Rectangle(w=100, h=50)
    assert rect.w == 100
    assert rect.h == 50
    assert pytest.approx(rect.A) == 5000
    assert isinstance(rect.centroid, Point)

def test_circle():
    circle = Circle(radius=10)
    assert circle.radius == 10
    assert pytest.approx(circle.A, 0.01) == 314.159
    assert isinstance(circle.centroid, Point)

def test_ishape():
    ishape = IShape(w=100, h=200, tw=10, tbf=20, ttf=20)
    assert ishape.w == 100
    assert ishape.h == 200
    assert ishape.tw == 10
    assert ishape.tbf == 20
    assert ishape.ttf == 20
    assert isinstance(ishape.centroid, Point)

def test_shape_translation():
    rect = Rectangle(w=100, h=50)
    translated_rect = rect.translated([10, 20, 30])
    assert isinstance(translated_rect, Shape)
    assert rect.centroid != translated_rect.centroid

def test_shape_orientation():
    rect = Rectangle(w=100, h=50)
    new_frame = Frame([0, 0, 1000], [1, 0, 0], [0, 1, 0])
    oriented_rect = rect.oriented(new_frame)
    assert isinstance(oriented_rect, Shape)
    assert rect.centroid != oriented_rect.centroid
