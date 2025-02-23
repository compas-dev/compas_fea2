from math import pi
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as mplPolygon
from matplotlib.path import Path

from compas_fea2 import units
from compas_fea2.base import FEAData
from compas_fea2.model.shapes import Circle
from compas_fea2.model.shapes import IShape
from compas_fea2.model.shapes import LShape
from compas_fea2.model.shapes import Rectangle


def from_shape(shape, material: "_Material", **kwargs) -> dict:  # noqa: F821
    return {
        "A": shape.A,
        "Ixx": shape.Ixx,
        "Iyy": shape.Iyy,
        "Ixy": shape.Ixy,
        "Avx": shape.Avx,
        "Avy": shape.Avy,
        "J": shape.J,
        "material": material,
        **kwargs,
    }


class _Section(FEAData):
    """
    Base class for sections.

    Parameters
    ----------
    material : :class:`~compas_fea2.model._Material`
        A material definition.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    key : int, read-only
        Identifier index of the section in the parent Model.
    material : :class:`~compas_fea2.model._Material`
        The material associated with the section.
    model : :class:`compas_fea2.model.Model`
        The model where the section is assigned.

    Notes
    -----
    Sections are registered to a :class:`compas_fea2.model.Model` and can be assigned
    to elements in different Parts.
    """

    def __init__(self, *, material: "_Material", **kwargs):  # noqa: F821
        super().__init__(**kwargs)
        self._material = material

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__,
            "material": self.material.__data__,
            "name": self.name,
            "uid": self.uid,
        }

    @classmethod
    def __from_data__(cls, data):
        material = data["material"].pop("class").__from_data__(data["material"])
        return cls(material=material)

    def __str__(self) -> str:
        return f"""
Section {self.name}
{'-' * len(self.name)}
model    : {self.model!r}
key      : {self.key}
material : {self.material!r}
"""

    @property
    def model(self):
        return self._registration

    @property
    def material(self) -> "_Material":  # noqa: F821
        return self._material

    @material.setter
    def material(self, value: "_Material"):  # noqa: F821
        from compas_fea2.model.materials import _Material

        if value:
            if not isinstance(value, _Material):
                raise ValueError("Material must be of type `compas_fea2.model._Material`.")
            self._material = value


# ==============================================================================
# 0D
# ==============================================================================


class MassSection(FEAData):
    """
    Section for point mass elements.

    Parameters
    ----------
    mass : float
        Point mass value.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    key : int, read-only
        Identifier of the element in the parent part.
    mass : float
        Point mass value.
    """

    def __init__(self, mass: float, **kwargs):
        super().__init__(**kwargs)
        self.mass = mass

    def __str__(self) -> str:
        return f"""
Mass Section  {self.name}
{'-' * len(self.name)}
model    : {self.model!r}
mass     : {self.mass}
"""

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__.__name__,
            "mass": self.mass,
            "uid": self.uid,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(mass=data["mass"], **data)


class SpringSection(FEAData):
    """
    Section for use with spring elements.

    Parameters
    ----------
    axial : float
        Axial stiffness value.
    lateral : float
        Lateral stiffness value.
    rotational : float
        Rotational stiffness value.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    axial : float
        Axial stiffness value.
    lateral : float
        Lateral stiffness value.
    rotational : float
        Rotational stiffness value.

    Notes
    -----
    SpringSections are registered to a :class:`compas_fea2.model.Model` and can be assigned
    to elements in different Parts.
    """

    def __init__(self, axial: float, lateral: float, rotational: float, **kwargs):
        super().__init__(**kwargs)
        self.axial = axial
        self.lateral = lateral
        self.rotational = rotational

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__.__name__,
            "axial": self.axial,
            "lateral": self.lateral,
            "rotational": self.rotational,
            "uid": self.uid,
            "name": self.name,
        }

    @classmethod
    def __from_data__(cls, data):
        sec = cls(axial=data["axial"], lateral=data["lateral"], rotational=data["rotational"])
        sec.uid = data["uid"]
        sec.name = data["name"]
        return sec

    def __str__(self) -> str:
        return f"""
Spring Section
--------------
Key                     : {self.key}
axial stiffness         : {self.axial}
lateral stiffness       : {self.lateral}
rotational stiffness    : {self.rotational}
"""

    @property
    def model(self):
        return self._registration

    @property
    def stiffness(self) -> dict:
        return {"Axial": self.axial, "Lateral": self.lateral, "Rotational": self.rotational}


# ==============================================================================
# 1D
# ==============================================================================

# # ============================================================================
# # 1D - beam cross-sections
# # ============================================================================


class BeamSection(_Section):
    """
    Custom section for beam elements.

    Parameters
    ----------
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    shape : :class:`compas_fea2.shapes.Shape`
        The shape of the section.
    """

    def __init__(self, *, A: float, Ixx: float, Iyy: float, Ixy: float, Avx: float, Avy: float, J: float, material: "_Material", **kwargs):  # noqa: F821
        super().__init__(material=material, **kwargs)
        self.A = A
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Ixy = Ixy
        self.Avx = Avx
        self.Avy = Avy
        self.J = J
        

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "A": self.A,
                "Ixx": self.Ixx,
                "Iyy": self.Iyy,
                "Ixy": self.Ixy,
                "Avx": self.Avx,
                "Avy": self.Avy,
                "J": self.J,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        section = super().__from_data__(data.pop("material"))
        return section(**data)

    def __str__(self) -> str:
        return f"""
{self.__class__.__name__}
{'-' * len(self.__class__.__name__)}
name     : {self.name}
material : {self.material!r}

A   : {self.A * units["m**2"]:.4g}
Ixx : {self.Ixx * units["m**4"]:.4g}
Iyy : {self.Iyy * units["m**4"]:.4g}
Ixy : {self.Ixy * units["m**4"]:.4g}
Avx : {self.Avx * units["m**2"]:.2g}
Avy : {self.Avy * units["m**2"]:.2g}
J   : {self.J}
g0  : {self.g0}
gw  : {self.gw}
"""

    @classmethod
    def from_shape(cls, shape, material: "_Material", **kwargs):  # noqa: F821
        section = cls(**from_shape(shape, material, **kwargs))
        section._shape = shape
        return section

    @property
    def shape(self):
        return self._shape

    def plot(self):
        self.shape.plot()

    def compute_stress(self, N: float = 0.0, Mx: float = 0.0, My: float = 0.0, Vx: float = 0.0, Vy: float = 0.0, x: float = 0.0, y: float = 0.0) -> tuple:
        """
        Compute normal and shear stresses at a given point.

        Parameters
        ----------
        N : float, optional
            Axial force (default is 0.0).
        Mx : float, optional
            Bending moment about the x-axis (default is 0.0).
        My : float, optional
            Bending moment about the y-axis (default is 0.0).
        Vx : float, optional
            Shear force in the x-direction (default is 0.0).
        Vy : float, optional
            Shear force in the y-direction (default is 0.0).
        x : float, optional
            X-coordinate of the point (default is 0.0).
        y : float, optional
            Y-coordinate of the point (default is 0.0).

        Returns
        -------
        tuple
            Normal stress, shear stress in x-direction, shear stress in y-direction.
        """
        sigma = (N / self.A) - (Mx * y / self.Ixx) + (My * x / self.Iyy)
        tau_x = Vx / self.Avx if self.Avx else Vx / self.A
        tau_y = Vy / self.Avy if self.Avy else Vy / self.A
        return sigma, tau_x, tau_y

    def compute_stress_distribution(self, N: float = 0.0, Mx: float = 0.0, My: float = 0.0, Vx: float = 0.0, Vy: float = 0.0, nx: int = 50, ny: int = 50) -> tuple:
        """
        Compute stress distribution over the section.

        Parameters
        ----------
        N : float, optional
            Axial force (default is 0.0).
        Mx : float, optional
            Bending moment about the x-axis (default is 0.0).
        My : float, optional
            Bending moment about the y-axis (default is 0.0).
        Vx : float, optional
            Shear force in the x-direction (default is 0.0).
        Vy : float, optional
            Shear force in the y-direction (default is 0.0).
        nx : int, optional
            Grid resolution in x direction (default is 50).
        ny : int, optional
            Grid resolution in y direction (default is 50).

        Returns
        -------
        tuple
            Grid of x-coordinates, grid of y-coordinates, grid of normal stresses, grid of shear stresses in x-direction, grid of shear stresses in y-direction.
        """
        verts = [(p.x, p.y) for p in self.shape.points]
        polygon_path = Path(verts)
        xs = [p[0] for p in verts]
        ys = [p[1] for p in verts]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        cx, cy, _ = self.shape.centroid
        x = np.linspace(x_min, x_max, nx)
        y = np.linspace(y_min, y_max, ny)
        grid_x, grid_y = np.meshgrid(x, y)
        points = np.vstack((grid_x.flatten(), grid_y.flatten())).T
        inside = polygon_path.contains_points(points)
        grid_sigma = np.full(grid_x.shape, np.nan)
        grid_tau_x = np.full(grid_x.shape, np.nan)
        grid_tau_y = np.full(grid_x.shape, np.nan)

        for i, (x_, y_) in enumerate(points):
            if inside[i]:
                x_fiber = x_ - cx
                y_fiber = y_ - cy
                sigma, tau_x, tau_y = self.compute_stress(N=N, Mx=Mx, My=My, Vx=Vx, Vy=Vy, x=x_fiber, y=y_fiber)
                grid_sigma.flat[i] = sigma
                grid_tau_x.flat[i] = tau_x
                grid_tau_y.flat[i] = tau_y

        return grid_x, grid_y, grid_sigma, grid_tau_x, grid_tau_y

    def compute_neutral_axis(self, N: float = 0.0, Mx: float = 0.0, My: float = 0.0) -> tuple:
        """
        Compute the neutral axis slope and intercept for the section.

        Parameters
        ----------
        N : float, optional
            Axial force (default is 0.0).
        Mx : float, optional
            Bending moment about the x-axis (default is 0.0).
        My : float, optional
            Bending moment about the y-axis (default is 0.0).

        Returns
        -------
        tuple
            Slope of the neutral axis (dy/dx) or None for vertical axis, intercept of the neutral axis in local coordinates.

        Raises
        ------
        ValueError
            If the neutral axis is undefined for pure axial load.
        """
        if Mx == 0 and My == 0:
            raise ValueError("Neutral axis is undefined for pure axial load.")

        # Centroid and properties
        cx, cy, _ = self.shape.centroid
        A = self.A
        Ixx = self.Ixx
        Iyy = self.Iyy

        # General slope-intercept form for the neutral axis
        if Mx == 0:  # Vertical neutral axis
            slope = None
            intercept = cx + (N * Iyy) / (My * A)
        elif My == 0:  # Horizontal neutral axis
            slope = 0.0
            intercept = cy + (N * Ixx) / (Mx * A)
        else:
            slope = (My / Iyy) / (Mx / Ixx)
            intercept = cy - slope * cx + (N * Ixx) / (Mx * A)

        return slope, intercept

    def plot_stress_distribution(
        self, N: float = 0.0, Mx: float = 0.0, My: float = 0.0, Vx: float = 0.0, Vy: float = 0.0, nx: int = 50, ny: int = 50, cmap: str = "coolwarm", show_tau: bool = True
    ):
        """
        Visualize normal stress (\u03c3) and optionally shear stresses (\u03c4_x, \u03c4_y) with the neutral axis.

        Parameters
        ----------
        N : float, optional
            Axial force (default is 0.0).
        Mx : float, optional
            Bending moment about the x-axis (default is 0.0).
        My : float, optional
            Bending moment about the y-axis (default is 0.0).
        Vx : float, optional
            Shear force in the x-direction (default is 0.0).
        Vy : float, optional
            Shear force in the y-direction (default is 0.0).
        nx : int, optional
            Grid resolution in x direction (default is 50).
        ny : int, optional
            Grid resolution in y direction (default is 50).
        cmap : str, optional
            Colormap for stress visualization (default is "coolwarm").
        show_tau : bool, optional
            Whether to display separate plots for shear stresses (\u03c4_x, \u03c4_y) (default is True).
        """
        grid_x, grid_y, grid_sigma, grid_tau_x, grid_tau_y = self.compute_stress_distribution(N=N, Mx=Mx, My=My, Vx=Vx, Vy=Vy, nx=nx, ny=ny)

        # Plot normal stress (\u03c3)
        fig_sigma, ax_sigma = plt.subplots(figsize=(6, 6))
        sigma_plot = ax_sigma.pcolormesh(
            grid_x,
            grid_y,
            grid_sigma,
            shading="auto",
            cmap=cmap,
            vmin=-np.nanmax(abs(grid_sigma)),  # Symmetrical range for compression/tension
            vmax=np.nanmax(abs(grid_sigma)),
        )
        cbar_sigma = plt.colorbar(sigma_plot, ax=ax_sigma, fraction=0.046, pad=0.04)
        cbar_sigma.set_label("Normal Stress (\u03c3) [N/mm²]", fontsize=9)

        # Add section boundary
        verts = [(p.x, p.y) for p in self.shape.points]
        xs, ys = zip(*verts + [verts[0]])  # Close the polygon loop
        ax_sigma.plot(xs, ys, color="black", linewidth=1.5)

        # Set aspect ratio and axis labels
        ax_sigma.set_aspect("equal", "box")
        ax_sigma.set_xlabel("X (mm)", fontsize=9)
        ax_sigma.set_ylabel("Y (mm)", fontsize=9)

        # Compute and plot the neutral axis on the \u03c3 plot
        try:
            slope, intercept = self.compute_neutral_axis(N=N, Mx=Mx, My=My)
        except ValueError as e:
            print(f"Warning: {e}")
            slope, intercept = None, None
        x_min, x_max = ax_sigma.get_xlim()
        y_min, y_max = ax_sigma.get_ylim()

        if slope is None:  # Vertical neutral axis
            if intercept is not None:
                ax_sigma.axvline(intercept, color="red", linestyle="--", linewidth=1.5)
        else:  # General or horizontal case
            x_vals = np.linspace(x_min, x_max, 100)
            y_vals = slope * x_vals + intercept
            valid = (y_vals >= y_min) & (y_vals <= y_max)
            if np.any(valid):
                ax_sigma.plot(x_vals[valid], y_vals[valid], color="red", linestyle="--", linewidth=1.5)

        ax_sigma.legend(loc="upper left", fontsize=8)
        plt.tight_layout()
        plt.show()

        # Plot shear stresses (\u03c4_x and \u03c4_y) if requested
        if show_tau:
            # \u03c4_x (Shear Stress in X)
            fig_tau_x, ax_tau_x = plt.subplots(figsize=(6, 6))
            tau_x_plot = ax_tau_x.pcolormesh(
                grid_x,
                grid_y,
                grid_tau_x,
                shading="auto",
                cmap=cmap,
                vmin=-np.nanmax(abs(grid_tau_x)),  # Independent range for tau_x
                vmax=np.nanmax(abs(grid_tau_x)),
            )
            cbar_tau_x = plt.colorbar(tau_x_plot, ax=ax_tau_x, fraction=0.046, pad=0.04)
            cbar_tau_x.set_label("Shear Stress (\u03c4_x) [N/mm²]", fontsize=9)

            ax_tau_x.plot(xs, ys, color="black", linewidth=1.5)
            ax_tau_x.set_aspect("equal", "box")
            ax_tau_x.set_xlabel("X (mm)", fontsize=9)
            ax_tau_x.set_ylabel("Y (mm)", fontsize=9)

            plt.tight_layout()
            plt.show()

            # \u03c4_y (Shear Stress in Y)
            fig_tau_y, ax_tau_y = plt.subplots(figsize=(6, 6))
            tau_y_plot = ax_tau_y.pcolormesh(
                grid_x,
                grid_y,
                grid_tau_y,
                shading="auto",
                cmap=cmap,
                vmin=-np.nanmax(abs(grid_tau_y)),  # Independent range for tau_y
                vmax=np.nanmax(abs(grid_tau_y)),
            )
            cbar_tau_y = plt.colorbar(tau_y_plot, ax=ax_tau_y, fraction=0.046, pad=0.04)
            cbar_tau_y.set_label("Shear Stress (\u03c4_y) [N/mm²]", fontsize=9)

            ax_tau_y.plot(xs, ys, color="black", linewidth=1.5)
            ax_tau_y.set_aspect("equal", "box")
            ax_tau_y.set_xlabel("X (mm)", fontsize=9)
            ax_tau_y.set_ylabel("Y (mm)", fontsize=9)

            plt.tight_layout()
            plt.show()

    def plot_section_with_stress(
        self, N: float = 0.0, Mx: float = 0.0, My: float = 0.0, Vx: float = 0.0, Vy: float = 0.0, direction: tuple = (1, 0), point: tuple = None, nx: int = 50, ny: int = 50
    ):
        """
        Plot the section and overlay the stress distribution along a general direction.

        Parameters
        ----------
        N : float, optional
            Axial force (default is 0.0).
        Mx : float, optional
            Bending moment about the x-axis (default is 0.0).
        My : float, optional
            Bending moment about the y-axis (default is 0.0).
        Vx : float, optional
            Shear force in the x-direction (default is 0.0).
        Vy : float, optional
            Shear force in the y-direction (default is 0.0).
        direction : tuple, optional
            A 2D vector defining the direction of the line (default is (1, 0)).
        point : tuple or None, optional
            A point on the line (defaults to the section centroid if None).
        nx : int, optional
            Grid resolution in x direction (default is 50).
        ny : int, optional
            Grid resolution in y direction (default is 50).

        Raises
        ------
        ValueError
            If the specified line does not pass through the section.
        """

        # Normalize the direction vector
        dx, dy = direction
        norm = np.sqrt(dx**2 + dy**2)
        dx /= norm
        dy /= norm

        # Default point to centroid if not provided
        if point is None:
            cx, cy, _ = self.shape.centroid
        else:
            cx, cy = point

        # Compute stress distribution
        grid_x, grid_y, grid_sigma, _, _ = self.compute_stress_distribution(N=N, Mx=Mx, My=My, Vx=Vx, Vy=Vy, nx=nx, ny=ny)

        # Extract stress along the specified direction
        t_vals = np.linspace(-1, 1, 500)
        line_x = cx + t_vals * dx  # Line's x-coordinates
        line_y = cy + t_vals * dy  # Line's y-coordinates

        # Filter points inside the section boundary
        path = Path([(p.x, p.y) for p in self.shape.points])
        points_on_line = [(x, y) for x, y in zip(line_x, line_y) if path.contains_point((x, y))]

        if not points_on_line:
            raise ValueError("The specified line does not pass through the section.")

        # Extract stress values along the line
        stresses = [grid_sigma[np.argmin(np.abs(grid_y[:, 0] - y)), np.argmin(np.abs(grid_x[0, :] - x))] for x, y in points_on_line]

        # Scale the stresses for visualization
        max_abs_stress = max(abs(s) for s in stresses)
        scaled_stress_x = [max(grid_x.flatten()) + 50 + 50 * (s / max_abs_stress) for s in stresses]
        stress_coords = [(sx, y) for (x, y), sx in zip(points_on_line, scaled_stress_x)]

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot the Section Boundary
        verts = [(p.x, p.y) for p in self.shape.points]
        verts.append(verts[0])  # Close the section boundary
        xs, ys = zip(*verts)
        ax.plot(xs, ys, color="black", linewidth=1.5, label="Section Boundary")
        ax.fill(xs, ys, color="#e6e6e6", alpha=0.8)

        # Plot Stress Profile
        poly = mplPolygon(stress_coords + list(reversed(points_on_line)), closed=True, facecolor="#b3d9ff", edgecolor="blue", alpha=0.8)
        ax.add_patch(poly)

        # Annotate Stress Values
        ax.annotate(
            f"{stresses[-1]:.1f} N/mm²",
            xy=(scaled_stress_x[-1] + 10, points_on_line[-1][1]),
            fontsize=9,
            color="blue",
            va="center",
        )
        ax.annotate(
            f"{stresses[0]:.1f} N/mm²",
            xy=(scaled_stress_x[0] + 10, points_on_line[0][1]),
            fontsize=9,
            color="blue",
            va="center",
        )

        # Axis Labels and Styling
        ax.set_aspect("equal", "box")
        ax.set_xlabel("X-axis (mm)", fontsize=9)
        ax.set_ylabel("Y-axis (mm)", fontsize=9)
        ax.set_title("Section with Stress Distribution Along Specified Direction", fontsize=12)
        ax.axhline(0, color="black", linestyle="--", linewidth=1)  # x-axis
        ax.axvline(0, color="black", linestyle="--", linewidth=1)  # y-axis
        ax.legend(loc="upper left", fontsize=9)
        plt.grid(True)
        plt.show()


class GenericBeamSection(BeamSection):
    """
    Generic beam cross-section for beam elements.

    Parameters
    ----------
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.
    """

    def __init__(self, A: float, Ixx: float, Iyy: float, Ixy: float, Avx: float, Avy: float, J: float, g0: float, gw: float, material: "_Material", **kwargs):  # noqa: F821
        super().__init__(A=A, Ixx=Ixx, Iyy=Iyy, Ixy=Ixy, Avx=Avx, Avy=Avy, J=J, g0=g0, gw=gw, material=material, **kwargs)
        self._shape = Circle(radius=sqrt(A / pi))

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "g0": self.g0,
                "gw": self.gw,
            }
        )
        return data


class AngleSection(BeamSection):
    """
    Uniform thickness angle cross-section for beam elements.

    Parameters
    ----------
    w : float
        Width.
    h : float
        Height.
    t1 : float
        Thickness.
    t2 : float
        Thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    w : float
        Width.
    h : float
        Height.
    t1 : float
        Thickness.
    t2 : float
        Thickness.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Warnings
    --------
    Ixy not yet calculated.
    """

    def __init__(self, w, h, t1, t2, material, **kwargs):
        self._shape = LShape(w, h, t1, t2)
        super().__init__(**from_shape(self._shape, material, **kwargs))

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "w": self._shape.w,
                "h": self._shape.h,
                "t1": self._shape.t1,
                "t2": self._shape.t2,
            }
        )
        return data


# FIXME: implement 'from_shape' method
class BoxSection(BeamSection):
    """
    Hollow rectangular box cross-section for beam elements.

    Parameters
    ----------
    w : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tf : float
        Flange thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    w : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tf : float
        Flange thickness.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Notes
    -----
    Currently you can only specify the thickness of the flanges and the webs.

    Warnings
    --------
    Ixy not yet calculated.
    """

    def __init__(self, w, h, tw, tf, material, **kwargs):
        self.w = w
        self.h = h
        self.tw = tw
        self.tf = tf

        Ap = (h - tf) * (w - tw)
        p = 2 * ((h - tf) / tw + (w - tw) / tf)

        A = w * h - (w - 2 * tw) * (h - 2 * tf)
        Ixx = (w * h**3) / 12.0 - ((w - 2 * tw) * (h - 2 * tf) ** 3) / 12.0
        Iyy = (h * w**3) / 12.0 - ((h - 2 * tf) * (w - 2 * tw) ** 3) / 12.0
        Ixy = 0  # FIXME
        Avx = 0  # FIXME
        Avy = 0  # FIXME
        J = 4 * (Ap**2) / p
        g0 = 0  # FIXME
        gw = 0  # FIXME

        super(BoxSection, self).__init__(
            A=A,
            Ixx=Ixx,
            Iyy=Iyy,
            Ixy=Ixy,
            Avx=Avx,
            Avy=Avy,
            J=J,
            g0=g0,
            gw=gw,
            material=material,
            **kwargs,
        )

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "w": self.w,
                "h": self.h,
                "tw": self.tw,
                "tf": self.tf,
            }
        )
        return data


class CircularSection(BeamSection):
    """
    Solid circular cross-section for beam elements.

    Parameters
    ----------
    r : float
        Radius.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    r : float
        Radius.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, r, material, **kwargs):
        self._shape = Circle(r, 360)
        super().__init__(**from_shape(self._shape, material, **kwargs))

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "r": self._shape.radius,
            }
        )
        return data


# FIXME: implement 'from_shape' method
class HexSection(BeamSection):
    """
    Hexagonal hollow section.

    Parameters
    ----------
    r : float
        Outside radius.
    t : float
        Wall thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    r : float
        Outside radius.
    t : float
        Wall thickness.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Raises
    ------
    NotImplementedError
        If the section is not available for the selected backend.
    """

    def __init__(self, r, t, material, **kwargs):
        raise NotImplementedError("This section is not available for the selected backend")

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "r": self.r,
                "t": self.t,
            }
        )
        return data


class ISection(BeamSection):
    """
    Equal flanged I-section for beam elements.

    Parameters
    ----------
    w : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tbf : float
        Bottom flange thickness.
    ttf : float
        Top flange thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    w : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tbf : float
        Bottom flange thickness.
    ttf : float
        Top flange thickness.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, w, h, tw, tbf, ttf, material, **kwargs):
        self._shape = IShape(w, h, tw, tbf, ttf)
        super().__init__(**from_shape(self._shape, material, **kwargs))
        
    @property
    def k(self):
        return 0.3 + 0.1 * ((self.shape.abf+self.shape.atf) / self.shape.area)

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "w": self._shape.w,
                "h": self._shape.h,
                "tw": self._shape.tw,
                "tbf": self._shape.tbf,
                "ttf": self._shape.ttf,
            }
        )
        return data

    @classmethod
    def IPE80(cls, material, **kwargs):
        return cls(w=46, h=80, tw=3.8, tbf=6.1, ttf=6.1, material=material, **kwargs)

    @classmethod
    def IPE100(cls, material, **kwargs):
        return cls(w=55, h=100, tw=4.1, tbf=6.7, ttf=6.7, material=material, **kwargs)

    @classmethod
    def IPE120(cls, material, **kwargs):
        return cls(w=64, h=120, tw=4.4, tbf=7.2, ttf=7.2, material=material, **kwargs)

    @classmethod
    def IPE140(cls, material, **kwargs):
        return cls(w=73, h=140, tw=4.7, tbf=7.5, ttf=7.5, material=material, **kwargs)

    @classmethod
    def IPE160(cls, material, **kwargs):
        return cls(w=82, h=160, tw=5, tbf=7.4, ttf=7.4, material=material, **kwargs)

    @classmethod
    def IPE180(cls, material, **kwargs):
        return cls(w=91, h=180, tw=5.3, tbf=8, ttf=8, material=material, **kwargs)

    @classmethod
    def IPE200(cls, material, **kwargs):
        return cls(w=100, h=200, tw=5.6, tbf=8.5, ttf=8.5, material=material, **kwargs)

    @classmethod
    def IPE220(cls, material, **kwargs):
        return cls(w=110, h=220, tw=5.9, tbf=9.2, ttf=9.2, material=material, **kwargs)

    @classmethod
    def IPE240(cls, material, **kwargs):
        return cls(w=120, h=240, tw=6.2, tbf=9.8, ttf=9.8, material=material, **kwargs)

    @classmethod
    def IPE270(cls, material, **kwargs):
        return cls(w=135, h=270, tw=6.6, tbf=10.2, ttf=10.2, material=material, **kwargs)

    @classmethod
    def IPE300(cls, material, **kwargs):
        return cls(w=150, h=300, tw=7.1, tbf=10.7, ttf=10.7, material=material, **kwargs)

    @classmethod
    def IPE330(cls, material, **kwargs):
        return cls(w=160, h=330, tw=7.5, tbf=11.5, ttf=11.5, material=material, **kwargs)

    @classmethod
    def IPE360(cls, material, **kwargs):
        return cls(w=170, h=360, tw=8, tbf=12.7, ttf=12.7, material=material, **kwargs)

    @classmethod
    def IPE400(cls, material, **kwargs):
        return cls(w=180, h=400, tw=8.6, tbf=13.5, ttf=13.5, material=material, **kwargs)

    # HEA Sections
    @classmethod
    def HEA100(cls, material, **kwargs):
        return cls(w=100, h=96, tw=5, tbf=8, ttf=8, material=material, **kwargs)

    @classmethod
    def HEA120(cls, material, **kwargs):
        return cls(w=120, h=114, tw=5, tbf=8, ttf=8, material=material, **kwargs)

    @classmethod
    def HEA140(cls, material, **kwargs):
        return cls(w=140, h=133, tw=5.5, tbf=8.5, ttf=8.5, material=material, **kwargs)

    @classmethod
    def HEA160(cls, material, **kwargs):
        return cls(w=160, h=152, tw=6, tbf=9, ttf=9, material=material, **kwargs)

    @classmethod
    def HEA180(cls, material, **kwargs):
        return cls(w=180, h=171, tw=6, tbf=9.5, ttf=9.5, material=material, **kwargs)

    @classmethod
    def HEA200(cls, material, **kwargs):
        return cls(w=200, h=190, tw=6.5, tbf=10, ttf=10, material=material, **kwargs)

    @classmethod
    def HEA220(cls, material, **kwargs):
        return cls(w=220, h=210, tw=7, tbf=11, ttf=11, material=material, **kwargs)

    @classmethod
    def HEA240(cls, material, **kwargs):
        return cls(w=240, h=230, tw=7.5, tbf=12, ttf=12, material=material, **kwargs)

    @classmethod
    def HEA260(cls, material, **kwargs):
        return cls(w=260, h=250, tw=7.5, tbf=12.5, ttf=12.5, material=material, **kwargs)

    @classmethod
    def HEA280(cls, material, **kwargs):
        return cls(w=280, h=270, tw=8, tbf=13, ttf=13, material=material, **kwargs)

    @classmethod
    def HEA300(cls, material, **kwargs):
        return cls(w=300, h=290, tw=9, tbf=14, ttf=14, material=material, **kwargs)

    @classmethod
    def HEA320(cls, material, **kwargs):
        return cls(w=320, h=310, tw=9.5, tbf=15, ttf=15, material=material, **kwargs)

    @classmethod
    def HEA340(cls, material, **kwargs):
        return cls(w=340, h=330, tw=10, tbf=16, ttf=16, material=material, **kwargs)

    @classmethod
    def HEA360(cls, material, **kwargs):
        return cls(w=360, h=350, tw=10, tbf=17, ttf=17, material=material, **kwargs)

    @classmethod
    def HEA400(cls, material, **kwargs):
        return cls(w=400, h=390, tw=11.5, tbf=18, ttf=18, material=material, **kwargs)

    @classmethod
    def HEA450(cls, material, **kwargs):
        return cls(w=450, h=440, tw=12.5, tbf=19, ttf=19, material=material, **kwargs)

    @classmethod
    def HEA500(cls, material, **kwargs):
        return cls(w=500, h=490, tw=14, tbf=21, ttf=21, material=material, **kwargs)

    @classmethod
    def HEA550(cls, material, **kwargs):
        return cls(w=550, h=540, tw=15, tbf=24, ttf=24, material=material, **kwargs)

    @classmethod
    def HEA600(cls, material, **kwargs):
        return cls(w=600, h=590, tw=15.5, tbf=25, ttf=25, material=material, **kwargs)

    @classmethod
    def HEA650(cls, material, **kwargs):
        return cls(w=650, h=640, tw=16, tbf=26, ttf=26, material=material, **kwargs)

    @classmethod
    def HEA700(cls, material, **kwargs):
        return cls(w=700, h=690, tw=16.5, tbf=27, ttf=27, material=material, **kwargs)

    @classmethod
    def HEA800(cls, material, **kwargs):
        return cls(w=800, h=790, tw=17.5, tbf=28, ttf=28, material=material, **kwargs)

    @classmethod
    def HEA900(cls, material, **kwargs):
        return cls(w=900, h=890, tw=18, tbf=29, ttf=29, material=material, **kwargs)

    @classmethod
    def HEA1000(cls, material, **kwargs):
        return cls(w=1000, h=990, tw=19, tbf=30, ttf=30, material=material, **kwargs)

    # HEB Sections
    @classmethod
    def HEB100(cls, material, **kwargs):
        return cls(w=100, h=100, tw=6, tbf=10, ttf=10, material=material, **kwargs)

    @classmethod
    def HEB120(cls, material, **kwargs):
        return cls(w=120, h=120, tw=6.5, tbf=11, ttf=11, material=material, **kwargs)

    @classmethod
    def HEB140(cls, material, **kwargs):
        return cls(w=140, h=140, tw=7, tbf=12, ttf=12, material=material, **kwargs)

    @classmethod
    def HEB160(cls, material, **kwargs):
        return cls(w=160, h=160, tw=8, tbf=13, ttf=13, material=material, **kwargs)

    @classmethod
    def HEB180(cls, material, **kwargs):
        return cls(w=180, h=180, tw=8.5, tbf=14, ttf=14, material=material, **kwargs)

    @classmethod
    def HEB200(cls, material, **kwargs):
        return cls(w=200, h=200, tw=9, tbf=15, ttf=15, material=material, **kwargs)

    @classmethod
    def HEB220(cls, material, **kwargs):
        return cls(w=220, h=220, tw=9.5, tbf=16, ttf=16, material=material, **kwargs)

    @classmethod
    def HEB240(cls, material, **kwargs):
        return cls(w=240, h=240, tw=10, tbf=17, ttf=17, material=material, **kwargs)

    @classmethod
    def HEB260(cls, material, **kwargs):
        return cls(w=260, h=260, tw=10, tbf=17.5, ttf=17.5, material=material, **kwargs)

    @classmethod
    def HEB280(cls, material, **kwargs):
        return cls(w=280, h=280, tw=10.5, tbf=18, ttf=18, material=material, **kwargs)

    @classmethod
    def HEB300(cls, material, **kwargs):
        return cls(w=300, h=300, tw=11, tbf=19, ttf=19, material=material, **kwargs)

    @classmethod
    def HEB320(cls, material, **kwargs):
        return cls(w=320, h=320, tw=11.5, tbf=20, ttf=20, material=material, **kwargs)

    @classmethod
    def HEB340(cls, material, **kwargs):
        return cls(w=340, h=340, tw=12, tbf=21, ttf=21, material=material, **kwargs)

    @classmethod
    def HEB360(cls, material, **kwargs):
        return cls(w=360, h=360, tw=12.5, tbf=22, ttf=22, material=material, **kwargs)

    @classmethod
    def HEB400(cls, material, **kwargs):
        return cls(w=400, h=400, tw=13.5, tbf=23, ttf=23, material=material, **kwargs)

    @classmethod
    def HEB450(cls, material, **kwargs):
        return cls(w=450, h=450, tw=14, tbf=24, ttf=24, material=material, **kwargs)

    @classmethod
    def HEB500(cls, material, **kwargs):
        return cls(w=500, h=500, tw=14.5, tbf=25, ttf=25, material=material, **kwargs)

    @classmethod
    def HEB550(cls, material, **kwargs):
        return cls(w=550, h=550, tw=15, tbf=26, ttf=26, material=material, **kwargs)

    @classmethod
    def HEB600(cls, material, **kwargs):
        return cls(w=600, h=600, tw=15.5, tbf=27, ttf=27, material=material, **kwargs)

    @classmethod
    def HEB650(cls, material, **kwargs):
        return cls(w=650, h=650, tw=16, tbf=28, ttf=28, material=material, **kwargs)

    @classmethod
    def HEB700(cls, material, **kwargs):
        return cls(w=700, h=700, tw=16.5, tbf=29, ttf=29, material=material, **kwargs)

    @classmethod
    def HEB800(cls, material, **kwargs):
        return cls(w=800, h=800, tw=17.5, tbf=30, ttf=30, material=material, **kwargs)

    @classmethod
    def HEB900(cls, material, **kwargs):
        return cls(w=900, h=900, tw=18, tbf=31, ttf=31, material=material, **kwargs)

    @classmethod
    def HEB1000(cls, material, **kwargs):
        return cls(w=1000, h=1000, tw=19, tbf=32, ttf=32, material=material, **kwargs)

    # HEM Sections
    @classmethod
    def HEM100(cls, material, **kwargs):
        return cls(w=120, h=106, tw=12, tbf=20, ttf=20, material=material, **kwargs)

    @classmethod
    def HEM120(cls, material, **kwargs):
        return cls(w=140, h=126, tw=12, tbf=21, ttf=21, material=material, **kwargs)

    @classmethod
    def HEM140(cls, material, **kwargs):
        return cls(w=160, h=146, tw=12, tbf=22, ttf=22, material=material, **kwargs)

    @classmethod
    def HEM160(cls, material, **kwargs):
        return cls(w=180, h=166, tw=13, tbf=23, ttf=23, material=material, **kwargs)

    @classmethod
    def HEM180(cls, material, **kwargs):
        return cls(w=200, h=186, tw=14, tbf=24, ttf=24, material=material, **kwargs)

    @classmethod
    def HEM200(cls, material, **kwargs):
        return cls(w=220, h=206, tw=15, tbf=25, ttf=25, material=material, **kwargs)

    @classmethod
    def HEM220(cls, material, **kwargs):
        return cls(w=240, h=226, tw=16, tbf=26, ttf=26, material=material, **kwargs)

    @classmethod
    def HEM240(cls, material, **kwargs):
        return cls(w=260, h=246, tw=17, tbf=27, ttf=27, material=material, **kwargs)

    @classmethod
    def HEM260(cls, material, **kwargs):
        return cls(w=280, h=266, tw=18, tbf=28, ttf=28, material=material, **kwargs)

    @classmethod
    def HEM280(cls, material, **kwargs):
        return cls(w=300, h=286, tw=19, tbf=29, ttf=29, material=material, **kwargs)

    @classmethod
    def HEM300(cls, material, **kwargs):
        return cls(w=320, h=306, tw=20, tbf=30, ttf=30, material=material, **kwargs)

    @classmethod
    def HEM320(cls, material, **kwargs):
        return cls(w=340, h=326, tw=21, tbf=31, ttf=31, material=material, **kwargs)

    @classmethod
    def HEM340(cls, material, **kwargs):
        return cls(w=360, h=346, tw=22, tbf=32, ttf=32, material=material, **kwargs)

    @classmethod
    def HEM360(cls, material, **kwargs):
        return cls(w=380, h=366, tw=23, tbf=33, ttf=33, material=material, **kwargs)

    @classmethod
    def HEM400(cls, material, **kwargs):
        return cls(w=400, h=396, tw=24, tbf=34, ttf=34, material=material, **kwargs)

    @classmethod
    def HEM450(cls, material, **kwargs):
        return cls(w=450, h=446, tw=25, tbf=35, ttf=35, material=material, **kwargs)

    @classmethod
    def HEM500(cls, material, **kwargs):
        return cls(w=500, h=496, tw=26, tbf=36, ttf=36, material=material, **kwargs)

    @classmethod
    def HEM550(cls, material, **kwargs):
        return cls(w=550, h=546, tw=27, tbf=37, ttf=37, material=material, **kwargs)

    @classmethod
    def HEM600(cls, material, **kwargs):
        return cls(w=600, h=596, tw=28, tbf=38, ttf=38, material=material, **kwargs)

    @classmethod
    def HEM650(cls, material, **kwargs):
        return cls(w=650, h=646, tw=29, tbf=39, ttf=39, material=material, **kwargs)

    @classmethod
    def HEM700(cls, material, **kwargs):
        return cls(w=700, h=696, tw=30, tbf=40, ttf=40, material=material, **kwargs)

    @classmethod
    def HEM800(cls, material, **kwargs):
        return cls(w=800, h=796, tw=31, tbf=41, ttf=41, material=material, **kwargs)

    @classmethod
    def HEM900(cls, material, **kwargs):
        return cls(w=900, h=896, tw=32, tbf=42, ttf=42, material=material, **kwargs)

    @classmethod
    def HEM1000(cls, material, **kwargs):
        return cls(w=1000, h=996, tw=33, tbf=43, ttf=43, material=material, **kwargs)


class PipeSection(BeamSection):
    """
    Hollow circular cross-section for beam elements.

    Parameters
    ----------
    r : float
        Outer radius.
    t : float
        Wall thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    r : float
        Outer radius.
    t : float
        Wall thickness.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, r, t, material, **kwargs):
        self.r = r
        self.t = t

        D = 2 * r

        A = 0.25 * pi * (D**2 - (D - 2 * t) ** 2)
        Ixx = Iyy = 0.25 * pi * (r**4 - (r - t) ** 4)
        Ixy = 0
        Avx = 0
        Avy = 0
        J = (2.0 / 3) * pi * (r + 0.5 * t) * t**3
        g0 = 0
        gw = 0

        super(PipeSection, self).__init__(
            A=A,
            Ixx=Ixx,
            Iyy=Iyy,
            Ixy=Ixy,
            Avx=Avx,
            Avy=Avy,
            J=J,
            g0=g0,
            gw=gw,
            material=material,
            **kwargs,
        )

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "r": self.r,
                "t": self.t,
            }
        )
        return data


class RectangularSection(BeamSection):
    """
    Solid rectangular cross-section for beam elements.

    Parameters
    ----------
    w : float
        Width.
    h : float
        Height.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    w : float
        Width.
    h : float
        Height.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, w, h, material, **kwargs):
        self._shape = Rectangle(w, h)
        super().__init__(**from_shape(self._shape, material, **kwargs))
        self.k = 5/6

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "w": self._shape.w,
                "h": self._shape.h,
            }
        )
        return data


class TrapezoidalSection(BeamSection):
    """
    Solid trapezoidal cross-section for beam elements.

    Parameters
    ----------
    w1 : float
        Width at bottom.
    w2 : float
        Width at top.
    h : float
        Height.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    w1 : float
        Width at bottom.
    w2 : float
        Width at top.
    h : float
        Height.
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Warnings
    --------
    J not yet calculated.
    """

    def __init__(self, w1, w2, h, material, **kwargs):
        self.w1 = w1
        self.w2 = w2
        self.h = h

        # c = (h * (2 * w2 + w1)) / (3. * (w1 + w2))  # NOTE: not used

        A = 0.5 * (w1 + w2) * h
        Ixx = (1 / 12.0) * (3 * w2 + w1) * h**3
        Iyy = (1 / 48.0) * h * (w1 + w2) * (w2**2 + 7 * w1**2)
        Ixy = 0
        Avx = 0
        Avy = 0
        J = 0
        g0 = 0
        gw = 0

        super(TrapezoidalSection, self).__init__(
            A=A,
            Ixx=Ixx,
            Iyy=Iyy,
            Ixy=Ixy,
            Avx=Avx,
            Avy=Avy,
            J=J,
            g0=g0,
            gw=gw,
            material=material,
            **kwargs,
        )

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "w1": self.w1,
                "w2": self.w2,
                "h": self.h,
            }
        )
        return data


# ==============================================================================
# 1D - no cross-section
# ==============================================================================


class TrussSection(BeamSection):
    """
    For use with truss elements.

    Parameters
    ----------
    A : float
        Area.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, A, material, **kwargs):
        Ixx = 0
        Iyy = 0
        Ixy = 0
        Avx = 0
        Avy = 0
        J = 0
        g0 = 0
        gw = 0
        super(TrussSection, self).__init__(
            A=A,
            Ixx=Ixx,
            Iyy=Iyy,
            Ixy=Ixy,
            Avx=Avx,
            Avy=Avy,
            J=J,
            g0=g0,
            gw=gw,
            material=material,
            **kwargs,
        )
        self._shape = Circle(radius=sqrt(A) / pi, segments=16)

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "A": self.A,
            }
        )
        return data


class StrutSection(TrussSection):
    """
    For use with strut elements.

    Parameters
    ----------
    A : float
        Area.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, A, material, **kwargs):
        super(StrutSection, self).__init__(A=A, material=material, **kwargs)


class TieSection(TrussSection):
    """
    For use with tie elements.

    Parameters
    ----------
    A : float
        Area.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    A : float
        Cross section area.
    Ixx : float
        Inertia with respect to XX axis.
    Iyy : float
        Inertia with respect to YY axis.
    Ixy : float
        Inertia with respect to XY axis.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y.
    J : float
        Torsion modulus.
    g0 : float
        Warping constant.
    gw : float
        Warping constant.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, A, material, **kwargs):
        super(TieSection, self).__init__(A=A, material=material, **kwargs)


# ==============================================================================
# 2D
# ==============================================================================


class ShellSection(_Section):
    """
    Section for shell elements.

    Parameters
    ----------
    t : float
        Thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    t : float
        Thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, t, material, **kwargs):
        super(ShellSection, self).__init__(material=material, **kwargs)
        self.t = t

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "t": self.t,
            }
        )
        return data


class MembraneSection(_Section):
    """
    Section for membrane elements.

    Parameters
    ----------
    t : float
        Thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    t : float
        Thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, t, material, **kwargs):
        super(MembraneSection, self).__init__(material=material, **kwargs)
        self.t = t

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "t": self.t,
            }
        )
        return data


# ==============================================================================
# 3D
# ==============================================================================


class SolidSection(_Section):
    """
    Section for solid elements.

    Parameters
    ----------
    material : :class:`compas_fea2.model._Material`
        The section material.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    material : :class:`compas_fea2.model._Material`
        The section material.
    """

    def __init__(self, material, **kwargs):
        super(SolidSection, self).__init__(material=material, **kwargs)
