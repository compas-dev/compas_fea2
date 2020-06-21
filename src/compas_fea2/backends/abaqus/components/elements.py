from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._core import NodeBase
from compas_fea2.backends._core import ElementBase
from compas_fea2.backends._core import BeamElementBase
from compas_fea2.backends._core import SpringElementBase
from compas_fea2.backends._core import TrussElementBase
from compas_fea2.backends._core import StrutElementBase
from compas_fea2.backends._core import TieElementBase
from compas_fea2.backends._core import ShellElementBase
from compas_fea2.backends._core import MembraneElementBase
# from compas_fea2.backends._core import FaceElementBase
from compas_fea2.backends._core import SolidElementBase
# from compas_fea2.backends._core import PentahedronElementBase
# from compas_fea2.backends._core import TetrahedronElementBase
# from compas_fea2.backends._core import HexahedronElementBase


# Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'MassElement',
    'BeamElement',
    # 'SpringElement',
    'TrussElement',
    # 'StrutElement',
    # 'TieElement',
    'ShellElement',
    'MembraneElement',
    # 'FaceElement',
    'SolidElement',
    # 'PentahedronElement',
    # 'TetrahedronElement',
    # 'HexahedronElement',
    ]

def _write_elemnts_keyword(obj, f):
    line = "*Element, type={}, elset={}\n".format(obj.eltype, obj.elset)
    f.write(line)


# ==============================================================================
# 0D elements
# ==============================================================================

class MassElement():
    """A 0D element for concentrated point mass.

    Attributes
    ----------
    key : int
        Number of the element.
    elset : str
        Name of the automatically generated element set where the masses is applied.
    mass : float
        Concentrated mass (mass of each point of the set).
    """

    def __init__(self, key, elset, mass):
        self.__name__         = 'Element'
        self.key              = key
        self.elset            = elset
        self.eltype            = 'MASS'


    def __str__(self):
        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))
        for attr in ['key','eltype', 'elset', 'mass']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))
        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.key)


# ==============================================================================
# 1D elements
# ==============================================================================

class BeamElement(BeamElementBase):
    """A 1D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self, key, connectivity, section, elset=None, thermal=None):
        super(BeamElement, self).__init__(key, connectivity, section, thermal=None)
        if not elset:
            self.elset = self.section.name
        else:
            self.elset = elset
        self.eltype = 'B31'

    def write_keyword(self, f):
        _write_elemnts_keyword(self, f)

    def write_data(self, f):
        f.write('{0}, {1},{2}\n'.format(self.key, self.connectivity[0], self.connectivity[1]))


# class SpringElement(SpringElementBase):
#     """A 1D spring element.

#     Parameters
#     ----------
#     None

#     """
#     pass
#     # def __init__(self):
#     #     super(SpringElement, self).__init__()


class TrussElement(TrussElementBase):
    """A 1D element that resists axial loads.

    Parameters
    ----------
    None

    """
    def __init__(self, key, connectivity, section, elset=None, thermal=None):
        super(TrussElement, self).__init__(key, connectivity, section, thermal=None)
        if not elset:
            self.elset = self.section.name
        else:
            self.elset = elset
        self.eltype = 'T3D2'


# class StrutElement(StrutElementBase):
#     """A truss element that resists axial compressive loads.

#     Parameters
#     ----------
#     None

#     """
#     pass
#     # def __init__(self):
#     #     super(StrutElement, self).__init__()


# class TieElement(TieElementBase):
#     """A truss element that resists axial tensile loads.

#     Parameters
#     ----------
#     None

#     """
#     pass
#     # def __init__(self):
#     #     super(TieElement, self).__init__()


# ==============================================================================
# 2D elements
# ==============================================================================

class ShellElement(ShellElementBase):
    """A 2D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(ShellElement, self).__init__()
    def __init__(self, key, connectivity, section, elset=None, thermal=None):
        super(TrussElement, self).__init__(key, connectivity, section, thermal=None)
        if not elset:
            self.elset = self.section.name
        else:
            self.elset = elset

        if len(self.connectivity) == 3:
            self.eltype = 'S3'
        elif len(self.connectivity) == 4:
            self.eltype = 'S4'
        else:
            NotImplemented


# class FaceElement(FaceElementBase):
#     """A 2D Face element used for special loading cases.

#     Parameters
#     ----------
#     None

#     """
#     pass
#     # def __init__(self):
#     #     super(FaceElement, self).__init__()


class MembraneElement(MembraneElementBase):
    """A shell element that resists only axial loads.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(MembraneElement, self).__init__()


# ==============================================================================
# 3D elements
# ==============================================================================

class SolidElement(SolidElementBase):

    def __init__(self, key, connectivity, section, eltype=None, elset=None, thermal=None):
        super(SolidElement, self).__init__(key, connectivity, section, thermal=None)
        if not elset:
            self.elset = self.section.name
        else:
            self.elset = elset

        if not eltype:
            eltypes = {4: 'C3D4', 6: 'C3D6', 8: 'C3D8'}
            self.eltype = eltypes[len(self.connectivity)]
        else:
            self.eltype = eltype

    def write_keyword(self, f):
        _write_elemnts_keyword(self, f)

    def write_data(self, f):
        nkeys = []
        for n in self.connectivity:
            nkeys.append(str(n.key))
        line    = '{0}, {1}\n'.format(self.key, ','.join(nkeys))
        f.write(line)



# class PentahedronElement(PentahedronElementBase):
#     """A Solid element with 5 faces (extruded triangle).

#     Parameters
#     ----------
#     None

#     """
#     pass
#     # def __init__(self):
#     #     super(PentahedronElement, self).__init__()


# class TetrahedronElement(TetrahedronElementBase):
#     """A Solid element with 4 faces.

#     Parameters
#     ----------
#     None

#     """
#     pass
#     # def __init__(self):
#     #     super(TetrahedronElement, self).__init__()


# class HexahedronElement(HexahedronElementBase):
#     """A Solid cuboid element with 6 faces (extruded rectangle).

#     Parameters
#     ----------
#     None

#     """
#     pass
#     # def __init__(self):
#     #     super(HexahedronElement, self).__init__()
