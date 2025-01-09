from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi, sqrt

from compas_fea2 import units
from compas_fea2.base import FEAData

from .materials.material import _Material
from .shapes import Rectangle, IShape, Circle


def from_shape(shape, material, **kwargs):
    return {
        "A": shape.A,
        "Ixx": shape.Ixx,
        "Iyy": shape.Iyy,
        "Ixy": shape.Ixy,
        "Avx": shape.Avx,
        "Avy": shape.Avy,
        "J": shape.J,
        "g0": shape.g0,
        "gw": shape.gw,
        "material": material,
        **kwargs,
    }


class _Section(FEAData):
    """Base class for sections.

    Parameters
    ----------
    material : :class:`~compas_fea2.model._Material`
        A material definition.

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

    def __init__(self, *, material, **kwargs):
        super(_Section, self).__init__(**kwargs)
        self._material = material

    @property
    def model(self):
        return self._registration

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if value:
            if not isinstance(value, _Material):
                raise ValueError("Material must be of type `compas_fea2.model._Material`.")
            self._material = value

    def __str__(self):
        return """
Section {}
--------{}
model    : {!r}
key      : {}
material : {!r}
""".format(
            self.name, "-" * len(self.name), self.model, self.key, self.material
        )


# ==============================================================================
# 0D
# ==============================================================================


class MassSection(FEAData):
    """Section for point mass elements.

    Parameters
    ----------
    mass : float
        Point mass value.

    Attributes
    ----------
    key : int, read-only
        Identifier of the element in the parent part.
    mass : float
        Point mass value.

    """

    def __init__(self, mass, **kwargs):
        super(MassSection, self).__init__(**kwargs)
        self.mass = mass

    def __str__(self):
        return """
Mass Section  {}
--------{}
model    : {!r}
mass     : {}
""".format(
            self.name, "-" * len(self.name), self.model, self.mass
        )


class SpringSection(FEAData):
    """Section for use with spring elements.

    Parameters
    ----------
    axial : float
        Axial stiffness value.
    lateral : float
        Lateral stiffness value.
    axial : float
        Rotational stiffness value.

    Attributes
    ----------
    axial : float
        Axial stiffness value.
    lateral : float
        Lateral stiffness value.
    axial : float
        Rotational stiffness value.

    Notes
    -----
    SpringSections are registered to a :class:`compas_fea2.model.Model` and can be assigned
    to elements in different Parts.
    """

    def __init__(self, axial, lateral, rotational, **kwargs):
        super(SpringSection, self).__init__(**kwargs)
        self.axial = axial
        self.lateral = lateral
        self.rotational = rotational

    def __str__(self):
        return """
Spring Section
--------------
Key                     : {}
axial stiffness         : {}
lateral stiffness       : {}
rotational stiffness    : {}
""".format(
            self.key, self.axial, self.lateral, self.rotational
        )

    @property
    def model(self):
        return self._registration

    @property
    def stiffness(self):
        return {"Axial": self._axial, "Lateral": self._lateral, "Rotational": self._rotational}


# ==============================================================================
# 1D
# ==============================================================================

# # ============================================================================
# # 1D - beam cross-sections
# # ============================================================================


class BeamSection(_Section):
    """Custom section for beam elements.

    Parameters
    ----------
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    """

    def __init__(self, *, A, Ixx, Iyy, Ixy, Avx, Avy, J, g0, gw, material, **kwargs):
        super(BeamSection, self).__init__(material=material, **kwargs)
        self.A = A
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Ixy = Ixy
        self.Avx = Avx
        self.Avy = Avy
        self.J = J
        self.g0 = g0
        self.gw = gw

    def __str__(self):
        return """
{}
{}
name     : {}
material : {!r}

A   : {:~.4g}
Ixx : {:~.4g}
Iyy : {:~.4g}
Ixy : {:~.4g}
Avx : {:~.2g}
Avy : {:~.2g}
J   : {}
g0  : {}
gw  : {}
""".format(
            self.__class__.__name__,
            len(self.__class__.__name__) * "-",
            self.name,
            self.material,
            (self.A * units["m**2"]),
            (self.Ixx * units["m**4"]),
            (self.Iyy * units["m**4"]),
            (self.Ixy * units["m**4"]),
            (self.Avx * units["m**2"]),
            (self.Avy * units["m**2"]),
            self.J,
            self.g0,
            self.gw,
        )

    @classmethod
    def from_shape(cls, shape, material, **kwargs):
        section = cls(**from_shape(shape, material, **kwargs))
        section._shape = shape
        return section

    @property
    def shape(self):
        return self._shape


class AngleSection(BeamSection):
    """Uniform thickness angle cross-section for beam elements.

    Parameters
    ----------
    w : float
        Width.
    h : float
        Height.
    t : float
        Thickness.
    material : :class:`compas_fea2.model.Material`
        The section material.
    name : str, optional
        Section name. If not provided, a unique identifier is automatically
        assigned.

    Attributes
    ----------
    w : float
        Width.
    h : float
        Height.
    t : float
        Thickness.
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.
    name : str
        Section name. If not provided, a unique identifier is automatically
        assigned.

    Warnings
    --------
    - Ixy not yet calculated.

    """

    def __init__(self, w, h, t, material, **kwargs):
        self.w = w
        self.h = h
        self.t = t

        p = 2.0 * (w + h - t)
        xc = (w**2 + h * t - t**2) / p
        yc = (h**2 + w * t - t**2) / p

        A = t * (w + h - t)
        Ixx = (1.0 / 3) * (w * h**3 - (w - t) * (h - t) ** 3) - self.A * (h - yc) ** 2
        Iyy = (1.0 / 3) * (h * w**3 - (h - t) * (w - t) ** 3) - self.A * (w - xc) ** 2
        Ixy = 0  # FIXME
        J = (1.0 / 3) * (h + w - t) * t**3
        Avx = 0  # FIXME
        Avy = 0  # FIXME
        g0 = 0  # FIXME
        gw = 0  # FIXME

        super(AngleSection, self).__init__(
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


# TODO implement different thickness along the 4 sides
class BoxSection(BeamSection):
    """Hollow rectangular box cross-section for beam elements.

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
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    Notes
    -----
    Currently you can only specify the thickness of the flanges and the webs.

    Warnings
    --------
    - Ixy not yet calculated.

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


class CircularSection(BeamSection):
    """Solid circular cross-section for beam elements.

    Parameters
    ----------
    r : float
        Radius.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    r : float
        Radius.
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    """

    def __init__(self, r, material, **kwargs):
        self.r = r

        D = 2 * r
        A = 0.25 * pi * D**2
        Ixx = Iyy = (pi * D**4) / 64.0
        Ixy = 0
        Avx = 0
        Avy = 0
        J = (pi * D**4) / 32
        g0 = 0
        gw = 0

        super(CircularSection, self).__init__(
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
        self._shape = Circle(radius=r, segments=16)


class HexSection(BeamSection):
    """Hexagonal hollow section.

    Parameters
    ----------
    r : float
        outside radius
    t : float
        wall thickness
    material : str
        material name to be assigned to the section.

    Attributes
    ----------
    r : float
        outside radius
    t : float
        wall thickness
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    """

    def __init__(self, r, t, material, **kwargs):
        raise NotImplementedError("This section is not available for the selected backend")


class ISection(BeamSection):
    """Equal flanged I-section for beam elements.

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
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    Notes
    -----
    Currently you the thickness of the two flanges is the same.

    """

    def __init__(self, w, h, tw, tf, material, **kwargs):
        self._shape = IShape(w, h, tw, tf, tf)
        super().__init__(**from_shape(self._shape, material, **kwargs))


class PipeSection(BeamSection):
    """Hollow circular cross-section for beam elements.

    Parameters
    ----------
    r : float
        Outer radius.
    t : float
        Wall thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    r : float
        Outer radius.
    t : float
        Wall thickness.
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
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


class RectangularSection(BeamSection):
    """Solid rectangular cross-section for beam elements.

    Parameters
    ----------
    w : float
        Width.
    h : float
        Height.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    w : float
        Width.
    h : float
        Height.
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    """

    def __init__(self, w, h, material, **kwargs):
        self._shape = Rectangle(w, h)
        super().__init__(**from_shape(self._shape, material, **kwargs))


class TrapezoidalSection(BeamSection):
    """Solid trapezoidal cross-section for beam elements.

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

    Attributes
    ----------
    w1 : float
        Width at bottom.
    w2 : float
        Width at top.
    h : float
        Height.
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    Warnings
    --------
    - J not yet calculated.

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


# ==============================================================================
# 1D - no cross-section
# ==============================================================================


class TrussSection(BeamSection):
    """For use with truss elements.

    Parameters
    ----------
    A : float
        Area.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
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


class StrutSection(TrussSection):
    """For use with strut elements.

    Parameters
    ----------
    A : float
        Area.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    """

    def __init__(self, A, material, **kwargs):
        super(StrutSection, self).__init__(A=A, material=material, **kwargs)


class TieSection(TrussSection):
    """For use with tie elements.

    Parameters
    ----------
    A : float
        Area.
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    A : float
        Cross section.
    Ixx : float
        Inertia wrt XX.
    Iyy : float
        Inertia wrt YY.
    Ixy : float
        Inertia wrt XY.
    Avx : float
        Shear area along x.
    Avy : float
        Shear area along y
    J : float
        Torsion modulus.
    g0 : float
        ???
    gw : float
        ???
    material : :class:`compas_fea2.model._Material`
        The section material.

    """

    def __init__(self, A, material, **kwargs):
        super(TieSection, self).__init__(A=A, material=material, **kwargs)


# ==============================================================================
# 2D
# ==============================================================================


class ShellSection(_Section):
    """Section for shell elements.

    Parameters
    ----------
    t : float
        Thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.

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


class MembraneSection(_Section):
    """Section for membrane elements.

    Parameters
    ----------
    t : float
        Thickness.
    material : :class:`compas_fea2.model._Material`
        The section material.

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


# ==============================================================================
# 3D
# ==============================================================================


class SolidSection(_Section):
    """Section for solid elements.

    Parameters
    ----------
    material : :class:`compas_fea2.model._Material`
        The section material.

    Attributes
    ----------
    material : :class:`compas_fea2.model._Material`
        The section material.

    """

    def __init__(self, material, **kwargs):
        super(SolidSection, self).__init__(material=material, **kwargs)
