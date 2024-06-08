from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Frame, Plane
from compas.geometry import Translation
from compas.geometry import Transformation
from compas.datastructures import Mesh
from compas_fea2.base import DimensionlessMeta
from compas_fea2.base import FEAData

import numpy as np
from math import degrees, sqrt, atan2, pi


class Shape(Polygon, FEAData):
    def __init__(self, points, frame=None):
        super().__init__(points)
        if not self.is_planar:
            raise ValueError("The points mast belong to the same plane")
        self._frame = frame or Frame.worldXY()
        self._T = Transformation.from_frame_to_frame(self._frame, Frame.worldXY())
        self._J = None
        self._g0 = None
        self._gw = None
        self._Avx = None
        self._Avy = None

    def __str__(self):
        return f"""
    type:               {self.__class__.__name__}
    number of points:   {len(self._points)}
    number of edges:    {len(self._points)}  # Assuming closed shapes where number of edges = number of points
        """

    # ==========================================================================
    # Properties
    # ==========================================================================
    @property
    def points_xy(self):
        return [p.transformed(self._T) for p in self.points]

    @property
    def A(self):
        return self.area

    @property
    def centroid_xy(self):
        """Compute the centroid."""
        sx = sy = 0
        x, y = self.xy_arrays
        n = len(self.points_xy)
        for i in range(n):
            j = (i + 1) % n  # Ensure the loop wraps around to the first point
            common_factor = x[i] * y[j] - x[j] * y[i]
            sx += (x[i] + x[j]) * common_factor
            sy += (y[i] + y[j]) * common_factor
        factor = 1 / (6 * self.area)
        return Point(sx * factor, sy * factor, 0.0)

    @property
    def xy_arrays(self):
        x = [c[0] for c in self.points_xy]
        x.append(self.points_xy[0][0])
        y = [c[1] for c in self.points_xy]
        y.append(self.points_xy[0][1])
        return x, y

    @property
    def centroid(self):
        return self.centroid_xy.transformed(self._T.inverted())

    @property
    def frame(self):
        """Frame : compas Frame object at the centroid of the polygon"""
        return self._frame

    @property
    def Ixx(self):
        """float : moment of inertia about the x axis parallel to the global X axis and passing through the centroid."""
        return self.inertia_xy[0]

    @property
    def rx(self):
        """float : radius of inertia w.r.t. the x axis parallel to the global X axis and passing through the centroid.
        This value reppresents the distance from x at which is possible to concentrate the entire mass to get the same
        moment of inertia.
        """
        return self.radii[0]

    @property
    def Iyy(self):
        """float : moment of inertia about the y axis parallel to the global Y axis and passing through the centroid."""
        return self.inertia_xy[1]

    @property
    def ry(self):
        """float : radius of inertia w.r.t. the y axis parallel to the global Y axis and passing through the centroid.
        This value reppresents the distance from x at which is possible to concentrate the entire mass to get the same
        moment of inertia."""
        return self.radii[1]

    @property
    def Ixy(self):
        """float : product of inertia w.r.t. the x and y axes"""
        self.inertia_xy[2]

    @property
    def I1(self):
        """float : first principal moment of inertia."""
        return self.principal[1]

    @property
    def r1(self):
        """float : radius of inertia w.r.t. the 1st principal axis."""
        return self.principal_radii[0]

    @property
    def I2(self):
        """float : second principal moment of inertia."""
        return self.principal[2]

    @property
    def r2(self):
        """float : radius of inertia w.r.t. the 2nd principal axis."""
        return self.principal_radii[1]

    @property
    def theta(self):
        """float : angle (in radians) between the first principal inertia axis ant the x axis."""
        return self.principal[3]

    @property
    def Avx(self):
        return self._Avx

    @property
    def Avy(self):
        return self._Avy

    @property
    def g0(self):
        return self._g0

    @property
    def gw(self):
        return self._gw

    @property
    def J(self):
        return self._J


    # ==========================================================================
    # Methods
    # ==========================================================================

    @property
    def inertia_xy(self):
        """Compute the moments and product of inertia about the centroid."""
        x, y = self.xy_arrays
        n = len(self.points)
        sum_x = sum_y = sum_xy = 0.0
        for i in range(n):
            j = (i + 1) % n
            a = x[i] * y[j] - x[j] * y[i]
            sum_x += (y[i] ** 2 + y[i] * y[j] + y[j] ** 2) * a
            sum_y += (x[i] ** 2 + x[i] * x[j] + x[j] ** 2) * a
            sum_xy += (x[i] * y[j] + 2 * x[i] * y[i] + 2 * x[j] * y[j] + x[j] * y[i]) * a
        area = self.area
        centroid_x, centroid_y, _ = self.centroid_xy
        factor = 1 / 12
        return (sum_x * factor - area * centroid_y**2,
                sum_y * factor - area * centroid_x**2,
                sum_xy / 24 - area * centroid_x * centroid_y)

    @property
    def radii(self):
        """Compute the radii of inertia."""
        Ixx, Iyy, _ = self.inertia_xy
        return sqrt(Ixx / self.area), sqrt(Iyy / self.area)

    @property
    def principal_radii(self):
        """Compute the radii of inertia."""
        I1, I2, _ = self.inertia_xy
        return sqrt(I1/ self.area), sqrt(I2 / self.area)

    @property
    def principal(self):
        """Compute the principal moments of inertia and the orientation of the principal axes."""
        Ixx, Iyy, Ixy = self.inertia_xy
        avg = (Ixx + Iyy) / 2
        diff = (Ixx - Iyy) / 2  # signed
        # theta = -atan(2*self.Jxy/(self.Jx - self.Jy))/2
        theta = atan2(-Ixy, diff) / 2
        I1 = avg + sqrt(diff**2 + Ixy**2)
        I2 = avg - sqrt(diff**2 + Ixy**2)
        return I1, I2, theta

    def translated(self, vector):
        T = Translation.from_vector(vector)
        frame = Frame.from_transformation(T)
        return Shape([point.transformed(T) for point in self._points], frame)

    def oriented(self, frame):
        T = Transformation.from_frame_to_frame(self._frame, frame)
        return Shape([point.transformed(T) for point in self._points], frame)

    # ==========================================================================
    # Reppresentation
    # ==========================================================================

    def summary(self):
        """Provide a text summary of cross-sectional properties."""
        props = (self.area, self.centroid[0], self.centroid[1], self.Ixx, self.Iyy, self.Ixy, self.rx, self.ry, self.J1, self.J2, self.r1, self.r2, degrees(self.theta))
        props = [round(prop, 2) for prop in props]

        summ = """
    Area
    A       = {}

    Centroid
    cx      = {}
    cy      = {}

    Moments and product of inertia about the centroid
    Igx     = {}
    Igy     = {}
    Igxy    = {}
    rx      = {}
    ry      = {}

    Principal moments of inertia about the centroid
    I1      = {}
    I2      = {}
    r1      = {}
    r2      = {}
    θ︎       = {}°
    """.format(
            *props
        )
        return summ


class Rectangle(Shape):
    def __init__(self, w, h):
        self.__name__ = "Rectangle"
        self._w = w
        self._h = h
        points = [Point(-self.w / 2, -self.h / 2.0, 0.0), Point(self.w / 2, -self.h / 2.0, 0.0), Point(self.w / 2, self.h / 2.0, 0.0), Point(-self.w / 2, self.h / 2.0, 0.0)]
        super().__init__(points=points)
        self._Avy = 0.833 * self.area
        self._Avx = 0.833 * self.area
        l1 = max([w, h])
        l2 = min([w, h])
        self._J = (l1 * l2**3) * (0.33333 - 0.21 * (l2 / l1) * (1 - (l2**4) / (l2 * l1**4)))
        self._g0 = 0  # FIXME
        self._gw = 0  # FIXME

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h


class Rhombus(Shape):
    def __init__(self, a, b):
        self.__name__ = "Rhombus"
        self._a = a
        self._b = b
        points = [Point(0.0, -b / 2, 0.0), Point(a / 2, 0.0, 0.0), Point(0.0, b / 2, 0.0), Point(-a / 2, 0.0, 0.0)]
        super().__init__(points)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


class UShape(Shape):
    def __init__(self, a, b, t1, t2, t3, direction="up"):
        self.__name__ = "U-shape_" + direction
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._t3 = t3
        self._direction = direction
        points = [
            Point(-a / 2, -b / 2, 0.0),
            Point(a / 2, -b / 2, 0.0),
            Point(a / 2, b / 2, 0.0),
            Point(a / 2 - t3, b / 2, 0.0),
            Point(a / 2 - t3, t2 - b / 2, 0.0),
            Point(t1 - a / 2, t2 - b / 2, 0.0),
            Point(t1 - a / 2, b / 2, 0.0),
            Point(-a / 2, b / 2, 0.0),
        ]
        super().__init__(points)

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, a):
        self._a = a
        self.points = self._set_points()

    @property
    def b(self):
        return self._b

    @property
    def t1(self):
        return self._t1

    @property
    def t2(self):
        return self._t2

    @property
    def t3(self):
        return self._t3


class TShape(Shape):
    def __init__(self, a, b, t1, t2, direction="up"):
        super(Shape, self).__init__()
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._direction = direction
        self._type = "U-shape_" + direction
        points = [
            Point(-a / 2, -b / 2, 0.0),
            Point(a / 2, -b / 2, 0.0),
            Point(a / 2, t1 - b / 2, 0.0),
            Point((a + t2) / 2 - a / 2, t1 - b / 2, 0.0),
            Point((a + t2) / 2 - a / 2, b / 2, 0.0),
            Point((a - t2) / 2 - a / 2, b / 2, 0.0),
            Point((a - t2) / 2 - a / 2, t1 - b / 2, 0.0),
            Point(-a / 2, t1 - b / 2, 0.0),
        ]
        super().__init__(points)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def t1(self):
        return self._t1

    @property
    def t2(self):
        return self._t2


class IShape(Shape):
    def __init__(self, a, b, t1, t2, t3, direction="up"):
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._t3 = t3
        self._direction = direction
        self._type = "I-shape_" + direction
        points = [
            Point(-a/2, -b/2, 0.0),
            Point(a/2, -b/2, 0.0),
            Point(a/2, -b/2+t2, 0.0),
            Point(t1/2, -b/2+t2, 0.0),
            Point(t1/2, b/2-t2, 0.0),
            Point(a/2, b/2-t2, 0.0),
            Point(a/2, b/2, 0.0),
            Point(-a/2, b/2, 0.0),
            Point(-a/2, b/2-t2, 0.0),
            Point(-t1/2, b/2-t2, 0.0),
            Point(-t1/2, -b/2+t2, 0.0),
            Point(-a/2, -b/2+t2, 0.0)
        ]
        super().__init__(points)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def t1(self):
        return self._t1

    @property
    def t2(self):
        return self._t2

    @property
    def t3(self):
        return self._t3


class LShape(Shape):
    def __init__(self, a, b, t1, t2, direction="up"):
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._direction = direction
        self._type = "L-shape_" + direction
        points = [
            Point(-a / 2, -b / 2, 0.0),
            Point(a / 2, -b / 2, 0.0),
            Point(a / 2, t1 - b / 2, 0.0),
            Point(t2 - a / 2, t1 - b / 2, 0.0),
            Point(t2 - a / 2, b / 2, 0.0),
            Point(-a / 2, b / 2, 0.0),
        ]
        super().__init__(points)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def t1(self):
        return self._t1

    @property
    def t2(self):
        return self._t2


class CShape(Shape):
    def __init__(self, height, flange_width, web_thickness, flange_thickness):
        super().__init__()
        self._height = height
        self._flange_width = flange_width
        self._web_thickness = web_thickness
        self._flange_thickness = flange_thickness
        self._hw = self._web_thickness / 2  # Half web thickness
        self._hf = self._flange_width  # Full flange width
        self._h = self._height
        self._ft = self._flange_thickness
        points = [
            Point(0, 0, 0),
            Point(self._hf, 0, 0),
            Point(self._hf, self._ft, 0),
            Point(self._hw, self._ft, 0),
            Point(self._hw, self._h - self._ft, 0),
            Point(self._hf, self._h - self._ft, 0),
            Point(self._hf, self._h, 0),
            Point(0, self._h, 0),
        ]
        super().__init__(points)


class CustomI(Shape):
    def __init__(self, height, top_flange_width, bottom_flange_width, web_thickness, top_flange_thickness, bottom_flange_thickness):
        self._height = height
        self._top_flange_width = top_flange_width
        self._bottom_flange_width = bottom_flange_width
        self._web_thickness = web_thickness
        self._top_flange_thickness = top_flange_thickness
        self._bottom_flange_thickness = bottom_flange_thickness
        self._points = self._set_points()

        htf = self._top_flange_width / 2
        hbf = self._bottom_flange_width / 2
        hw = self._web_thickness / 2
        # Calculate shifts to center the shape on (0,0)
        shift_x = hw / 2
        shift_y = self._height / 2
        points = [
            Point(-hbf - shift_x, -shift_y, 0),
            Point(hbf - shift_x, -shift_y, 0),
            Point(hbf - shift_x, self._bottom_flange_thickness - shift_y, 0),
            Point(hw - shift_x, self._bottom_flange_thickness - shift_y, 0),
            Point(hw - shift_x, self._height - self._top_flange_thickness - shift_y, 0),
            Point(htf - shift_x, self._height - self._top_flange_thickness - shift_y, 0),
            Point(htf - shift_x, self._height - shift_y, 0),
            Point(-htf - shift_x, self._height - shift_y, 0),
            Point(-htf - shift_x, self._height - self._top_flange_thickness - shift_y, 0),
            Point(-hw - shift_x, self._height - self._top_flange_thickness - shift_y, 0),
            Point(-hw - shift_x, self._bottom_flange_thickness - shift_y, 0),
            Point(-hbf - shift_x, self._bottom_flange_thickness - shift_y, 0),
        ]
        super().__init__(points)


class Star(Shape):
    def __init__(
        self,
        a,
        b,
        c,
    ):
        super(Shape, self).__init__()
        self._a = a
        self._b = b
        self._c = c
        self._type = "Star"
        self._points = self._set_points()

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, a):
        self._a = a
        self.points = self._set_points()

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, b):
        self._b = b
        self.points = self._set_points()

    @property
    def c(self):
        return self._c

    @c.setter
    def t(self, c):
        self._c = c
        self.points = self._set_points()

    @property
    def points(self):
        return self._points

    def _set_points(self):
        return [
            Point(0.0, 0.0, 0.0),
            Point(self.a / 2, self.c, 0.0),
            Point(self.a, 0.0, 0.0),
            Point((self.a - self.c), self.b / 2, 0.0),
            Point(self.a, self.b, 0.0),
            Point(self.a / 2, self.b - self.c, 0.0),
            Point(0.0, self.b, 0.0),
            Point(self.c, self.b / 2, 0.0),
        ]


class Circle(Shape):
    def __init__(self, radius, segments=32):
        super().__init__()
        self._radius = radius
        self._segments = segments
        self._points = self._set_points()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        self._points = self._set_points()

    def _set_points(self):
        return [Point(self._radius * np.cos(theta), self._radius * np.sin(theta), 0.0) for theta in np.linspace(0, 2 * np.pi, self._segments, endpoint=False)]


class Ellipse(Shape):
    def __init__(self, radius_a, radius_b, segments=32):
        super().__init__()
        self._radius_a = radius_a
        self._radius_b = radius_b
        self._segments = segments
        self._points = self._set_points()

    @property
    def radius_a(self):
        return self._radius_a

    @radius_a.setter
    def radius_a(self, radius_a):
        self._radius_a = radius_a
        self._points = self._set_points()

    @property
    def radius_b(self):
        return self._radius_b

    @radius_b.setter
    def radius_b(self, radius_b):
        self._radius_b = radius_b
        self._points = self._set_points()

    def _set_points(self):
        return [Point(self._radius_a * np.cos(theta), self._radius_b * np.sin(theta), 0.0) for theta in np.linspace(0, 2 * np.pi, self._segments, endpoint=False)]


class Hexagon(Shape):
    def __init__(self, side_length):
        super().__init__()
        self._side_length = side_length
        self._points = self._set_points()

    @property
    def side_length(self):
        return self._side_length

    @side_length.setter
    def side_length(self, side_length):
        self._side_length = side_length
        self._points = self._set_points()

    def _set_points(self):
        return [Point(self._side_length * np.cos(np.pi / 3 * i), self._side_length * np.sin(np.pi / 3 * i), 0.0) for i in range(6)]


class Pentagon(Shape):
    def __init__(self, circumradius):
        super().__init__()
        self._circumradius = circumradius
        self._points = self._set_points()

    def _set_points(self):
        angle = 2 * np.pi / 5  # 360 degrees / 5
        return [Point(self._circumradius * np.cos(i * angle), self._circumradius * np.sin(i * angle), 0.0) for i in range(5)]


class Octagon(Shape):
    def __init__(self, circumradius):
        super().__init__()
        self._circumradius = circumradius
        self._points = self._set_points()

    def _set_points(self):
        angle = 2 * np.pi / 8  # 360 degrees / 8
        return [Point(self._circumradius * np.cos(i * angle), self._circumradius * np.sin(i * angle), 0.0) for i in range(8)]


class Triangle(Shape):
    def __init__(self, circumradius):
        super().__init__()
        self._circumradius = circumradius
        self._points = self._set_points()

    def _set_points(self):
        angle = 2 * np.pi / 3  # 360 degrees / 3
        return [Point(self._circumradius * np.cos(i * angle), self._circumradius * np.sin(i * angle), 0.0) for i in range(3)]


class Parallelogram(Shape):
    def __init__(self, width, height, angle):
        super().__init__()
        self._width = width
        self._height = height
        self._angle = angle  # Angle in radians between the base and the adjacent side
        self._points = self._set_points()

    def _set_points(self):
        dx = self._height * np.sin(self._angle)
        dy = self._height * np.cos(self._angle)
        return [Point(0, 0, 0), Point(self._width, 0, 0), Point(self._width + dx, dy, 0), Point(dx, dy, 0)]


class Trapezoid(Shape):
    def __init__(self, top_width, bottom_width, height):
        super().__init__()
        self._top_width = top_width
        self._bottom_width = bottom_width
        self._height = height
        self._points = self._set_points()

    def _set_points(self):
        dx = (self._bottom_width - self._top_width) / 2
        return [Point(dx, 0, 0), Point(dx + self._top_width, 0, 0), Point(self._bottom_width, self._height, 0), Point(0, self._height, 0)]


if __name__ == "__main__":
    r = Rectangle(w=100, h=300)
    # t = TShape(10, 20, 3, 5)
    # u = UShape(10, 20, 3, 5, 4)
    # s = Star(10, 10, 2)
    # circle = Circle(5)
    # ellipse = Ellipse(10, 5)
    # hexagon = Hexagon(3)

    # print(circle)
    # print(ellipse)
    # print(hexagon)

    r_transf = r.oriented(Frame([0, 0, 1000], [1, 0, 0], [0, 1, 0]))
    print(r_transf.points)

    m1 = r.to_mesh()
    m2 = r_transf.to_mesh()
