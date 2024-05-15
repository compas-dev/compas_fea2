from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Polygon

from compas_fea2 import units
from compas_fea2.base import FEAData

from .materials.material import _Material


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

    def __init__(self, material, **kwargs):
        super(_Section, self).__init__(**kwargs)
        self._key = None
        self._material = material
        self._shape = None

    @property
    def model(self):
        return self._registration

    @property
    def key(self):
        return self._key

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if value:
            if not isinstance(value, _Material):
                raise ValueError("Material must be of type `compas_fea2.model._Material`.")
            self._material = value

    @property
    def shape(self):
        return self._shape

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
        self._key = None

    @property
    def key(self):
        return self._key

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
    forces : dict
        Forces data for non-linear springs.
    displacements : dict
        Displacements data for non-linear springs.
    stiffness : dict
        Elastic stiffness for linear springs.

    Attributes
    ----------
    key : int, read-only
        Identifier of the element in the parent part.
    forces : dict
        Forces data for non-linear springs.
    displacements : dict
        Displacements data for non-linear springs.
    stiffness : dict
        Elastic stiffness for linear springs.

    Notes
    -----
    - Force and displacement data should range from negative to positive values.
    - Requires either a stiffness dict for linear springs, or forces and displacement lists for non-linear springs.
    - Directions are 'axial', 'lateral', 'rotation'.

    """

    def __init__(self, forces=None, displacements=None, stiffness=None, **kwargs):
        super(SpringSection, self).__init__(**kwargs)
        # TODO would be good to know the structure of these dicts and validate
        self.forces = forces or {}
        self.displacements = displacements or {}
        self.stiffness = stiffness or {}

    def __str__(self):
        return """
Spring Section
--------------
name      : {}
material  : None
forces    : {}
displ     : {}
stiffness : {}
""".format(
            self.name, self.forces, self.displacements, self.stiffness
        )


# ==============================================================================
# 1D
# ==============================================================================


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
        Ixy = 0
        J = (1.0 / 3) * (h + w - t) * t**3
        Avx = 0
        Avy = 0
        g0 = 0
        gw = 0

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
        Ixy = 0
        Avx = 0
        Avy = 0
        J = 4 * (Ap**2) / p
        g0 = 0
        gw = 0

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
        self._shape = Circle(radius=r, frame=Frame([0, 0, 0], [1, 0, 0], [0, 1, 0]))


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
        self.w = w
        self.h = h
        self.tw = tw
        self.tf = tf

        A = 2 * w * tf + (h - 2 * tf) * tw
        Ixx = (tw * (h - 2 * tf) ** 3) / 12.0 + 2 * ((tf**3) * w / 12.0 + w * tf * (h / 2.0 - tf / 2.0) ** 2)
        Iyy = ((h - 2 * tf) * tw**3) / 12.0 + 2 * ((w**3) * tf / 12.0)
        Ixy = 0
        Avx = 0
        Avy = 0
        J = (1.0 / 3) * (2 * w * tf**3 + (h - tf) * tw**3)
        g0 = 0
        gw = 0

        super(ISection, self).__init__(
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
        self._w = w
        self._h = h

        l1 = max([w, h])
        l2 = min([w, h])

        A = w * h
        Ixx = (1 / 12.0) * w * h**3
        Iyy = (1 / 12.0) * h * w**3
        Ixy = 0
        Avy = 0.833 * A
        Avx = 0.833 * A
        J = (l1 * l2**3) * (0.33333 - 0.21 * (l2 / l1) * (1 - (l2**4) / (l2 * l1**4)))
        g0 = 0
        gw = 0

        super(RectangularSection, self).__init__(
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
        self._shape = Polygon(points=[[-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2, 0], [-w / 2, h / 2, 0]])


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
