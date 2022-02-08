from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas_fea2.base import FEABase
from compas_fea2.model.materials import Material


class Section(FEABase):
    """Initialises base Section object.

    Parameters
    ----------
    name : str
        Section object name.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, material):
        super(Section, self).__init__(name=name)
        self._material = None
        self.material = material

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if value:
            if not isinstance(value, Material):
                raise ValueError('Material must be of type `compas_fea2.model.Material`.')
            self._material = value


# ==============================================================================
# 0D
# ==============================================================================

class MassSection(FEABase):
    """Section for point mass elements.

    Parameters
    ----------
    name : str
        Section name.
    mass : float
        Point mass value.

    """

    def __init__(self, name, mass):
        super(MassSection, self).__init__(name=name)
        self.mass = mass


class SpringSection(Section):
    """For use with spring elements.

    Parameters
    ----------
    name : str
        Section name.
    forces : dict
        Forces data for non-linear springs.
    displacements : dict
        Displacements data for non-linear springs.
    stiffness : dict
        Elastic stiffness for linear springs.

    Attributes
    ----------
    name : str
        Section object name.
    forces : dict
        Forces data for non-linear springs.
    displacements : dict
        Displacements data for non-linear springs.
    stiffness : dict
        Elastic stiffness for linear springs.

    Note
    ----
    - Force and displacement data should range from negative to positive values.
    - Requires either a stiffness dict for linear springs, or forces and displacement lists for non-linear springs.
    - Directions are 'axial', 'lateral', 'rotation'.

    """

    def __init__(self, name, forces={}, displacements={}, stiffness={}):
        super(SpringSection, self).__init__(name)
        self.forces = forces
        self.displacements = displacements
        self.stiffness = stiffness


# ==============================================================================
# 1D
# ==============================================================================

class BeamSection(Section):
    """Initialises base Section object.

    Parameters
    ----------
    name : str
        Section object name.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, material):
        super(BeamSection, self).__init__(name, material)
        self.A = 0.0
        self.Ixx = 0.0
        self.Iyy = 0.0
        self.Ixy = 0.0
        self.Avx = 0.0
        self.Avy = 0.0
        self.J = 0.0
        self.g0 = 0.0
        self.gw = 0.0


class AngleSection(BeamSection):
    """Uniform thickness angle cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.
    t : float
        Thickness.
    material : obj
        `compas_fea2` Material object.

    Notes
    -----
    - Ixy not yet calculated.

    """

    def __init__(self, name, b, h, t, material):
        super(AngleSection, self).__init__(name, material)
        # parameters
        self.b = b
        self.h = h
        self.t = t
        # aux parameters
        self.p = 2. * (b + h - t)
        self.xc = (b**2 + h * t - t**2) / self.p
        self.yc = (h**2 + b * t - t**2) / self.p
        # default properties
        self.A = t * (b + h - t)
        self.Ixx = (1. / 3) * (b * h**3 - (b - t) * (h - t)**3) - self.A * (h - self.yc)**2
        self.Iyy = (1. / 3) * (h * b**3 - (h - t) * (b - t)**3) - self.A * (b - self.xc)**2
        self.J = (1. / 3) * (h + b - t) * t**3


class BoxSection(BeamSection):
    """Hollow rectangular box cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tf : float
        Flange thickness.
    material : obj
        `compas_fea2` Material object.

    Notes
    -----
    - Ixy not yet calculated.

    """

    def __init__(self, name, b, h, tw, tf, material):
        super(BoxSection, self).__init__(name, material)
        # parameters
        self.b = b
        self.h = h
        self.tw = tw
        self.tf = tf
        # aux parameters
        self.Ap = (h - tf) * (b - tw)
        self.p = 2 * ((h - tf) / tw + (b - tw) / tf)
        # default parameters
        self.A = b * h - (b - 2 * tw) * (h - 2 * tf)
        self.Ixx = (b * h**3) / 12. - ((b - 2 * tw) * (h - 2 * tf)**3) / 12.
        self.Iyy = (h * b**3) / 12. - ((h - 2 * tf) * (b - 2 * tw)**3) / 12.
        self.J = 4 * (self.Ap**2) / self.p


class CircularSection(BeamSection):
    """Solid circular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    r : float
        Radius.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, r, material):
        super(CircularSection, self).__init__(name, material)
        # parameters
        self.r = r
        # aux parameters
        self.D = 2 * r
        # default parameters
        self.A = 0.25 * pi * self.D**2
        self.Ixx = self.Iyy = (pi * self.D**4) / 64.
        self.J = (pi * self.D**4) / 32


class ISection(BeamSection):
    """Equal flanged I-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tf : float
        Flange thickness.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, b, h, tw, tf, material):
        super(ISection, self).__init__(name, material)
        # parameters
        self.b = b
        self.h = h
        self.tw = tw
        self.tf = tf
        # aux parameters
        # default parameters
        self.A = 2 * b * tf + (h - 2 * tf) * tw
        self.Ixx = (tw * (h - 2 * tf)**3) / 12. + 2 * ((tf**3) * b / 12. + b * tf * (h / 2. - tf / 2.)**2)
        self.Iyy = ((h - 2 * tf) * tw**3) / 12. + 2 * ((b**3) * tf / 12.)
        self.J = (1. / 3) * (2 * b * tf**3 + (h - tf) * tw**3)


class PipeSection(BeamSection):
    """Hollow circular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    r : float
        Outer radius.
    t : float
        Wall thickness.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, r, t, material):
        super(PipeSection, self).__init__(name, material)
        # parameters
        self.r = r
        self.t = t
        # aux parameters
        self.D = 2 * r
        # default parameters
        self.A = 0.25 * pi * (self.D**2 - (self.D - 2 * t)**2)
        self.Ixx = self.Iyy = 0.25 * pi * (r**4 - (r - t)**4)
        self.J = (2. / 3) * pi * (r + 0.5 * t) * t**3


class RectangularSection(BeamSection):
    """Solid rectangular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, b, h, material):
        super(RectangularSection, self).__init__(name, material)
        # parameters
        self.b = b
        self.h = h
        # aux parameters
        self.l1 = max([b, h])
        self.l2 = min([b, h])
        # default parameters
        self.A = b * h
        self.Ixx = (1 / 12.) * b * h**3
        self.Iyy = (1 / 12.) * h * b**3
        self.Ixy = 0.
        # self.Avy = 0.833 * A
        # self.Avx = 0.833 * A
        self.J = (self.l1 * self.l2**3) * (0.33333 - 0.21 * (self.l2 / self.l1) * (1 - (self.l2**4) / (self.l2 * self.l1**4)))


class TrapezoidalSection(BeamSection):
    """Solid trapezoidal cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b1 : float
        Width at bottom.
    b2 : float
        Width at top.
    h : float
        Height.
    material : obj
        `compas_fea2` Material object.

    Note
    ----
    - J not yet calculated.

    """

    def __init__(self, name, b1, b2, h, material):
        super(TrapezoidalSection, self).__init__(name, material)
        # parameters
        self.b1 = b1
        self.b2 = b2
        self.h = h
        # aux parameters
        self.c = (h * (2 * b2 + b1)) / (3. * (b1 + b2))  # NOTE: not used
        # default paramters
        self.A = 0.5 * (b1 + b2) * h
        self.Ixx = (1 / 12.) * (3 * b2 + b1) * h**3
        self.Iyy = (1 / 48.) * h * (b1 + b2) * (b2**2 + 7 * b1**2)


class TrussSection(BeamSection):
    """For use with truss elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, A, material):
        super(TrussSection, self).__init__(name, material)
        self.A = A


class StrutSection(TrussSection):
    """For use with strut elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, A, material):
        super(StrutSection, self).__init__(name, A, material)


class TieSection(TrussSection):
    """For use with tie elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, A, material):
        super(TieSection, self).__init__(name, A, material)


# ==============================================================================
# 2D
# ==============================================================================

class ShellSection(Section):
    """Section for shell elements.

    Parameters
    ----------
    name : str
        Section name.
    t : float
        Thickness.
    material : obj
        `compas_fea2` Material object.

    """

    def __init__(self, name, t, material):
        super(ShellSection, self).__init__(name, material)
        self.t = t


class MembraneSection(Section):
    """Section for membrane elements.

    Parameters
    ----------
    name : str
        Section name.
    t : float
        Thickness.
    material : obj
        `compas_fea2` Material object.
    """

    def __init__(self, name, t, material):
        super(MembraneSection, self).__init__(name, material)
        self.t = t


# ==============================================================================
# 3D
# ==============================================================================

class SolidSection(Section):
    """Section for solid elements.

    Parameters
    ----------
    name : str
        Section name.
    material : obj
        `compas_fea2` Material object.
    """

    def __init__(self, name, material):
        super(SolidSection, self).__init__(name, material)
