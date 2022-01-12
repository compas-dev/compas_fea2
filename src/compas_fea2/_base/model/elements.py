from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2._base.base import FEABase
# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'ElementBase',
    'MassElementBase',
    'BeamElementBase',
    'SpringElementBase',
    'TrussElementBase',
    'StrutElementBase',
    'TieElementBase',
    'ShellElementBase',
    'MembraneElementBase',
    # 'FaceElementBase',
    'SolidElementBase',
    'PentahedronElementBase',
    'TetrahedronElementBase',
    'HexahedronElementBase',
]


class ElementBase(FEABase):
    """Initialises a base Element object.

    Parameters
    ----------
    key : int
        Key number of the element.
    connectivity : list
        Ordered nodes keys the element connects to.
    section : Section Object
        Section Object assigned to the element.
    thermal : bool, optional
        Thermal properties on or off, by default None
    name : str, optional
        The name of the Element, by default the element key.

    Warnings
    --------
    The connectivity of the element must be provided in the correct order!
    """

    def __init__(self, connectivity, section, thermal=None, name=None):
        self.__name__ = 'Element'
        self._key = None
        self._name = str(self.key)
        self._connectivity = connectivity  # TODO add find node method to get the connectivity from the Node object
        self._connectivity_key = '_'.join(sorted([str(c) for c in self.connectivity]))
        self._connected_nodes = []
        self._section = section
        self._thermal = thermal
        self._axes = None

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.key)

    @property
    def name(self):
        """str : The name of the Element."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def key(self):
        """int : Key number of the element."""
        return self._key

    @property
    def connectivity(self):
        """list : list of nodes keys the element connects to."""
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
        """obj or str: compas_fea2 `Section` object or name of a Section previously
        added to the model."""
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


class MassElementBase():
    """A 0D element for concentrated point mass.

    Parameters
    ----------
    None
    """

    def __init__(self, key, node, mass, elset):
        self.__name__ = 'MassElement'
        self.key = key
        self.node = node
        self.mass = mass
        self.elset = elset
        # self.eltype = 'MASS'

    def __str__(self):
        print('\n')
        print('compas_fea2 {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))
        for attr in ['key', 'eltype', 'elset', 'mass']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))
        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.key)

# ==============================================================================
# 1D elements
# ==============================================================================


class BeamElementBase(ElementBase):
    """A 1D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None
    """

    def __init__(self, connectivity, section, thermal=None):
        super(BeamElementBase, self).__init__(connectivity, section, thermal)
        self.__name__ = 'BeamElement'
        # self.eltype = 'beam'


class SpringElementBase(ElementBase):
    """A 1D spring element.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(SpringElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'SpringElement'
        # self.eltype = 'spring'


class TrussElementBase(ElementBase):
    """A 1D element that resists axial loads.

    Parameters
    ----------
    None
    """

    def __init__(self, connectivity, section, thermal=None):
        super(TrussElementBase, self).__init__(connectivity, section, thermal)
        self.__name__ = 'TrussElement'

    def _checks(self):
        if self.section.__name__ in []:
            raise TypeError("The chosen section cannot be applied to Truss elements")


class StrutElementBase(TrussElementBase):
    """A truss element that resists axial compressive loads.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(StrutElementBase, self).__init__(key, connectivity, section, thermal)
        self.__name__ = 'StrutElement'
        # self.eltype = 'strut'


class TieElementBase(TrussElementBase):
    """A truss element that resists axial tensile loads.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(TieElementBase, self).__init__(key, connectivity, section, thermal)
        self.__name__ = 'TieElement'
        # self.eltype = 'tie'

# ==============================================================================
# 2D elements
# ==============================================================================


class ShellElementBase(ElementBase):
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
        super(ShellElementBase, self).__init__(connectivity, section, thermal)
        self.__name__ = 'ShellElement'
        # self.eltype = 'shell'

# class FaceElementBase(ElementBase):
#     """A 2D Face element used for special loading cases.

#     Parameters
#     ----------
#     None
#     """

#     def __init__(self,key, connectivity, section, thermal):
#         super(ElementBase, self).__init__(key, connectivity, section, thermal)
#         self.__name__ = 'FaceElement'
#         self.eltype = 'beam'


class MembraneElementBase(ShellElementBase):
    """A shell element that resists only axial loads.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(MembraneElementBase, self).__init__(key, connectivity, section, thermal)
        self.__name__ = 'MembraneElement'
        # self.eltype = 'membrane'

# ==============================================================================
# 3D elements
# ==============================================================================


class SolidElementBase(ElementBase):
    """A 3D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None
    """

    def __init__(self, connectivity, section, thermal=None):
        super(SolidElementBase, self).__init__(connectivity, section, thermal)
        self.__name__ = 'SolidElement'
        # self.eltype = 'solid'


class TetrahedronElementBase(SolidElementBase):
    """A Solid element with 4 faces.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(TetrahedronElementBase, self).__init__(key, connectivity, section, thermal)
        self.__name__ = 'TetrahedronElement'


class PentahedronElementBase(SolidElementBase):
    """A Solid element with 5 faces (extruded triangle).

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(PentahedronElementBase, self).__init__(key, connectivity, section, thermal)
        self.__name__ = 'PentahedronElement'
        # self.eltype = 'solid5'


class HexahedronElementBase(SolidElementBase):
    """A Solid cuboid element with 6 faces (extruded rectangle).

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(HexahedronElementBase, self).__init__(key, connectivity, section, thermal)
        self.__name__ = 'HexahedronElement'
        # self.eltype = 'solid6'


if __name__ == "__main__":
    my_element = BeamElementBase([0, 1], 'my_section')
    print(my_element)
