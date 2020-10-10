
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas_fea2.backends._base.model import SectionBase
from compas_fea2.backends._base.model import AngleSectionBase
from compas_fea2.backends._base.model import BoxSectionBase
from compas_fea2.backends._base.model import CircularSectionBase
from compas_fea2.backends._base.model import GeneralSectionBase
from compas_fea2.backends._base.model import ISectionBase
from compas_fea2.backends._base.model import PipeSectionBase
from compas_fea2.backends._base.model import RectangularSectionBase
from compas_fea2.backends._base.model import ShellSectionBase
from compas_fea2.backends._base.model import MembraneSectionBase
from compas_fea2.backends._base.model import SolidSectionBase
from compas_fea2.backends._base.model import TrapezoidalSectionBase
from compas_fea2.backends._base.model import TrussSectionBase
from compas_fea2.backends._base.model import StrutSectionBase
from compas_fea2.backends._base.model import TieSectionBase
from compas_fea2.backends._base.model import SpringSectionBase


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'MassSection',
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
]

labels = ['A', 'Ixx', 'Ixy', 'Iyy', 'J', 'g0', 'gw']

def _generate_beam_data(obj):
    properties = []
    for l in labels:
        if l in obj.geometry.keys():
            properties.append(str(obj.geometry[l]))
    return """** Section: {}
*Beam Section, elset={}, material={}, section={}
{}\n""".format(obj.name, obj.elset, obj.material.name, obj.stype, ','.join(properties))


# ==============================================================================
# 0D
# ==============================================================================

class MassSection(SectionBase):
    """Section for mass elements.

    Parameters
    ----------
    name : str
        Section name.
    mass : float
        Point mass value.
    """

    def __init__(self, name, mass):
        super(MassSection, self).__init__(name)
        self.mass = mass

    def _generate_data(self, set_name, orientation):
        return """** Section: {}
*Mass, elset={}
{}\n""".format(self.name, set_name, self.mass)

# ==============================================================================
# 1D
# ==============================================================================

class AngleSection(AngleSectionBase):

    def __init__(self, name, b, h, t, material):
        super(AngleSection, self).__init__(name, b, h, t, material)
        # self.data = _generate_beam_data(self)


class BoxSection(BoxSectionBase):
    """
    Note: Section properties are computed automatically by Abaqus.
    """
    def __init__(self, name, a, b, t1, t2, t3, t4, material):
        super(BoxSection, self).__init__(name, material)
        self.stype = 'box'
        self.properties = [str(a), str(b), str(t1), str(t2), str(t3), str(t4)]

    def _generate_data(self, set_name, orientation):
        orientation_line = ', '.join([str(v) for v in orientation])
        return """** Section: {}
*Beam Section, elset={}, material={}, section={}
{}\n{}\n""".format(self.name, set_name, self.material, self.stype, ', '.join(self.properties), orientation_line)


class CircularSection(CircularSectionBase):

    def __init__(self, name, r, material):
        super(CircularSection, self).__init__(name, r, material)
        # self.data = _generate_beam_data(self)


class GeneralSection(GeneralSectionBase):

    def __init__(self, name, A, Ixx, Ixy, Iyy, J, g0, gw, material):
        super(GeneralSection, self).__init__(name, A, Ixx, Ixy, Iyy, J, g0, gw, material)
        # self.data = _generate_beam_data(self)


class ISection(ISectionBase):

    def __init__(self, name, b, h, tw, tf, material):
        super(ISection, self).__init__(name, b, h, tw, tf, material)
        # self.data = _generate_beam_data(self)


class PipeSection(PipeSectionBase):

    def __init__(self, name, r, t, material):
        super(PipeSection, self).__init__(name, r, t, material)
        # self.data = _generate_beam_data(self)


class RectangularSection(RectangularSectionBase):

    def __init__(self, name, b, h, material):
        super(RectangularSection, self).__init__(name, b, h, material)
        # self.data = _generate_beam_data(self)


class TrapezoidalSection(TrapezoidalSectionBase):

    def __init__(self, name, b1, b2, h, material):
        super(TrapezoidalSection, self).__init__( name, b1, b2, h, material)
        # self.data = _generate_beam_data(self)


class TrussSection(TrussSectionBase):

    def __init__(self, name, A, material):
        super(TrussSection, self).__init__(name, A, material)

    def _generate_data(self, set_name):
        return """** Section: {}
*Solid Section, elset={}, material={}
{},\n""".format(self.name, set_name, self.material, self.geometry['A'])


class StrutSection(StrutSectionBase):

    def __init__(self, name, A, material):
        super(StrutSection, self).__init__(name, A, material)
        self.elset = elset

class TieSection(TieSectionBase):

    def __init__(self, name, A, material):
        super(TieSection, self).__init__(name, A, material)
        self.elset = elset

class SpringSection(SpringSectionBase):

    def __init__(self, name, forces={}, displacements={}, stiffness={}):
        super(SpringSection, self).__init__(name, forces={}, displacements={}, stiffness={})
        self.elset = elset

# ==============================================================================
# 2D
# ==============================================================================

class ShellSection(ShellSectionBase):

    """
    int_points : int
        number of integration points. 5 by default.

    """

    def __init__(self, name, t, material, int_points=5):
        super(ShellSection, self).__init__(name, t, material)
        self.__doc__ += ShellSection.__doc__
        self.int_points = int_points

    def _generate_data(self, set_name):
        return """** Section: {}
*Shell Section, elset={}, material={}
{}, {}\n""".format(self.name, set_name, self.material.name, self.t, self.int_points)


class MembraneSection(MembraneSectionBase):

    def __init__(self, name, t, material):
        super(MembraneSection, self).__init__(name, t, material)

    def _generate_data(self, set_name):
        return """** Section: {}
*Membrane Section, elset={}, material={}
{},\n""".format(self.name, set_name, self.material.name, self.t)

# ==============================================================================
# 3D
# ==============================================================================

class SolidSection(SolidSectionBase):

    def __init__(self, name, material):
        super(SolidSectionBase, self).__init__(name, material)

    def _generate_data(self, set_name):
        return """** Section: {}
*Solid Section, elset={}, material={}
,\n""".format(self.name, set_name, self.material.name)


if __name__ == "__main__":

    from compas_fea2.backends.abaqus import Concrete

    conc = Concrete('my_mat',1,2,3,4)
    solid = BoxSection('mysec', 100, 20,1,2,conc)

    print(solid.data)
