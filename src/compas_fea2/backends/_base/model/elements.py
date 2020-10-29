from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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


class ElementBase(object):
    """Initialises a base Element object.

    Parameters
    ----------
    key : int
        Key number of the element.
    connectivity : list
        Ordered nodes keys the element connects to.
    section : Section Object
        Section Object assigned to the element.
    thermal : bool
        Thermal properties on or off.

    Attributes
    ----------
    axes : dict
        The local element axes.
    etype : str
        Element type identifier. Each software has a different way of identifying the elements.
    """

    def __init__(self, connectivity, section, thermal=None):
        self.__name__ = 'Element'
        self.key = 0
        self.connectivity = connectivity
        self.connectivity_key = '_'.join(
            sorted([str(c) for c in self.connectivity]))
        self.section = section
        self.thermal = thermal
        self.etype = None
        self.axes = None

    def __str__(self):

        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        data = []
        for attr in ['key', 'etype', 'connectivity']:
            data.append('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(data))

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.key)

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
        self.eltype = 'MASS'

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
        self.etype = 'beam'


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
        self.etype = 'spring'


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
            raise TypeError(
                "The chosen section cannot be applied to Truss elements")


class StrutElementBase(TrussElementBase):
    """A truss element that resists axial compressive loads.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(StrutElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'StrutElement'
        self.etype = 'strut'


class TieElementBase(TrussElementBase):
    """A truss element that resists axial tensile loads.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(TieElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'TieElement'
        self.etype = 'tie'

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
        self.etype = 'shell'

# class FaceElementBase(ElementBase):
#     """A 2D Face element used for special loading cases.

#     Parameters
#     ----------
#     None
#     """

#     def __init__(self,key, connectivity, section, thermal):
#         super(ElementBase, self).__init__(key, connectivity, section, thermal)
#         self.__name__ = 'FaceElement'
#         self.etype = 'beam'


class MembraneElementBase(ShellElementBase):
    """A shell element that resists only axial loads.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(MembraneElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'MembraneElement'
        self.etype = 'membrane'

# ==============================================================================
# 3D elements
# ==============================================================================


class SolidElementBase(ElementBase):
    """A 3D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(SolidElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'SolidElement'
        self.etype = 'solid'


class TetrahedronElementBase(SolidElementBase):
    """A Solid element with 4 faces.

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(TetrahedronElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'TetrahedronElement'
        self.etype = 'solid4'


class PentahedronElementBase(SolidElementBase):
    """A Solid element with 5 faces (extruded triangle).

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(PentahedronElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'PentahedronElement'
        self.etype = 'solid5'


class HexahedronElementBase(SolidElementBase):
    """A Solid cuboid element with 6 faces (extruded rectangle).

    Parameters
    ----------
    None
    """

    def __init__(self, key, connectivity, section, thermal=None):
        super(HexahedronElementBase, self).__init__(
            key, connectivity, section, thermal)
        self.__name__ = 'HexahedronElement'
        self.etype = 'solid6'


if __name__ == "__main__":
    my_element = BeamElementBase(1, [0, 1], 'my_section')
    print(my_element)
