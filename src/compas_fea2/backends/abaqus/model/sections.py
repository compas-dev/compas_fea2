
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas_fea2.backends._base.model import SectionBase
from compas_fea2.backends._base.model import GeneralSectionBase
from compas_fea2.backends._base.model import ShellSectionBase
from compas_fea2.backends._base.model import MembraneSectionBase
from compas_fea2.backends._base.model import SolidSectionBase
from compas_fea2.backends._base.model import TrussSectionBase
from compas_fea2.backends._base.model import StrutSectionBase
from compas_fea2.backends._base.model import TieSectionBase
from compas_fea2.backends._base.model import SpringSectionBase


# Author(s): Francesco Ranaudo (github.com/franaudo)
#           Andrew Liew (github.com/andrewliew)


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


class AbaqusBeamSection(SectionBase):
    """
    Notes
    -----
    The properties for beam sections are automatically computed by Abaqus.
    """

    def __init__(self, name, material):
        super(AbaqusBeamSection, self).__init__(name, material)

    def _generate_data(self, set_name, orientation):
        orientation_line = ', '.join([str(v) for v in orientation])
        return """** Section: {}
*Beam Section, elset={}, material={}, section={}
{}\n{}\n""".format(self.name, set_name, self.material, self._stype, ', '.join([str(v) for v in self.properties]), orientation_line)


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


class GeneralSection(GeneralSectionBase):

    def __init__(self, name, A, Ixx, Ixy, Iyy, J, g0, gw, material):
        super(GeneralSection, self).__init__(name, A, Ixx, Ixy, Iyy, J, g0, gw, material)


class AngleSection(AbaqusBeamSection):
    """L section.

    Parameters
    ----------
    a : float
        base of the section.
    b : float
        total height of the section (including the flanges).
    t : float or list
        thickness(es) of the section. If the two thicknesses are different,
        provide a list the two values [t1, t2]
    material : str
        material name to be assigned to the section.
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, a, b, t, material):
        super(ISection, self).__init__(name, material)
        self._stype = 'L'
        if not isinstance(t, list):
            t = [t]*2
        self.properties = [a, b, *t]


class BoxSection(AbaqusBeamSection):
    """Box section.

    Parameters
    ----------
    a : float
        base of the section.
    b : float
        total height of the section (including the flanges).
    t : float or list
        thickness(es) of the section. If the four thicknesses are different,
        provide a list the four values [t1, t2, t3, t4]
    material : str
        material name to be assigned to the section.
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, a, b, t, material):
        super(BoxSection, self).__init__(name, material)
        self._stype = 'box'
        if not isinstance(t, list):
            t = [t]*4
        elif not len(t) == 4:
            raise ValueError("You must specify a tickness for every side of the box")
        self.properties = [a, b, *t]


class CircularSection(AbaqusBeamSection):
    """Circular filled section.

    Parameters
    ----------
    r : float
        outside radius
    material : str
        material name to be assigned to the section.
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, r, material):
        super(CircularSection, self).__init__(name, material)
        self._stype = 'circ'
        self.properties = [r]


class HexSection(AbaqusBeamSection):
    """Hexagonal hollow section.

    Parameters
    ----------
    r : float
        outside radius
    t : float
        wall thickness
    material : str
        material name to be assigned to the section.
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, d, t, material):
        super(HexSection, self).__init__(name, r, material)
        self._stype = 'hex'
        self.properties = [d, t]


class ISection(AbaqusBeamSection):
    """I or T section.

    Parameters
    ----------
    b : float or list
        base(s) of the section. If the two bases are different, provide a list
        with the two values [b1, b2]
    h : float
        total height of the section (including the flanges).
    t : float or list
        thickness(es) of the section. If the three thicknesses are different,
        provide a list the three values [t1, t2, t3]
    material : str
        material name to be assigned to the section.
    l : float
        distance of the origin of the local cross-section axis from the origin
        of the beam axis along the 2-axis, by default 0.

    Notes
    -----
    Set b1 and t1 or b2 and t2 to zero to model a T-section
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, b, h, t, material, l=0):
        super(ISection, self).__init__(name, material)
        self._stype = 'I'
        if not isinstance(b, list):
            b = [b]*2
        if not isinstance(t, list):
            t = [t]*3
        self.properties = [l, h, *b, *t]


class PipeSection(AbaqusBeamSection):
    """Pipe section.

    Parameters
    ----------
    r : float
        outside radius
    t : float
        wall thickness
    material : str
        material name to be assigned to the section.
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, r, t, material):
        super(PipeSection, self).__init__(name, material)
        self._stype = 'pipe'
        self.properties = [r, t]


class RectangularSection(AbaqusBeamSection):
    """Rectangular filled section.

    Parameters
    ----------
    a : float
        base of the section.
    b : float
        height of the section.
    material : str
        material name to be assigned to the section.
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, a, b, material):
        super(RectangularSection, self).__init__(name, material)
        self._stype = 'rect'
        self.properties = [a, b]


class TrapezoidalSection(AbaqusBeamSection):
    """Rectangular filled section.

    Parameters
    ----------
    a : float
        bottom base of the section.
    b : float
        height of the section.
    c : float
        top base of the section.
    d : float
        distance of the origin of the local cross-section axis from the origin
        of the beam axis along the 2-axis, by default 0.
    material : str
        material name to be assigned to the section.
    """
    __doc__ += AbaqusBeamSection.__doc__

    def __init__(self, name, a, b, c, d, material):
        super(TrapezoidalSection, self).__init__(name, material)
        self._stype = 'rect'
        self.properties = [a, b, c, d]


# TODO -> check how these sections are implemented in ABAQUS
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
    Parameters
    ----------
    name : str
        name of the section
    t : float
        thickness of the section
    material : obj
        compas_fea2 Material object
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
{}, {}\n""".format(self.name, set_name, self.material, self.t, self.int_points)


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
,\n""".format(self.name, set_name, self.material)


if __name__ == "__main__":

    from compas_fea2.backends.abaqus import Concrete

    conc = Concrete('my_mat', 1, 2, 3, 4)
    solid = BoxSection('mysec', 100, 20, 1, 2, conc)

    print(solid.jobdata)
