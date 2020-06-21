
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

#TODO: probably elsest should be defined in the section object definition
def _write_beam_section(obj, elset):
    properties = []
    for l in labels:
        if l in obj.geometry.keys():
            properties.append(str(obj.geometry[l]))
    line="""** Section: {}
*Beam Section, elset={}, material={}
{}\n""".format(obj.name, elset, obj.material.name, ','.join(properties))
    f.write(line)

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
        self.__name__ = 'MassSection'
        self.mass = mass

    def write_data(self, elset, f):
        line="""** Section: {}
*Mass, elset={}
{}\n""".format(self.name, elset, self.mass)
        f.write(line)

# ==============================================================================
# 1D
# ==============================================================================

class AngleSection(AngleSectionBase):

    def __init__(self, name, b, h, t, material):
        super(AngleSection, self).__init__(name, b, h, t, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)

class BoxSection(BoxSectionBase):

    def __init__(self, name, b, h, tw, tf, material):
        super(BoxSection, self).__init__(name, b, h, tw, tf, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)

class CircularSection(CircularSectionBase):

    def __init__(self, name, r, material):
        super(CircularSection, self).__init__(name, r, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)
class GeneralSection(GeneralSectionBase):

    def __init__(self, name, A, Ixx, Ixy, Iyy, J, g0, gw, material):
        super(GeneralSection, self).__init__(name, A, Ixx, Ixy, Iyy, J, g0, gw, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)

class ISection(ISectionBase):

    def __init__(self, name, b, h, tw, tf, material):
        super(ISection, self).__init__(name, b, h, tw, tf, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)

class PipeSection(PipeSectionBase):

    def __init__(self, name, r, t, material):
        super(PipeSection, self).__init__(name, r, t, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)

class RectangularSection(RectangularSectionBase):

    def __init__(self, name, b, h, material):
        super(RectangularSection, self).__init__(name, b, h, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)

class TrapezoidalSection(TrapezoidalSectionBase):

    def __init__(self, name, b1, b2, h, material):
        super(TrapezoidalSection, self).__init__( name, b1, b2, h, material)

    def write_data(self, elset, f):
        _write_beam_section(self,elset)

class TrussSection(TrussSectionBase):

    def __init__(self, name, A, material):
        super(TrussSection, self).__init__(name, A, material)

    def write_data(self, elset, f):
        line="""** Section: {}
*Solid Section, elset={}, material={}
{},\n""".format(self.name, elset, self.material.name, self.geometry['A'])
        f.write(line)

class StrutSection(StrutSectionBase):

    def __init__(self, name, A, material):
        super(StrutSection, self).__init__(name, A, material)


class TieSection(TieSectionBase):

    def __init__(self, name, A, material):
        super(TieSection, self).__init__(name, A, material)


class SpringSection(SpringSectionBase):

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

    def __init__(self, name, t, material, int_points=5):
        super(ShellSection, self).__init__(name, t, material)
        self.__doc__ += ShellSection.__doc__
        self.int_points = int_points

    def write_data(self, elset, f):
        line="""** Section: {}
*Shell Section, elset={}, material={}
{}, {}\n""".format(self.name, elset, self.material.name, self.t, self.int_points)
        f.write(line)

class MembraneSection(MembraneSectionBase):

    def __init__(self, name, t, material):
        super(MembraneSection, self).__init__(name, t, material)

    def write_data(self, elset, f):

        line="""** Section: {}
*Membrane Section, elset={}, material={}
{},\n""".format(self.name, elset, self.material.name, self.t)

        f.write(line)
# ==============================================================================
# 3D
# ==============================================================================

class SolidSection(SolidSectionBase):

    def __init__(self, name, material):
        super(SolidSectionBase, self).__init__(name, material)

    def write_data(self, elset, f):
        print(self.name)
        line="""** Section: {}
*Solid Section, elset={}, material={}
,\n""".format(self.name, elset, self.material.name)
        f.write(line)



if __name__ == "__main__":
    from compas_fea2.backends.abaqus.components import Concrete
    conc = Concrete('my_mat',1,2,3,4)
    solid = BoxSection('mysec', 100, 20,1,2,conc)
    # solid = SolidSection('mysec',conc)
    f=open('/home/fr/Downloads/test_input.inp','w')
    # f = open('C:/temp/input_temp.inp', 'w')
    solid.write_data('my_elset', f)
    f.close

