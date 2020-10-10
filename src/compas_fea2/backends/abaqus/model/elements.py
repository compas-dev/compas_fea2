from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model import ElementBase
from compas_fea2.backends._base.model import BeamElementBase
from compas_fea2.backends._base.model import SpringElementBase
from compas_fea2.backends._base.model import TrussElementBase
from compas_fea2.backends._base.model import StrutElementBase
from compas_fea2.backends._base.model import TieElementBase
from compas_fea2.backends._base.model import ShellElementBase
from compas_fea2.backends._base.model import MembraneElementBase
# from compas_fea2.backends._base.model import FaceElementBase
from compas_fea2.backends._base.model import SolidElementBase
# from compas_fea2.backends._base.model import PentahedronElementBase
# from compas_fea2.backends._base.model import TetrahedronElementBase
# from compas_fea2.backends._base.model import HexahedronElementBase


# Author(s): Francesco Ranaudo (github.com/franaudo)

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

# # TODO the key should not be assigned by the user but generated automatically

# def _generate_keyword(obj):
#     return "*Element, type={}, elset={}\n".format(obj.eltype, obj.elset)


# ==============================================================================
# 0D elements
# ==============================================================================

class MassElement():
    """A 0D element for concentrated point mass.

    Parameters
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

    def __init__(self, connectivity, section, orientation=[0.0, 0.0, -1.0], elset=None, thermal=None):
        super(BeamElement, self).__init__(connectivity=connectivity, section=section, thermal=thermal)
        self.elset = elset
        self.eltype = 'B31'
        self.orientation = orientation
        # self.keyword = _generate_keyword(self)
        # self.data    = '{0}, {1}, {2}\n'.format(self.key, self.connectivity[0].key, self.connectivity[1].key)

    def _generate_data(self):
        return '{0}, {1}, {2}\n'.format(self.key+1, self.connectivity[0]+1, self.connectivity[1]+1)

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
    def __init__(self, connectivity, section, elset=None, thermal=None):
        super(TrussElement, self).__init__(connectivity, section, thermal=None)

        self.elset = elset
        self.eltype = 'T3D2'
        self.orientation = None
        # self.keyword = _generate_keyword(self)

    def _generate_data(self):
        return '{0}, {1}, {2}\n'.format(self.key+1, self.connectivity[0]+1, self.connectivity[1]+1)

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
            raise NotImplementedError


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
    NotImplemented
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

        # self.keyword = _generate_keyword(self)
        self.data    = self._generate_data()

    def _generate_data(self):
        nkeys = []
        for n in self.connectivity:
            nkeys.append(str(n.key))
        return '{0}, {1}\n'.format(self.key+1, ','.join(nkeys))



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

if __name__ == "__main__":
    from compas_fea2.backends.abaqus import Node
    from compas_fea2.backends.abaqus import BeamElement

    n = Node(1,[2,3,4])
    b = BeamElement(1, [n,n], 's')
