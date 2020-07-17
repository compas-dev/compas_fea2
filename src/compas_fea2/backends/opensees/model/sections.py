
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas_fea2.backends._core.model import SectionBase
from compas_fea2.backends._core.model import AngleSectionBase
from compas_fea2.backends._core.model import BoxSectionBase
from compas_fea2.backends._core.model import CircularSectionBase
from compas_fea2.backends._core.model import GeneralSectionBase
from compas_fea2.backends._core.model import ISectionBase
from compas_fea2.backends._core.model import PipeSectionBase
from compas_fea2.backends._core.model import RectangularSectionBase
from compas_fea2.backends._core.model import ShellSectionBase
from compas_fea2.backends._core.model import MembraneSectionBase
from compas_fea2.backends._core.model import SolidSectionBase
from compas_fea2.backends._core.model import TrapezoidalSectionBase
from compas_fea2.backends._core.model import TrussSectionBase
from compas_fea2.backends._core.model import StrutSectionBase
from compas_fea2.backends._core.model import TieSectionBase
from compas_fea2.backends._core.model import SpringSectionBase
from compas_fea2.backends._core.model import MassSectionBase


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Section',
    'AngleSection',
    'BoxSection',
    'CircularSection',
    'GeneralSection',
    'ISection',
    'PipeSection',
    'RectangularSection',
    'ShellSection',
    'MembraneSection',
    'SolidSection',
    'TrapezoidalSection',
    'TrussSection',
    'StrutSection',
    'TieSection',
    'SpringSection',
    'MassSection'
]


class Section(SectionBase):

    """ Initialises base Section object.

    Parameters
    ----------
    name : str
        Section object name.

    Attributes
    ----------
    name : str
        Section object name.
    geometry : dict
        Geometry of the Section.

    """

    def __init__(self, name):
        super(Section, self).__init__(name)


# ==============================================================================
# 0D
# ==============================================================================

class MassSection(MassSectionBase):

    """ Section for mass elements.

    Parameters
    ----------
    name : str
        Section name.

    """

    def __init__(self, name):
        super(MassSection, self).__init__(name)


# ==============================================================================
# 1D
# ==============================================================================

class AngleSection(AngleSectionBase):

    """ Uniform thickness angle cross-section for beam elements.

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

    Notes
    -----
    - Ixy not yet calculated.

    """

    def __init__(self, name, b, h, t):
        super(AngleSection, self).__init__(name, b, h, t)


class BoxSection(BoxSectionBase):

    """ Hollow rectangular box cross-section for beam elements.

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

    """

    def __init__(self, name, b, h, tw, tf):
        super(BoxSection, self).__init__(name, b, h, tw, tf)


class CircularSection(CircularSectionBase):

    """ Solid circular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    r : float
        Radius.

    """

    def __init__(self, name, r):
        super(CircularSection, self).__init__(name, r)


class GeneralSection(GeneralSectionBase):

    """ General cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.
    Ixx : float
        Second moment of area about axis x-x.
    Ixy : float
        Cross moment of area.
    Iyy : float
        Second moment of area about axis y-y.
    J : float
        Torsional rigidity.
    g0 : float
        Sectorial moment.
    gw : float
        Warping constant.

    """

    def __init__(self, name, A, Ixx, Ixy, Iyy, J, g0, gw):
        super(GeneralSection, self).__init__(name, A, Ixx, Ixy, Iyy, J, g0, gw)


class ISection(ISectionBase):

    """ Equal flanged I-section for beam elements.

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

    """

    def __init__(self, name, b, h, tw, tf):
        super(ISection, self).__init__(name, b, h, tw, tf)


class PipeSection(PipeSectionBase):

    """ Hollow circular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    r : float
        Outer radius.
    t : float
        Wall thickness.

    """

    def __init__(self, name, r, t):
        super(PipeSection, self).__init__(name, r, t)


class RectangularSection(RectangularSectionBase):

    """ Solid rectangular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.

    """

    def __init__(self, name, b, h):
        super(RectangularSection, self).__init__(name, b, h)


class TrapezoidalSection(TrapezoidalSectionBase):

    """ Solid trapezoidal cross-section for beam elements.

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

    Notes
    -----
    - J not yet calculated.

    """

    def __init__(self, name, b1, b2, h):
        super(TrapezoidalSection, self).__init__( name, b1, b2, h)


class TrussSection(TrussSectionBase):

    """ For use with truss elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.

    """

    def __init__(self, name, A):
        super(TrussSection, self).__init__(name, A)


class StrutSection(StrutSectionBase):

    """ For use with strut elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.

    """

    def __init__(self, name, A):
        super(StrutSection, self).__init__(name, A)


class TieSection(TieSectionBase):

    """ For use with tie elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.

    """

    def __init__(self, name, A):
        super(TieSection, self).__init__(name, A)


class SpringSection(SpringSectionBase):

    """ For use with spring elements.

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

    Notes
    -----
    - Force and displacement data should range from negative to positive values.
    - Requires either a stiffness dict for linear springs, or forces and displacement lists for non-linear springs.
    - Directions are 'axial', 'lateral', 'rotation'.

    """

    def __init__(self, name, forces={}, displacements={}, stiffness={}):
        super(SpringSection, self).__init__(name, forces={}, displacements={}, stiffness={})


# ==============================================================================
# 2D
# ==============================================================================

class ShellSection(ShellSectionBase):

    """ Section for shell elements.

    Parameters
    ----------
    name : str
        Section name.
    t : float
        Thickness.

    """
    pass
    # def __init__(self, name, t):
    #     super(ShellSection, self).__init__(name, t)


class MembraneSection(MembraneSectionBase):

    """ Section for membrane elements.

    Parameters
    ----------
    name : str
        Section name.
    t : float
        Thickness.

    """
    pass
    # def __init__(self, name, t):
    #     super(MembraneSection, self).__init__(name, t)


# ==============================================================================
# 3D
# ==============================================================================

class SolidSection(SolidSectionBase):

    """ Section for solid elements.

    Parameters
    ----------
    name : str
        Section name.

    """
    pass
    # def __init__(self, name):
    #     super(SolidSection, self).__init__(name)



