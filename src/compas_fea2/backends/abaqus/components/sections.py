
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas_fea2.backends._core import SectionBase
from compas_fea2.backends._core import AngleSectionBase
from compas_fea2.backends._core import BoxSectionBase
from compas_fea2.backends._core import CircularSectionBase
from compas_fea2.backends._core import GeneralSectionBase
from compas_fea2.backends._core import ISectionBase
from compas_fea2.backends._core import PipeSectionBase
from compas_fea2.backends._core import RectangularSectionBase
from compas_fea2.backends._core import ShellSectionBase
from compas_fea2.backends._core import MembraneSectionBase
from compas_fea2.backends._core import SolidSectionBase
from compas_fea2.backends._core import TrapezoidalSectionBase
from compas_fea2.backends._core import TrussSectionBase
from compas_fea2.backends._core import StrutSectionBase
from compas_fea2.backends._core import TieSectionBase
from compas_fea2.backends._core import SpringSectionBase
from compas_fea2.backends._core import MassSectionBase


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

    def __init__(self, name, A):
        super(TrussSection, self).__init__(name, A)

    def write_data(self, elset, f):

        line="""** Section: {}
*Solid Section, elset={}, material={}
{},""".format(self.name, elset, self.material.name, self.geometry['A'])

        f.write(line)

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

    """
    int_points : int
        number of integration points. 5 by default.

    """
    def __init__(self, name, t, int_points=5):
        super(ShellSection, self).__init__(name, t)
        self.__doc__ += ShellSection.__doc__
        self.int_points = int_points

    def write_data(self, elset, f):

        line="""** Section: {}
*Shell Section, elset={}, material={}
{}, {}""".format(self.name, elset, self.material.name, self.t, self.int_points)

        f.write(line)

class MembraneSection(MembraneSectionBase):

    # def __init__(self, name, t):
    #     super(MembraneSection, self).__init__(name, t)

    def write_data(self, elset, f):

        line="""** Section: {}
*Membrane Section, elset={}, material={}
{},""".format(self.name, elset, self.material.name, self.t)

        f.write(line)
# ==============================================================================
# 3D
# ==============================================================================

class SolidSection(SolidSectionBase):

    def __init__(self, name, material):
        super(SolidSectionBase, self).__init__(name, material)

    def write_data(self, elset, f):

        line="""** Section: {}
*Solid Section, elset={}, material={}
,""".format(self.name, elset, self.material.name)

        f.write(line)



if __name__ == "__main__":
    shell = SolidSection('mysec', material='mat')

    print(shell.material)
