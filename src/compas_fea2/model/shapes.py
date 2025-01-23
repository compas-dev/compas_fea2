import math
from math import atan2, degrees, pi, sqrt
from functools import cached_property
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.lines import Line2D
from compas.geometry import Point

import numpy as np

from compas.datastructures import Mesh
from compas.geometry import (
    Frame,
    Polygon,
    Rotation,
    Transformation,
    Translation,
)
from compas_fea2.base import FEAData


class Shape(Polygon, FEAData):
    """
    A base class representing a planar polygonal shape for FEA,
    providing computed properties like area, centroid, and inertia.

    This class:
      - Inherits from `compas.geometry.Polygon` for geometric functionality.
      - Implements FEAData to integrate with compas_fea2.
      - Maintains its own local frame and transformations.
      - Caches computed properties (area, centroid, inertia, etc.) to avoid
        repeated recalculations.

    References:
      - NASA: https://www.grc.nasa.gov/www/k-12/airplane/areas.html
      - Wikipedia: https://en.wikipedia.org/wiki/Second_moment_of_area
    """

    def __init__(self, points: List[Point], frame: Optional[Frame] = None, check_planarity: bool = True):
        super().__init__(points)
        if not self.is_planar and check_planarity:
            raise ValueError("The points must lie in the same plane.")

        # Store local frame, default = worldXY
        self._frame = frame or Frame.worldXY()

        # Transformation from local frame to world XY
        self._T = Transformation.from_frame_to_frame(self._frame, Frame.worldXY())

    def __str__(self) -> str:
        return f"""
    type:               {self.__class__.__name__}
    number of points:   {len(self._points)}
    number of edges:    {len(self._points)}  # (closed polygon)
        """

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------
    @cached_property
    def area(self) -> float:
        """Area of the shape in the local plane (inherited from `Polygon`)."""
        return super().area

    @property
    def A(self) -> float:
        """Alias for area."""
        return self.area

    @cached_property
    def points_xy(self) -> List[Point]:
        """Coordinates of the polygon’s points in the worldXY frame."""
        return [p.transformed(self._T) for p in self.points]

    @property
    def xy_arrays(self) -> Tuple[List[float], List[float]]:
        """
        Convenience arrays for X and Y of the shape's points in worldXY,
        appending the first point again to close the loop.
        """
        x_vals = [pt.x for pt in self.points_xy]
        y_vals = [pt.y for pt in self.points_xy]
        # append the first point to close
        x_vals.append(x_vals[0])
        y_vals.append(y_vals[0])
        return x_vals, y_vals

    @cached_property
    def centroid_xy(self) -> Point:
        """
        Centroid of the polygon in the worldXY plane.

        Formula reference (polygon centroid):
          - NASA: https://www.grc.nasa.gov/www/k-12/airplane/areas.html
        """
        x, y = self.xy_arrays
        n = len(self.points_xy)
        sx = sy = 0.0
        for i in range(n):
            j = (i + 1) % n
            cross = x[i] * y[j] - x[j] * y[i]
            sx += (x[i] + x[j]) * cross
            sy += (y[i] + y[j]) * cross
        factor = 1.0 / (6.0 * self.area)
        return Point(sx * factor, sy * factor, 0.0)

    @property
    def centroid(self) -> Point:
        """Centroid in the shape’s local frame (undoing `self._T`)."""
        return self.centroid_xy.transformed(self._T.inverted())

    @property
    def frame(self) -> Frame:
        """Shape’s local frame."""
        return self._frame

    # --------------------------------------------------------------------------
    # Second moment of area (inertia) and related
    # --------------------------------------------------------------------------
    @cached_property
    def inertia_xy(self) -> Tuple[float, float, float]:
        """
        (Ixx, Iyy, Ixy) about the centroid in the local x-y plane (units: length^4).

        Formula reference (polygon second moments):
          - NASA: https://www.grc.nasa.gov/www/k-12/airplane/areas.html
        """
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
        factor = 1.0 / 12.0

        Ixx = sum_x * factor - area * (cy**2)
        Iyy = sum_y * factor - area * (cx**2)
        Ixy = (sum_xy / 24.0) - area * cx * cy
        return (Ixx, Iyy, Ixy)

    @property
    def Ixx(self) -> float:
        """Moment of inertia about local x-axis (through centroid)."""
        return self.inertia_xy[0]

    @property
    def Iyy(self) -> float:
        """Moment of inertia about local y-axis (through centroid)."""
        return self.inertia_xy[1]

    @property
    def Ixy(self) -> float:
        """Product of inertia about local x and y axes (through centroid)."""
        return self.inertia_xy[2]

    @cached_property
    def radii(self) -> Tuple[float, float]:
        """Radii of gyration about local x and y axes."""
        Ixx, Iyy, _ = self.inertia_xy
        return (sqrt(Ixx / self.area), sqrt(Iyy / self.area))

    @property
    def rx(self) -> float:
        """Radius of gyration about local x-axis."""
        return self.radii[0]

    @property
    def ry(self) -> float:
        """Radius of gyration about local y-axis."""
        return self.radii[1]

    @cached_property
    def principal(self) -> Tuple[float, float, float]:
        """
        (I1, I2, theta): principal moments of inertia and
        the orientation of the principal axis (theta) from x-axis to I1.

        Angle sign convention: rotation from x-axis toward y-axis is positive.
        """
        Ixx, Iyy, Ixy = self.inertia_xy
        avg = 0.5 * (Ixx + Iyy)
        diff = 0.5 * (Ixx - Iyy)
        # angle
        theta = 0.5 * atan2(-Ixy, diff)
        # principal values
        radius = math.sqrt(diff**2 + Ixy**2)
        I1 = avg + radius  # TODO: check this
        I2 = avg - radius
        return (I1, I2, theta)

    @property
    def I1(self) -> float:
        """First principal moment of inertia."""
        return self.principal[0]

    @property
    def I2(self) -> float:
        """Second principal moment of inertia."""
        return self.principal[1]

    @property
    def theta(self) -> float:
        """
        Angle (radians) between the local x-axis and the axis of I1.
        Positive angle: rotation from x-axis toward y-axis.
        """
        return self.principal[2]

    @cached_property
    def principal_radii(self) -> Tuple[float, float]:
        """Radii of gyration about the principal axes."""
        I1, I2, _ = self.principal
        return (sqrt(I1 / self.area), sqrt(I2 / self.area))

    @property
    def r1(self) -> float:
        """Radius of gyration about the first principal axis."""
        return self.principal_radii[0]

    @property
    def r2(self) -> float:
        """Radius of gyration about the second principal axis."""
        return self.principal_radii[1]

    # --------------------------------------------------------------------------
    # Optional FEA properties
    # --------------------------------------------------------------------------
    @property
    def Avx(self) -> Optional[float]:
        """Shear area in the x-direction (if defined)."""
        raise NotImplementedError()

    @property
    def Avy(self) -> Optional[float]:
        """Shear area in the y-direction (if defined)."""
        raise NotImplementedError()

    @property
    def J(self):
        """Torsional constant (polar moment of inertia)."""
        raise NotImplementedError()

    # --------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------
    def translated(self, vector, check_planarity: bool = True) -> "Shape":
        """
        Return a translated copy of the shape.
        The new shape will have an updated frame.

        Args:
            vector: A translation vector.
            check_planarity: Whether to verify planarity of new shape.
        """
        T = Translation.from_vector(vector)
        new_frame = Frame.from_transformation(T)
        new_points = [pt.transformed(T) for pt in self._points]
        return Shape(new_points, new_frame, check_planarity=check_planarity)

    def oriented(self, frame: Frame, check_planarity: bool = True) -> "Shape":
        """
        Return a shape oriented to a new frame.
        Example: flipping or rotating the shape by a custom orientation.
        """
        rot = Rotation.from_axis_and_angle([1, 0, 0], pi / 2)
        T = Transformation.from_frame_to_frame(self._frame, frame) * rot
        new_points = [pt.transformed(T) for pt in self._points]
        return Shape(new_points, frame, check_planarity=check_planarity)

    def summary(self) -> str:
        """
        Provide a text summary of cross-sectional properties.
        Rounds the values to 2 decimals for convenience.
        """
        props = [
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
        ]
        props = [round(prop, 2) for prop in props]
        return f"""
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

    def to_mesh(self) -> Mesh:
        """Convert the shape to a compas Mesh."""
        vertices = self.points[:]  # polygon points
        faces = [list(range(len(vertices)))]
        return Mesh.from_vertices_and_faces(vertices, faces)

    def plot(
        self,
        fill: bool = True,
        facecolor: str = "#B0C4DE",  # light steel blue
        edgecolor: str = "#333333",  # dark gray
        centroid_color: str = "red",
        axis_color: str = "#555555",  # medium gray
        alpha: float = 0.6,
        figsize=(8, 6),
    ):
        # Use a clean style (white background, subtle grid)
        with plt.style.context("seaborn-v0_8-whitegrid"):
            fig, ax = plt.subplots(figsize=figsize)

            # ---------------------------------------------------------------------
            # 1) Polygon Patch
            # ---------------------------------------------------------------------
            pts_xy = self.points_xy  # world XY coordinates
            coords = [(p.x, p.y) for p in pts_xy]

            polygon = MplPolygon(coords, closed=True, fill=fill, facecolor=facecolor if fill else "none", edgecolor=edgecolor, alpha=alpha, linewidth=1.5)
            ax.add_patch(polygon)

            # ---------------------------------------------------------------------
            # 2) Centroid Marker
            # ---------------------------------------------------------------------
            c = self.centroid_xy
            ax.plot(c.x, c.y, marker="o", color=centroid_color, markersize=6, zorder=5)

            # ---------------------------------------------------------------------
            # 3) Principal Axes
            # ---------------------------------------------------------------------
            # We'll draw lines for I1 and I2 through the centroid with some length
            xs = [p.x for p in pts_xy]
            ys = [p.y for p in pts_xy]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            diag = math.hypot(max_x - min_x, max_y - min_y)
            axis_len = 0.5 * diag  # half the diagonal of bounding box

            theta = self.theta  # angle of I1 from local x-axis
            # I1 axis
            x_i1 = c.x + axis_len * math.cos(theta)
            y_i1 = c.y + axis_len * math.sin(theta)
            x_i1_neg = c.x - axis_len * math.cos(theta)
            y_i1_neg = c.y - axis_len * math.sin(theta)

            ax.add_line(Line2D([x_i1_neg, x_i1], [y_i1_neg, y_i1], color=axis_color, linestyle="--", linewidth=1.5, zorder=4))

            # I2 axis is perpendicular => theta + pi/2
            theta_2 = theta + math.pi / 2
            x_i2 = c.x + axis_len * math.cos(theta_2)
            y_i2 = c.y + axis_len * math.sin(theta_2)
            x_i2_neg = c.x - axis_len * math.cos(theta_2)
            y_i2_neg = c.y - axis_len * math.sin(theta_2)

            ax.add_line(Line2D([x_i2_neg, x_i2], [y_i2_neg, y_i2], color=axis_color, linestyle="--", linewidth=1.5, zorder=4))

            # ---------------------------------------------------------------------
            # 4) Annotations for Key Properties
            # ---------------------------------------------------------------------
            txt = (
                f"Shape: {self.__class__.__name__}\n"
                f"Area (A): {self.A:.2f}\n"
                f"Centroid: ({c.x:.2f}, {c.y:.2f})\n"
                f"Ixx: {self.Ixx:.2e}\n"
                f"Iyy: {self.Iyy:.2e}\n"
                f"Ixy: {self.Ixy:.2e}\n"
                f"I1: {self.I1:.2e}\n"
                f"I2: {self.I2:.2e}\n"
                f"Theta (deg): {math.degrees(theta):.2f}"
            )

        text_x = max_x + 0.1 * (max_x - min_x)
        text_y = max_y

        ax.text(text_x, text_y, txt, fontsize=9, verticalalignment="top", bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8), color="#333333")

        # -------------------------------------------------------------
        # 5) Final Touches
        # -------------------------------------------------------------
        ax.set_aspect("equal", "box")

        # Expand x-limits so text is visible on the right
        # We add an extra margin for the text box
        x_margin = 0.3 * (max_x - min_x)
        ax.set_xlim(min_x - 0.1 * diag, max_x + x_margin)
        # And a bit of margin on y-limits
        y_margin = 0.1 * (max_y - min_y) if (max_y - min_y) != 0 else 1.0
        ax.set_ylim(min_y - y_margin, max_y + y_margin)

        # Optional: remove ticks for a "clean" look
        # ax.set_xticks([])
        # ax.set_yticks([])

        plt.show()


# ------------------------------------------------------------------------------
# Below are specific shape subclasses. They override the constructor
# to set their own `_points` geometry but otherwise rely on the parent class.
# ------------------------------------------------------------------------------


class Circle(Shape):
    """
    A circular cross section defined by a radius and segmented approximation.
    """

    def __init__(self, radius: float, segments: int = 360, frame: Optional[Frame] = None):
        self._radius = radius
        self._segments = segments
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        thetas = np.linspace(0, 2 * pi, self._segments, endpoint=False)
        return [Point(self._radius * math.cos(t), self._radius * math.sin(t), 0.0) for t in thetas]

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, val: float):
        self._radius = val
        self.points = self._set_points()

    @property
    def segments(self) -> int:
        return self._segments

    @property
    def diameter(self) -> float:
        return 2 * self._radius

    @property
    def circumference(self) -> float:
        return 2 * pi * self._radius

    @property
    def J(self) -> float:
        """Polar moment of inertia for a circular cross-section."""
        return pi * self._radius**4 / 2

    @property
    def Avx(self) -> float:
        """Shear area in the x-direction."""
        return 9 / 10 * self.area

    @property
    def Avy(self) -> float:
        """Shear area in the y-direction."""
        return 9 / 10 * self.area


class Ellipse(Shape):
    """
    An elliptical cross section defined by two principal radii (radius_a, radius_b).
    """

    def __init__(self, radius_a: float, radius_b: float, segments: int = 32, frame: Optional[Frame] = None):
        self._radius_a = radius_a
        self._radius_b = radius_b
        self._segments = segments
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        thetas = np.linspace(0, 2 * pi, self._segments, endpoint=False)
        return [Point(self._radius_a * math.cos(t), self._radius_b * math.sin(t), 0.0) for t in thetas]

    @property
    def radius_a(self) -> float:
        return self._radius_a

    @radius_a.setter
    def radius_a(self, val: float):
        self._radius_a = val
        self.points = self._set_points()

    @property
    def radius_b(self) -> float:
        return self._radius_b

    @radius_b.setter
    def radius_b(self, val: float):
        self._radius_b = val
        self.points = self._set_points()

    @property
    def segments(self) -> int:
        return self._segments

    @property
    def J(self) -> float:
        return pi * self._radius_a * self._radius_b**3 / 2

    def _calculate_shear_area(self):
        """
        Calculate the shear area (A_s) of a solid elliptical cross-section along x and y axes.

        Parameters:
            a (float): Semi-major axis of the ellipse (longer radius).
            b (float): Semi-minor axis of the ellipse (shorter radius).

        Returns:
            tuple: Shear area along x-axis (A_s,x) and y-axis (A_s,y).
        """
        # Total area of the ellipse

        # Shear coefficients
        kappa_x = (4 / 3) * (self._radius_b**2 / (self._radius_a**2 + self._radius_b**2))
        kappa_y = (4 / 3) * (self._radius_a**2 / (self._radius_a**2 + self._radius_b**2))

        # Shear areas
        A_s_x = kappa_x * self.A
        A_s_y = kappa_y * self.A
        return A_s_x, A_s_y

    @property
    def Avx(self) -> float:
        return self._calculate_shear_area()[0]

    @property
    def Avy(self) -> float:
        return self._calculate_shear_area()[1]

    @property
    def circumference(self) -> float:
        a = self._radius_a
        b = self._radius_b
        return pi * (3 * (a + b) - sqrt((3 * a + b) * (a + 3 * b)))


class Rectangle(Shape):
    """
    Rectangle shape specified by width (w) and height (h).
    """

    def __init__(self, w: float, h: float, frame: Optional[Frame] = None):
        self._w = w
        self._h = h
        pts = [
            Point(-w / 2, -h / 2, 0.0),
            Point(w / 2, -h / 2, 0.0),
            Point(w / 2, h / 2, 0.0),
            Point(-w / 2, h / 2, 0.0),
        ]
        super().__init__(pts, frame=frame)

    @property
    def w(self) -> float:
        return self._w

    @property
    def h(self) -> float:
        return self._h

    @property
    def J(self):
        """Torsional constant (polar moment of inertia).
        Roark's Formulas for stress & Strain, 7th Edition, Warren C. Young & Richard G. Budynas
        """
        a = self.w
        b = self.h
        if b > a:
            b = self.w
            a = self.h
        term1 = 16 / 3
        term2 = 3.36 * (b / a) * (1 - (b**4) / (12 * a**4))
        J = (a * b**3 / 16) * (term1 - term2)

        return J

    @property
    def Avx(self) -> float:
        return 5 / 6 * self.area

    @property
    def Avy(self) -> float:
        return 5 / 6 * self.area


class Rhombus(Shape):
    """
    Rhombus shape specified by side lengths a and b
    (the shape is basically a diamond shape).
    """

    def __init__(self, a: float, b: float, frame: Optional[Frame] = None):
        self._a = a
        self._b = b
        pts = [
            Point(0.0, -b / 2, 0.0),
            Point(a / 2, 0.0, 0.0),
            Point(0.0, b / 2, 0.0),
            Point(-a / 2, 0.0, 0.0),
        ]
        super().__init__(pts, frame=frame)

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b


class UShape(Shape):
    """
    U-shaped cross section.
    """

    def __init__(self, a: float, b: float, t1: float, t2: float, t3: float, direction: str = "up", frame: Optional[Frame] = None):
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._t3 = t3
        self._direction = direction

        pts = [
            Point(-a / 2, -b / 2, 0.0),
            Point(a / 2, -b / 2, 0.0),
            Point(a / 2, b / 2, 0.0),
            Point(a / 2 - t3, b / 2, 0.0),
            Point(a / 2 - t3, t2 - b / 2, 0.0),
            Point(t1 - a / 2, t2 - b / 2, 0.0),
            Point(t1 - a / 2, b / 2, 0.0),
            Point(-a / 2, b / 2, 0.0),
        ]
        super().__init__(pts, frame=frame)

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def t1(self) -> float:
        return self._t1

    @property
    def t2(self) -> float:
        return self._t2

    @property
    def t3(self) -> float:
        return self._t3


class TShape(Shape):
    """
    T-shaped cross section.
    """

    def __init__(self, a: float, b: float, t1: float, t2: float, direction: str = "up", frame: Optional[Frame] = None):
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._direction = direction

        pts = [
            Point(-a / 2, -b / 2, 0.0),
            Point(a / 2, -b / 2, 0.0),
            Point(a / 2, t1 - b / 2, 0.0),
            Point((a + t2) / 2 - a / 2, t1 - b / 2, 0.0),
            Point((a + t2) / 2 - a / 2, b / 2, 0.0),
            Point((a - t2) / 2 - a / 2, b / 2, 0.0),
            Point((a - t2) / 2 - a / 2, t1 - b / 2, 0.0),
            Point(-a / 2, t1 - b / 2, 0.0),
        ]
        super().__init__(pts, frame=frame)

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def t1(self) -> float:
        return self._t1

    @property
    def t2(self) -> float:
        return self._t2


class IShape(Shape):
    """
    I-shaped (or wide-flange) cross section.
    """

    def __init__(self, w: float, h: float, tw: float, tbf: float, ttf: float, direction: str = "up", frame: Optional[Frame] = None):
        self._w = w
        self._h = h
        self._tw = tw
        self._tbf = tbf
        self._ttf = ttf
        self._direction = direction

        # Half-dimensions for clarity
        half_w = 0.5 * w
        half_h = 0.5 * h
        half_tw = 0.5 * tw

        pts = [
            # Bottom outer edge
            Point(-half_w, -half_h, 0.0),
            Point(half_w, -half_h, 0.0),
            # Move up by bottom flange thickness (tbf)
            Point(half_w, -half_h + tbf, 0.0),
            Point(half_tw, -half_h + tbf, 0.0),
            # Web to top
            Point(half_tw, half_h - ttf, 0.0),
            Point(half_w, half_h - ttf, 0.0),
            # Top outer edge
            Point(half_w, half_h, 0.0),
            Point(-half_w, half_h, 0.0),
            # Move down by top flange thickness (ttf)
            Point(-half_w, half_h - ttf, 0.0),
            Point(-half_tw, half_h - ttf, 0.0),
            # Web down to bottom
            Point(-half_tw, -half_h + tbf, 0.0),
            Point(-half_w, -half_h + tbf, 0.0),
        ]
        super().__init__(pts, frame=frame)

    @property
    def w(self) -> float:
        return self._w

    @property
    def h(self) -> float:
        return self._h

    @property
    def tw(self) -> float:
        return self._tw

    @property
    def hw(self) -> float:
        return self.h - self.tbf - self.ttf

    @property
    def tbf(self) -> float:
        return self._tbf

    @property
    def ttf(self) -> float:
        return self._ttf

    @property
    def atf(self) -> float:
        return self._ttf * self.w

    @property
    def abf(self) -> float:
        return self._tbf * self.w

    @property
    def aw(self) -> float:
        return self._tw * self.hw

    @property
    def J(self) -> float:
        """
        Torsional constant approximation for an I-beam cross-section.
        (Very rough formula.)
        """
        return (1.0 / 3.0) * (self.w * (self.tbf**3 + self.ttf**3) + (self.h - self.tbf - self.ttf) * self.tw**3)

    def shear_area_I_beam_axes(self):
        """
        Calculate the shear area (A_s) of an I-beam cross-section along x- and y-axes,
        allowing for different flange thicknesses.

        Returns:
            tuple: Shear area along x-axis (A_s,x) and y-axis (A_s,y).
        """
        # Web area

        # Shear coefficients
        kappa_web = 1
        kappa_flange = 1 / 3

        # Shear area along x-axis
        A_s_x = kappa_web * self.aw + kappa_flange * self.abf + kappa_flange * self.atf

        # Shear area along y-axis (primarily web contribution)
        A_s_y = self.aw

        return A_s_x, A_s_y

    @property
    def Avx(self) -> float:
        return self.shear_area_I_beam_axes()[0]

    @property
    def Avy(self) -> float:
        return self.shear_area_I_beam_axes()[1]


class LShape(Shape):
    """
    L-shaped cross section (angle profile).
    """

    def __init__(self, a: float, b: float, t1: float, t2: float, direction: str = "up", frame: Optional[Frame] = None):
        self._a = a
        self._b = b
        self._t1 = t1
        self._t2 = t2
        self._direction = direction

        pts = [
            Point(-a / 2, -b / 2, 0.0),
            Point(a / 2, -b / 2, 0.0),
            Point(a / 2, t1 - b / 2, 0.0),
            Point(t2 - a / 2, t1 - b / 2, 0.0),
            Point(t2 - a / 2, b / 2, 0.0),
            Point(-a / 2, b / 2, 0.0),
        ]
        super().__init__(pts, frame=frame)

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def t1(self) -> float:
        return self._t1

    @property
    def t2(self) -> float:
        return self._t2


class CShape(Shape):
    """
    C-shaped cross section (channel).
    """

    def __init__(self, height: float, flange_width: float, web_thickness: float, flange_thickness: float, frame: Optional[Frame] = None):
        self._height = height
        self._flange_width = flange_width
        self._web_thickness = web_thickness
        self._flange_thickness = flange_thickness

        hw = web_thickness / 2.0
        hf = flange_width
        h = height
        ft = flange_thickness
        pts = [
            Point(0, 0, 0),
            Point(hf, 0, 0),
            Point(hf, ft, 0),
            Point(hw, ft, 0),
            Point(hw, h - ft, 0),
            Point(hf, h - ft, 0),
            Point(hf, h, 0),
            Point(0, h, 0),
        ]
        super().__init__(pts, frame=frame)


class CustomI(Shape):
    """
    Custom "I"-like shape with different top/bottom flange widths.
    """

    def __init__(
        self,
        height: float,
        top_flange_width: float,
        bottom_flange_width: float,
        web_thickness: float,
        top_flange_thickness: float,
        bottom_flange_thickness: float,
        frame: Optional[Frame] = None,
    ):
        self._height = height
        self._top_flange_width = top_flange_width
        self._bottom_flange_width = bottom_flange_width
        self._web_thickness = web_thickness
        self._top_flange_thickness = top_flange_thickness
        self._bottom_flange_thickness = bottom_flange_thickness

        htf = top_flange_width / 2.0
        hbf = bottom_flange_width / 2.0
        hw = web_thickness / 2.0

        # shift_x, shift_y can help center the shape about the local origin
        shift_x = hw / 2.0
        shift_y = height / 2.0

        pts = [
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
        super().__init__(pts, frame=frame)


class Star(Shape):
    """
    A star-like shape, parameterized by a, b, c for demonstration.
    """

    def __init__(self, a: float, b: float, c: float, frame: Optional[Frame] = None):
        self._a = a
        self._b = b
        self._c = c
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        return [
            Point(0.0, 0.0, 0.0),
            Point(self._a / 2.0, self._c, 0.0),
            Point(self._a, 0.0, 0.0),
            Point(self._a - self._c, self._b / 2.0, 0.0),
            Point(self._a, self._b, 0.0),
            Point(self._a / 2.0, self._b - self._c, 0.0),
            Point(0.0, self._b, 0.0),
            Point(self._c, self._b / 2.0, 0.0),
        ]

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, val: float):
        self._a = val
        self.points = self._set_points()

    @property
    def b(self) -> float:
        return self._b

    @b.setter
    def b(self, val: float):
        self._b = val
        self.points = self._set_points()

    @property
    def c(self) -> float:
        return self._c

    @c.setter
    def c(self, val: float):
        self._c = val
        self.points = self._set_points()


class Hexagon(Shape):
    """
    A regular hexagon specified by its side length.
    """

    def __init__(self, side_length: float, frame: Optional[Frame] = None):
        self._side_length = side_length
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        return [
            Point(
                self._side_length * math.cos(math.pi / 3 * i),
                self._side_length * math.sin(math.pi / 3 * i),
                0.0,
            )
            for i in range(6)
        ]

    @property
    def side_length(self) -> float:
        return self._side_length

    @side_length.setter
    def side_length(self, val: float):
        self._side_length = val
        self.points = self._set_points()


class Pentagon(Shape):
    """
    A regular pentagon specified by its circumradius.
    """

    def __init__(self, circumradius: float, frame: Optional[Frame] = None):
        self._circumradius = circumradius
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        angle = 2 * pi / 5
        return [
            Point(
                self._circumradius * math.cos(i * angle),
                self._circumradius * math.sin(i * angle),
                0.0,
            )
            for i in range(5)
        ]


class Octagon(Shape):
    """
    A regular octagon specified by its circumradius.
    """

    def __init__(self, circumradius: float, frame: Optional[Frame] = None):
        self._circumradius = circumradius
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        angle = 2 * pi / 8
        return [
            Point(
                self._circumradius * math.cos(i * angle),
                self._circumradius * math.sin(i * angle),
                0.0,
            )
            for i in range(8)
        ]


class Triangle(Shape):
    """
    An equilateral triangle specified by its circumradius.
    """

    def __init__(self, circumradius: float, frame: Optional[Frame] = None):
        self._circumradius = circumradius
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        angle = 2 * pi / 3
        return [
            Point(
                self._circumradius * math.cos(i * angle),
                self._circumradius * math.sin(i * angle),
                0.0,
            )
            for i in range(3)
        ]


class Parallelogram(Shape):
    """
    A parallelogram specified by width, height, and the angle (in radians).
    """

    def __init__(self, width: float, height: float, angle: float, frame: Optional[Frame] = None):
        self._width = width
        self._height = height
        self._angle = angle
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        dx = self._height * math.sin(self._angle)
        dy = self._height * math.cos(self._angle)
        return [
            Point(0.0, 0.0, 0.0),
            Point(self._width, 0.0, 0.0),
            Point(self._width + dx, dy, 0.0),
            Point(dx, dy, 0.0),
        ]


class Trapezoid(Shape):
    """
    A trapezoid specified by top width, bottom width, and height.
    """

    def __init__(self, top_width: float, bottom_width: float, height: float, frame: Optional[Frame] = None):
        self._top_width = top_width
        self._bottom_width = bottom_width
        self._height = height
        pts = self._set_points()
        super().__init__(pts, frame=frame)

    def _set_points(self) -> List[Point]:
        dx = (self._bottom_width - self._top_width) / 2.0
        return [
            Point(dx, 0.0, 0.0),
            Point(dx + self._top_width, 0.0, 0.0),
            Point(self._bottom_width, self._height, 0.0),
            Point(0.0, self._height, 0.0),
        ]
