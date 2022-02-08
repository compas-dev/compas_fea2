from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class Element(FEABase):
    """Initialises a base Element object.

    Parameters
    ----------
    key : int
        Key number of the element.
    connectivity : list[int]
        Ordered nodes keys the element connects to.
    section : :class:`compas_fea2.model.SectionBase`
        Section Object assigned to the element.
    thermal : bool, optional
        Thermal properties on or off, by default None
    name : str, optional
        The name of the Element, by default the element key.

    Warnings
    --------
    The connectivity of the element must be provided in the correct order!

    """

    def __init__(self, connectivity, section, thermal=False, name=None):
        super(Element, self).__init__(name=name)
        self._key = None
        self._connectivity = connectivity  # TODO add find node method to get the connectivity from the Node object
        self._connectivity_key = '_'.join(sorted([str(c) for c in self.connectivity]))
        self._connected_nodes = []
        self._section = section
        self._thermal = thermal
        self._axes = None

    @property
    def key(self):
        """int : Key number of the element."""
        return self._key

    @property
    def connectivity(self):
        """list[int] : list of nodes keys the element connects to."""
        return self._connectivity

    @connectivity.setter
    def connectivity(self, value):
        self._connectivity = value

    @property
    def connectivity_key(self):
        """str : string identifier of the conntected nodes"""
        return self._connectivity_key

    @property
    def section(self):
        """:class:`compas_fea2.model.SectionBase` : object or name of a Section previously added to the model."""
        return self._section

    @section.setter
    def section(self, value):
        self._section = value

    @property
    def thermal(self):
        """The thermal property."""
        return self._thermal

    @thermal.setter
    def thermal(self, value):
        self._thermal = value

    @property
    def axes(self):
        """The axes property."""
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value


# ==============================================================================
# 0D elements
# ==============================================================================

class MassElement(Element):
    """A 0D element for concentrated point mass.
    """

    def __init__(self, key, node, mass, elset):
        super(MassElement, self).__init__()
        self.key = key
        self.node = node
        self.mass = mass
        self.elset = elset

    # def __str__(self):
    #     print('\n')
    #     print('compas_fea2 {0} object'.format(self.__name__))
    #     print('-' * (len(self.__name__) + 18))
    #     for attr in ['key', 'eltype', 'elset', 'mass']:
    #         print('{0:<10} : {1}'.format(attr, getattr(self, attr)))
    #     return ''

    # def __repr__(self):
    #     return '{0}({1})'.format(self.__name__, self.key)


# ==============================================================================
# 1D elements
# ==============================================================================

class BeamElement(Element):
    """A 1D element that resists axial, shear, bending and torsion.
    """

    def __init__(self, connectivity, section, thermal=None):
        super(BeamElement, self).__init__(connectivity, section, thermal)


class SpringElement(Element):
    """A 1D spring element.
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(SpringElement, self).__init__(key, connectivity, section, thermal)


class TrussElement(Element):
    """A 1D element that resists axial loads.
    """

    def __init__(self, connectivity, section, thermal=None):
        super(TrussElement, self).__init__(connectivity, section, thermal)

    def _checks(self):
        if self.section.__name__ in []:
            raise TypeError("The chosen section cannot be applied to Truss elements")


class StrutElement(TrussElement):
    """A truss element that resists axial compressive loads.
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(StrutElement, self).__init__(key, connectivity, section, thermal)


class TieElement(TrussElement):
    """A truss element that resists axial tensile loads.
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(TieElement, self).__init__(key, connectivity, section, thermal)


# ==============================================================================
# 2D elements
# ==============================================================================

class ShellElement(Element):
    """A 2D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    connectivity : list
        List containing the nodes sequence building the shell element
    section : obj
        compas_fea2 ShellSection object
    thermal : bool
        NotImplemented
    """

    def __init__(self, connectivity, section, thermal=None):
        super(ShellElement, self).__init__(connectivity, section, thermal)


class MembraneElement(ShellElement):
    """A shell element that resists only axial loads.
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(MembraneElement, self).__init__(key, connectivity, section, thermal)


# ==============================================================================
# 3D elements
# ==============================================================================

class SolidElement(Element):
    """A 3D element that resists axial, shear, bending and torsion.
    """

    def __init__(self, connectivity, section, thermal=None):
        super(SolidElement, self).__init__(connectivity, section, thermal)


class TetrahedronElement(SolidElement):
    """A Solid element with 4 faces.
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(TetrahedronElement, self).__init__(key, connectivity, section, thermal)


class PentahedronElement(SolidElement):
    """A Solid element with 5 faces (extruded triangle).
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(PentahedronElement, self).__init__(key, connectivity, section, thermal)


class HexahedronElement(SolidElement):
    """A Solid cuboid element with 6 faces (extruded rectangle).
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(HexahedronElement, self).__init__(key, connectivity, section, thermal)
