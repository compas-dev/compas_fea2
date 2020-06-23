
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

#TODO: elset should come from the element the section is assigned to and not form the section itself...

def _generate_beam_data(obj):
    properties = []
    for l in labels:
        if l in obj.geometry.keys():
            properties.append(str(obj.geometry[l]))
    return """** Section: {}
*Beam Section, elset={}, material={}
{}\n""".format(obj.name, obj.elset, obj.material.name, ','.join(properties))


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

    def __init__(self, name, mass, elset=None):
        super(MassSection, self).__init__(name)
        self.mass = mass

        self.data = """** Section: {}
*Mass, elset={}
{}\n""".format(name, elset, mass)

# ==============================================================================
# 1D
# ==============================================================================

class AngleSection(AngleSectionBase):

    def __init__(self, name, b, h, t, material, elset=None):
        super(AngleSection, self).__init__(name, b, h, t, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class BoxSection(BoxSectionBase):

    def __init__(self, name, b, h, tw, tf, material, elset=None):
        super(BoxSection, self).__init__(name, b, h, tw, tf, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class CircularSection(CircularSectionBase):

    def __init__(self, name, r, material, elset=None):
        super(CircularSection, self).__init__(name, r, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class GeneralSection(GeneralSectionBase):

    def __init__(self, name, A, Ixx, Ixy, Iyy, J, g0, gw, material, elset=None):
        super(GeneralSection, self).__init__(name, A, Ixx, Ixy, Iyy, J, g0, gw, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class ISection(ISectionBase):

    def __init__(self, name, b, h, tw, tf, material, elset=None):
        super(ISection, self).__init__(name, b, h, tw, tf, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class PipeSection(PipeSectionBase):

    def __init__(self, name, r, t, material, elset=None):
        super(PipeSection, self).__init__(name, r, t, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class RectangularSection(RectangularSectionBase):

    def __init__(self, name, b, h, material, elset=None):
        super(RectangularSection, self).__init__(name, b, h, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class TrapezoidalSection(TrapezoidalSectionBase):

    def __init__(self, name, b1, b2, h, material, elset=None):
        super(TrapezoidalSection, self).__init__( name, b1, b2, h, material)
        self.elset = elset
        self.data = _generate_beam_data(self)


class TrussSection(TrussSectionBase):

    def __init__(self, name, A, material, elset=None):
        super(TrussSection, self).__init__(name, A, material)
        self.elset = elset
        self.data = """** Section: {}
*Solid Section, elset={}, material={}
{},\n""".format(self.name, elset, self.material.name, self.geometry['A'])


class StrutSection(StrutSectionBase):

    def __init__(self, name, A, material, elset=None):
        super(StrutSection, self).__init__(name, A, material)
        self.elset = elset

class TieSection(TieSectionBase):

    def __init__(self, name, A, material, elset=None):
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

    def __init__(self, name, t, material, elset=None, int_points=5):
        super(ShellSection, self).__init__(name, t, material)
        self.__doc__ += ShellSection.__doc__
        self.elset = elset
        self.int_points = int_points
        self.data = """** Section: {}
*Shell Section, elset={}, material={}
{}, {}\n""".format(self.name, self.elset, self.material.name, self.t, self.int_points)


class MembraneSection(MembraneSectionBase):

    def __init__(self, name, t, material, elset=None):
        super(MembraneSection, self).__init__(name, t, material)
        self.elset = elset
        self.data = """** Section: {}
*Membrane Section, elset={}, material={}
{},\n""".format(self.name, elset, self.material.name, self.t)

# ==============================================================================
# 3D
# ==============================================================================

class SolidSection(SolidSectionBase):

    def __init__(self, name, material, elset=None):
        super(SolidSectionBase, self).__init__(name, material)
        self.elset = elset
        self.data = """** Section: {}
*Solid Section, elset={}, material={}
,\n""".format(self.name, elset, self.material.name)


if __name__ == "__main__":

    from compas_fea2.backends.abaqus.components import Concrete

    conc = Concrete('my_mat',1,2,3,4)
    solid = BoxSection('mysec', 100, 20,1,2,conc)
    # solid = SolidSection('mysec',conc)
    # f=open('/home/fr/Downloads/test_input.inp','w')
    # # f = open('C:/temp/input_temp.inp', 'w')
    # solid.write_data('my_elset', f)
    # f.close

    print(solid.data)
