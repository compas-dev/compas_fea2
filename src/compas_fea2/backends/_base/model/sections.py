
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas_fea2.backends._base.base import FEABase
from compas_fea2.backends._base.model.materials import MaterialBase

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'SectionBase',
    'MassSectionBase',
    'BeamSectionBase',
    'SpringSectionBase',
    'AngleSectionBase',
    'BoxSectionBase',
    'CircularSectionBase',
    'ISectionBase',
    'PipeSectionBase',
    'RectangularSectionBase',
    'ShellSectionBase',
    'MembraneSectionBase',
    'SolidSectionBase',
    'TrapezoidalSectionBase',
    'TrussSectionBase',
    'StrutSectionBase',
    'TieSectionBase',
]


class SectionBase(FEABase):
    """Initialises base Section object.

    Parameters
    ----------
    name : str
        Section object name.
    material : obj
        `compas_fea2` Material object.
    """

    def __init__(self, name, material):
        super(SectionBase, self).__init__()
        self.__name__ = 'Section'
        self._name = name
        self._material = material

    @property
    def name(self):
        """The name property."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def material(self):
        """obj : `compas_fea2` Material object."""
        return self._material

    @material.setter
    def material(self, value):
        if not isinstance(value, MaterialBase):
            raise ValueError('must be a `compas_fea2` Material object')
        self._material = value

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

# ==============================================================================
# 0D
# ==============================================================================


class MassSectionBase(FEABase):
    """Section for point mass elements.

    Parameters
    ----------
    name : str
        Section name.
    mass : float
        Point mass value.
    """

    def __init__(self, name, mass):
        super(SectionBase, self).__init__()
        self._name = name
        self._mass = mass

    @property
    def name(self):
        """The name of the section."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def mass(self):
        """float : Point mass value."""
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value


class SpringSectionBase(SectionBase):
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
        super(SpringSectionBase, self).__init__(self, name)

        self.__name__ = 'SpringSection'
        self.geometry = None
        self.material = None
        self.forces = forces
        self.displacements = displacements
        self.stiffness = stiffness

# ==============================================================================
# 1D
# ==============================================================================


class BeamSectionBase(SectionBase):
    """Initialises base Section object.

    Parameters
    ----------
    name : str
        Section object name.
    material : obj
        `compas_fea2` Material object.
    """

    def __init__(self, name, material):
        super(BeamSectionBase, self).__init__(name, material)
        self.__name__ = 'BeamSection'

        self._A = 0.
        self._Ixx = 0.
        self._Iyy = 0.
        self._Ixy = 0.
        self._Avx = 0.
        self._Avy = 0.
        self._J = 0.
        self._g0 = 0.
        self._gw = 0.

    @property
    def A(self):
        """float : The area of the section."""
        return self._A

    @A.setter
    def A(self, value):
        self._A = value

    @property
    def Ixx(self):
        """float: Second moment of area about axis x-x."""
        return self._Ixx

    @Ixx.setter
    def Ixx(self, value):
        self._Ixx = value

    @property
    def Iyy(self):
        """float: Second moment of area about axis y-y."""
        return self._Iyy

    @Iyy.setter
    def Iyy(self, value):
        self._Iyy = value

    @property
    def Ixy(self):
        """float : Cross moment of area.."""
        return self._Ixy

    @Ixy.setter
    def Ixy(self, value):
        self._Ixy = value

    @property
    def Avx(self):
        """float : shear area along x."""
        return self._Avx

    @Avx.setter
    def Avx(self, value):
        self._Avx = value

    @property
    def Avy(self):
        """float : shear area along y."""
        return self._Avy

    @Avy.setter
    def Avy(self, value):
        self._Avy = value

    @property
    def J(self):
        """float : Torsional rigidity."""
        return self._J

    @J.setter
    def J(self, value):
        self._J = value

    @property
    def g0(self):
        """float : Sectorial moment."""
        return self._g0

    @g0.setter
    def g0(self, value):
        self._g0 = value

    @property
    def gw(self):
        """float : Warping constant."""
        return self._gw

    @gw.setter
    def gw(self, value):
        self._gw = value

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class AngleSectionBase(BeamSectionBase):
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
        super(AngleSectionBase, self).__init__(name, material)
        # parameters
        self.__name__ = 'AngleSection'
        self._b = b
        self._h = h
        self._t = t
        # aux parameters
        self._p = 2. * (b + h - t)
        self._xc = (b**2 + h * t - t**2) / self._p
        self._yc = (h**2 + b * t - t**2) / self._p
        # default properties
        self._A = t * (b + h - t)
        self._Ixx = (1. / 3) * (b * h**3 - (b - t) * (h - t)**3) - self._A * (h - self._yc)**2
        self._Iyy = (1. / 3) * (h * b**3 - (h - t) * (b - t)**3) - self._A * (b - self._xc)**2
        self._J = (1. / 3) * (h + b - t) * t**3


class BoxSectionBase(BeamSectionBase):
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
        super(BoxSectionBase, self).__init__(name, material)
        # parameters
        self.__name__ = 'BoxSection'
        self._b = b
        self._h = h
        self._tw = tw
        self._tf = tf
        # aux parameters
        self._Ap = (h - tf) * (b - tw)
        self._p = 2 * ((h - tf) / tw + (b - tw) / tf)
        # default parameters
        self._A = b * h - (b - 2 * tw) * (h - 2 * tf)
        self._Ixx = (b * h**3) / 12. - ((b - 2 * tw) * (h - 2 * tf)**3) / 12.
        self._Iyy = (h * b**3) / 12. - ((h - 2 * tf) * (b - 2 * tw)**3) / 12.
        self._J = 4 * (self._Ap**2) / self._p


class CircularSectionBase(BeamSectionBase):
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
        super(CircularSectionBase, self).__init__(name, material)
        # parameters
        self.__name__ = 'CircularSection'
        self._r = r
        # aux parameters
        self._D = 2 * r
        # default parameters
        self._A = 0.25 * pi * self._D**2
        self._Ixx = Iyy = (pi * self._D**4) / 64.
        self._J = (pi * self._D**4) / 32


class ISectionBase(BeamSectionBase):
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
        super(ISectionBase, self).__init__(name, material)
        # parameters
        self.__name__ = 'ISection'
        self._b = b
        self._h = h
        self._tw = tw
        self._tf = tf
        # aux parameters

        # default parameters
        self._A = 2 * b * tf + (h - 2 * tf) * tw
        self._Ixx = (tw * (h - 2 * tf)**3) / 12. + 2 * ((tf**3) * b / 12. + b * tf * (h / 2. - tf / 2.)**2)
        self._Iyy = ((h - 2 * tf) * tw**3) / 12. + 2 * ((b**3) * tf / 12.)
        self._J = (1. / 3) * (2 * b * tf**3 + (h - tf) * tw**3)


class PipeSectionBase(BeamSectionBase):
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
        super(PipeSectionBase, self).__init__(name, material)
        # parameters
        self.__name__ = 'PipeSection'
        self._r = r
        self._t = t
        # aux parameters
        self._D = 2 * r
        # default parameters
        A = 0.25 * pi * (self._D**2 - (self._D - 2 * t)**2)
        Ixx = Iyy = 0.25 * pi * (r**4 - (r - t)**4)
        J = (2. / 3) * pi * (r + 0.5 * t) * t**3


class RectangularSectionBase(BeamSectionBase):
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
        super(RectangularSectionBase, self).__init__(name, material)
        # parameters
        self.__name__ = 'RectangularSection'
        self._b = b
        self._h = h
        # aux parameters
        self._l1 = max([b, h])
        self._l2 = min([b, h])
        # default parameters
        self._A = b * h
        self._Ixx = (1 / 12.) * b * h**3
        self._Iyy = (1 / 12.) * h * b**3
        self._Ixy = 0.
        # self._Avy = 0.833 * A
        # self._Avx = 0.833 * A
        self._J = (self._l1 * self._l2**3) * (0.33333 - 0.21 *
                                              (self._l2 / self._l1) * (1 - (self._l2**4) / (self._l2 * self._l1**4)))


class TrapezoidalSectionBase(BeamSectionBase):
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
        super(TrapezoidalSectionBase, self).__init__(name, material)
        # parameters
        self.__name__ = 'TrapezoidalSection'
        self._b1 = b1
        self._b2 = b2
        self._h = h
        # aux parameters
        self._c = (h * (2 * b2 + b1)) / (3. * (b1 + b2))  # NOTE: not used
        # default paramters
        self._A = 0.5 * (b1 + b2) * h
        self._Ixx = (1 / 12.) * (3 * b2 + b1) * h**3
        self._Iyy = (1 / 48.) * h * (b1 + b2) * (b2**2 + 7 * b1**2)


class TrussSectionBase(BeamSectionBase):
    """For use with truss elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.
    material : obj
        `compas_fea2` Material object.

    Attributes
    ----------
    name : str
        Section object name.
    material : obj
        `compas_fea2` Material object.
    geometry : dict
        Dictionary containing the geometric properties of the section.
    """

    def __init__(self, name, A, material):
        super(TrussSectionBase, self).__init__(name, material)

        # parameters
        self.__name__ = 'TrussSection'
        # aux parameters
        # default paramters
        self._A = A


class StrutSectionBase(TrussSectionBase):
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
        super(StrutSectionBase, self).__init__(name, A, material)

        self.__name__ = 'StrutSection'


class TieSectionBase(TrussSectionBase):
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
        super(TieSectionBase, self).__init__(name, A, material)

        self.__name__ = 'TieSection'


# ==============================================================================
# 2D
# ==============================================================================

class ShellSectionBase(SectionBase):
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
        super(ShellSectionBase, self).__init__(name, material)

        self.__name__ = 'ShellSection'
        self._t = t

    @property
    def t(self):
        """float : The thickness of the shell."""
        return self._t

    @t.setter
    def t(self, value):
        self._t = value


class MembraneSectionBase(SectionBase):
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
        super(MembraneSectionBase, self).__init__(name, material)

        self.__name__ = 'MembraneSection'
        self._t = t

    @property
    def t(self):
        """float : The thickness of the membrane."""
        return self._t

    @t.setter
    def t(self, value):
        self._t = value


# ==============================================================================
# 3D
# ==============================================================================

class SolidSectionBase(SectionBase):
    """Section for solid elements.

    Parameters
    ----------
    name : str
        Section name.
    material : obj
        `compas_fea2` Material object.
    """

    def __init__(self, name, material):
        super(SolidSectionBase, self).__init__(name, material)

        self.__name__ = 'SolidSection'
