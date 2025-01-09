from compas.geometry import Point, Frame, Translation, Transformation, Rotation, Polygon
from compas.datastructures import Mesh
from compas_fea2.base import FEAData

import numpy as np
from math import degrees, sqrt, atan2, pi


class Shape(Polygon, FEAData):
    def __init__(self, points, frame=None, check_planarity=True):
        super().__init__(points)
        if not self.is_planar and check_planarity:
            raise ValueError("The points must belong to the same plane")
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
    number of edges:    {len(self._points)}  # Assuming closed polygon
        """

    # ==========================================================================
    # Properties
    # ==========================================================================
    @property
    def points_xy(self):
        """Coordinates of the polygon’s points in the worldXY frame."""
        return [p.transformed(self._T) for p in self.points]

    @property
    def A(self):
        """Area of the shape."""
        return self.area

    @property
    def centroid_xy(self):
        """Compute the centroid in the worldXY plane."""
        sx = sy = 0
        x, y = self.xy_arrays
        n = len(self.points_xy)
        for i in range(n):
            j = (i + 1) % n
            common_factor = x[i] * y[j] - x[j] * y[i]
            sx += (x[i] + x[j]) * common_factor
            sy += (y[i] + y[j]) * common_factor
        factor = 1 / (6 * self.area)
        return Point(sx * factor, sy * factor, 0.0)

    @property
    def xy_arrays(self):
        """Convenience arrays for X and Y of the shape points in worldXY."""
        x = [c[0] for c in self.points_xy]
        x.append(self.points_xy[0][0])
        y = [c[1] for c in self.points_xy]
        y.append(self.points_xy[0][1])
        return x, y

    @property
    def centroid(self):
        """Centroid in the shape’s local frame (undoing T)."""
        return self.centroid_xy.transformed(self._T.inverted())

    @property
    def frame(self):
        """Shape’s local frame (compas Frame object)."""
        return self._frame

    @property
    def Ixx(self):
        """Moment of inertia about the local x-axis (through centroid)."""
        return self.inertia_xy[0]

    @property
    def rx(self):
        """Radius of inertia w.r.t. the local x-axis (through centroid)."""
        return self.radii[0]

    @property
    def Iyy(self):
        """Moment of inertia about the local y-axis (through centroid)."""
        return self.inertia_xy[1]

    @property
    def ry(self):
        """Radius of inertia w.r.t. the local y-axis (through centroid)."""
        return self.radii[1]

    @property
    def Ixy(self):
        """Product of inertia w.r.t. local x and y axes."""
        return self.inertia_xy[2]

    @property
    def I1(self):
        """First principal moment of inertia."""
        return self.principal[0]

    @property
    def I2(self):
        """Second principal moment of inertia."""
        return self.principal[1]

    @property
    def theta(self):
        """
        Angle (in radians) between the first principal inertia axis and the local x-axis.
        Positive angle indicates rotation from x-axis towards y-axis.
        """
        return self.principal[2]

    @property
    def r1(self):
        """Radius of inertia w.r.t. the 1st principal axis."""
        return self.principal_radii[0]

    @property
    def r2(self):
        """Radius of inertia w.r.t. the 2nd principal axis."""
        return self.principal_radii[1]

    @property
    def Avx(self):
        """Shear area in the x-direction."""
        return self._Avx

    @property
    def Avy(self):
        """Shear area in the y-direction."""
        return self._Avy

    @property
    def g0(self):
        """Shear modulus in the x-y plane."""
        return self._g0

    @property
    def gw(self):
        """Shear modulus in the x-z plane."""
        return self._gw

    @property
    def J(self):
        """Torsional constant."""
        return self._J

    # ==========================================================================
    # Methods
    # ==========================================================================
    @property
    def inertia_xy(self):
        """Compute the moments and product of inertia about the centroid (local x, y)."""
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
        cx, cy, _ = self.centroid_xy
        factor = 1 / 12
        Ixx = sum_x * factor - area * cy**2
        Iyy = sum_y * factor - area * cx**2
        Ixy = (sum_xy / 24) - area * cx * cy
        return (Ixx, Iyy, Ixy)

    @property
    def radii(self):
        """Compute the radii of inertia w.r.t. local x and y axes."""
        Ixx, Iyy, _ = self.inertia_xy
        return (sqrt(Ixx / self.area), sqrt(Iyy / self.area))

    @property
    def principal_radii(self):
        """Compute the radii of inertia w.r.t. the principal axes."""
        I1, I2, _ = self.principal
        return (sqrt(I1 / self.area), sqrt(I2 / self.area))

    @property
    def principal(self):
        """
        Compute the principal moments of inertia and the orientation (theta)
        of the principal axes.
        Returns (I1, I2, theta).
        """
        Ixx, Iyy, Ixy = self.inertia_xy
        avg = (Ixx + Iyy) / 2
        diff = (Ixx - Iyy) / 2
        theta = atan2(-Ixy, diff) / 2
        radius = sqrt(diff**2 + Ixy**2)
        I1 = avg + radius
        I2 = avg - radius
        return (I1, I2, theta)

    def translated(self, vector, check_planarity=True):
        """Return a translated copy of the shape."""
        T = Translation.from_vector(vector)
        new_frame = Frame.from_transformation(T)
        return Shape([point.transformed(T) for point in self._points], new_frame, check_planarity=check_planarity)

    def oriented(self, frame, check_planarity=True):
        """Return a shape oriented to a new frame."""
        from math import pi

        T = Transformation.from_frame_to_frame(self._frame, frame) * Rotation.from_axis_and_angle([1, 0, 0], pi / 2)
        return Shape([point.transformed(T) for point in self._points], frame, check_planarity=check_planarity)

    def summary(self):
        """Provide a text summary of cross-sectional properties."""
        props = (
            self.A,
            self.centroid[0],
            self.centroid[1],
            self.Ixx,
            self.Iyy,
            self.Ixy,
            self.rx,
            self.ry,
            self.I1,
            self.I2,
            self.r1,
            self.r2,
            degrees(self.theta),
        )
        props = [round(prop, 2) for prop in props]

        summ = f"""
    Area
    A       = {props[0]}

    Centroid
    cx      = {props[1]}
    cy      = {props[2]}

    Moments and product of inertia about the centroid
    Ixx     = {props[3]}
    Iyy     = {props[4]}
    Ixy     = {props[5]}
    rx      = {props[6]}
    ry      = {props[7]}

    Principal moments of inertia about the centroid
    I1      = {props[8]}
    I2      = {props[9]}
    r1      = {props[10]}
    r2      = {props[11]}
    θ       = {props[12]}°
    """
        return summ

    def to_mesh(self):
        """Convert the shape to a mesh."""
        vertices = [point for point in self.points]
        faces = [list(range(len(vertices)))]
        return Mesh.from_vertices_and_faces(vertices, faces)


class Rectangle(Shape):
    def __init__(self, w, h, frame=None):
        self._w = w
        self._h = h
        points = [
            Point(-w / 2, -h / 2, 0.0),
            Point(w / 2, -h / 2, 0.0),
            Point(w / 2, h / 2, 0.0),
            Point(-w / 2, h / 2, 0.0),
        ]
        super().__init__(points, frame=frame)
        self._Avy = 0.833 * self.area  # TODO: Check this
        self._Avx = 0.833 * self.area  # TODO: Check this
        l1 = max(w, h)
        l2 = min(w, h)
        self._J = (l1 * l2**3) * (0.33333 - 0.21 * (l2 / l1) * (1 - (l2**4) / (l2 * l1**4)))
        self._g0 = 0  # Placeholder
        self._gw = 0  # Placeholder

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h


class Rhombus(Shape):
    def __init__(self, a, b, frame=None):
        self._a = a
        self._b = b
        points = [
            Point(0.0, -b / 2, 0.0),
            Point(a / 2, 0.0, 0.0),
            Point(0.0, b / 2, 0.0),
            Point(-a / 2, 0.0, 0.0),
        ]
        super().__init__(points, frame=frame)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b


class UShape(Shape):
    def __init__(self, a, b, t1, t2, t3, direction="up", frame=None):
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
        super().__init__(points, frame=frame)

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


class TShape(Shape):
    def __init__(self, a, b, t1, t2, direction="up", frame=None):
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._direction = direction
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
        super().__init__(points, frame=frame)

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
    def __init__(self, w, h, tw, tbf, ttf, direction="up", frame=None):
        self._w = w
        self._h = h
        self._tw = tw
        self._tbf = tbf
        self._ttf = ttf
        self._direction = direction
        points = [
            Point(-w / 2, -h / 2, 0.0),
            Point(w / 2, -h / 2, 0.0),
            Point(w / 2, -h / 2 + tbf, 0.0),
            Point(tw / 2, -h / 2 + tbf, 0.0),
            Point(tw / 2, h / 2 - tbf, 0.0),
            Point(w / 2, h / 2 - tbf, 0.0),
            Point(w / 2, h / 2, 0.0),
            Point(-w / 2, h / 2, 0.0),
            Point(-w / 2, h / 2 - ttf, 0.0),
            Point(-tw / 2, h / 2 - ttf, 0.0),
            Point(-tw / 2, -h / 2 + ttf, 0.0),
            Point(-w / 2, -h / 2 + ttf, 0.0),
        ]
        super().__init__(points, frame=frame)

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def tw(self):
        return self._tw

    @property
    def tbf(self):
        return self._tbf

    @property
    def ttf(self):
        return self._ttf

    @property
    def J(self):
        """Torsional constant approximation."""
        return (1 / 3) * (self.w * (self.tbf**3 + self.ttf**3) + (self.h - self.tbf - self.ttf) * self.tw**3)


class LShape(Shape):
    def __init__(self, a, b, t1, t2, direction="up", frame=None):
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._direction = direction
        points = [
            Point(-a / 2, -b / 2, 0.0),
            Point(a / 2, -b / 2, 0.0),
            Point(a / 2, t1 - b / 2, 0.0),
            Point(t2 - a / 2, t1 - b / 2, 0.0),
            Point(t2 - a / 2, b / 2, 0.0),
            Point(-a / 2, b / 2, 0.0),
        ]
        super().__init__(points, frame=frame)

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
    def __init__(self, height, flange_width, web_thickness, flange_thickness, frame=None):
        self._height = height
        self._flange_width = flange_width
        self._web_thickness = web_thickness
        self._flange_thickness = flange_thickness
        hw = self._web_thickness / 2.0
        hf = self._flange_width
        h = self._height
        ft = self._flange_thickness
        points = [
            Point(0, 0, 0),
            Point(hf, 0, 0),
            Point(hf, ft, 0),
            Point(hw, ft, 0),
            Point(hw, h - ft, 0),
            Point(hf, h - ft, 0),
            Point(hf, h, 0),
            Point(0, h, 0),
        ]
        super().__init__(points, frame=frame)


class CustomI(Shape):
    def __init__(self, height, top_flange_width, bottom_flange_width, web_thickness, top_flange_thickness, bottom_flange_thickness, frame=None):
        self._height = height
        self._top_flange_width = top_flange_width
        self._bottom_flange_width = bottom_flange_width
        self._web_thickness = web_thickness
        self._top_flange_thickness = top_flange_thickness
        self._bottom_flange_thickness = bottom_flange_thickness

        htf = top_flange_width / 2
        hbf = bottom_flange_width / 2
        hw = web_thickness / 2
        # shifts for centering
        shift_x = hw / 2
        shift_y = height / 2
        points = [
            Point(-hbf - shift_x, -shift_y, 0),
            Point(hbf - shift_x, -shift_y, 0),
            Point(hbf - shift_x, bottom_flange_thickness - shift_y, 0),
            Point(hw - shift_x, bottom_flange_thickness - shift_y, 0),
            Point(hw - shift_x, height - top_flange_thickness - shift_y, 0),
            Point(htf - shift_x, height - top_flange_thickness - shift_y, 0),
            Point(htf - shift_x, height - shift_y, 0),
            Point(-htf - shift_x, height - shift_y, 0),
            Point(-htf - shift_x, height - top_flange_thickness - shift_y, 0),
            Point(-hw - shift_x, height - top_flange_thickness - shift_y, 0),
            Point(-hw - shift_x, bottom_flange_thickness - shift_y, 0),
            Point(-hbf - shift_x, bottom_flange_thickness - shift_y, 0),
        ]
        super().__init__(points, frame=frame)


class Star(Shape):
    def __init__(self, a, b, c, frame=None):
        self._a = a
        self._b = b
        self._c = c
        points = self._set_points()
        super().__init__(points, frame=frame)

    def _set_points(self):
        return [
            Point(0.0, 0.0, 0.0),
            Point(self._a / 2, self._c, 0.0),
            Point(self._a, 0.0, 0.0),
            Point(self._a - self._c, self._b / 2, 0.0),
            Point(self._a, self._b, 0.0),
            Point(self._a / 2, self._b - self._c, 0.0),
            Point(0.0, self._b, 0.0),
            Point(self._c, self._b / 2, 0.0),
        ]

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, val):
        self._a = val
        self.points = self._set_points()

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, val):
        self._b = val
        self.points = self._set_points()

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, val):
        self._c = val
        self.points = self._set_points()


class Circle(Shape):
    def __init__(self, radius, segments=32, frame=None):
        self._radius = radius
        self._segments = segments
        points = self._set_points()
        super().__init__(points, frame=frame)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, val):
        self._radius = val
        self.points = self._set_points()

    def _set_points(self):
        return [Point(self._radius * np.cos(theta), self._radius * np.sin(theta), 0.0) for theta in np.linspace(0, 2 * pi, self._segments, endpoint=False)]


class Ellipse(Shape):
    def __init__(self, radius_a, radius_b, segments=32, frame=None):
        self._radius_a = radius_a
        self._radius_b = radius_b
        self._segments = segments
        points = self._set_points()
        super().__init__(points, frame=frame)

    @property
    def radius_a(self):
        return self._radius_a

    @radius_a.setter
    def radius_a(self, val):
        self._radius_a = val
        self.points = self._set_points()

    @property
    def radius_b(self):
        return self._radius_b

    @radius_b.setter
    def radius_b(self, val):
        self._radius_b = val
        self.points = self._set_points()

    def _set_points(self):
        return [Point(self._radius_a * np.cos(theta), self._radius_b * np.sin(theta), 0.0) for theta in np.linspace(0, 2 * pi, self._segments, endpoint=False)]


class Hexagon(Shape):
    def __init__(self, side_length, frame=None):
        self._side_length = side_length
        points = self._set_points()
        super().__init__(points, frame=frame)

    def _set_points(self):
        return [Point(self._side_length * np.cos(np.pi / 3 * i), self._side_length * np.sin(np.pi / 3 * i), 0.0) for i in range(6)]

    @property
    def side_length(self):
        return self._side_length

    @side_length.setter
    def side_length(self, val):
        self._side_length = val
        self.points = self._set_points()


class Pentagon(Shape):
    def __init__(self, circumradius, frame=None):
        self._circumradius = circumradius
        points = self._set_points()
        super().__init__(points, frame=frame)

    def _set_points(self):
        angle = 2 * pi / 5
        return [Point(self._circumradius * np.cos(i * angle), self._circumradius * np.sin(i * angle), 0.0) for i in range(5)]


class Octagon(Shape):
    def __init__(self, circumradius, frame=None):
        self._circumradius = circumradius
        points = self._set_points()
        super().__init__(points, frame=frame)

    def _set_points(self):
        angle = 2 * pi / 8
        return [Point(self._circumradius * np.cos(i * angle), self._circumradius * np.sin(i * angle), 0.0) for i in range(8)]


class Triangle(Shape):
    def __init__(self, circumradius, frame=None):
        self._circumradius = circumradius
        points = self._set_points()
        super().__init__(points, frame=frame)

    def _set_points(self):
        angle = 2 * pi / 3
        return [Point(self._circumradius * np.cos(i * angle), self._circumradius * np.sin(i * angle), 0.0) for i in range(3)]


class Parallelogram(Shape):
    def __init__(self, width, height, angle, frame=None):
        self._width = width
        self._height = height
        self._angle = angle  # radians
        points = self._set_points()
        super().__init__(points, frame=frame)

    def _set_points(self):
        dx = self._height * np.sin(self._angle)
        dy = self._height * np.cos(self._angle)
        return [
            Point(0, 0, 0),
            Point(self._width, 0, 0),
            Point(self._width + dx, dy, 0),
            Point(dx, dy, 0),
        ]


class Trapezoid(Shape):
    def __init__(self, top_width, bottom_width, height, frame=None):
        self._top_width = top_width
        self._bottom_width = bottom_width
        self._height = height
        points = self._set_points()
        super().__init__(points, frame=frame)

    def _set_points(self):
        dx = (self._bottom_width - self._top_width) / 2
        return [
            Point(dx, 0, 0),
            Point(dx + self._top_width, 0, 0),
            Point(self._bottom_width, self._height, 0),
            Point(0, self._height, 0),
        ]
