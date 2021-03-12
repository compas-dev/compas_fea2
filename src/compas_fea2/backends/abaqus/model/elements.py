from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model import ElementBase
from compas_fea2.backends._base.model import MassElementBase
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

# ==============================================================================
# 0D elements
# ==============================================================================


class MassElement(MassElementBase):
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

    def __init__(self,  key, node, mass, elset):
        super(MassElement, self).__init__(key, node, mass, elset)

    # TODO: continue

    def _generate_data(self):
        line = ("*ELEMENT, TYPE=MASS, ELSET={}\n"
                "{}, {}\n"
                "*MASS, ELSET={0}\n"
                "{}\n").format(self.elset, self.node, )


# ==============================================================================
# 1D elements
# ==============================================================================

class BeamElement(BeamElementBase):

    def __init__(self, connectivity, section, orientation=[0.0, 0.0, -1.0], elset=None, thermal=None):
        super(BeamElement, self).__init__(connectivity, section, thermal)
        self.elset = elset
        self.eltype = 'B31'
        self.orientation = orientation

    def _generate_data(self):
        return '{0}, {1}, {2}\n'.format(self.key+1, self.connectivity[0]+1, self.connectivity[1]+1)


class SpringElement(SpringElementBase):
    """A 1D spring element.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(SpringElement, self).__init__()


class TrussElement(TrussElementBase):
    """A 1D element that resists axial loads.

    Parameters
    ----------
    None

    """

    def __init__(self, connectivity, section, elset=None, thermal=None):
        super(TrussElement, self).__init__(connectivity, section, thermal)

        self.elset = elset
        self.eltype = 'T3D2'
        self.orientation = None

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
    connectivity : list
        List containing the nodes sequence building the shell element.
    section : obj
        compas_fea2 ShellSection object
    elset : obj
        compas_fea2 Set object, optional
    thermal : bool
        NotImplemented,
    """

    def __init__(self, connectivity, section, elset=None, thermal=None):
        super(ShellElement, self).__init__(connectivity, section, thermal)
        if not elset:
            self.elset = self.section
        else:
            self.elset = elset

        if len(self.connectivity) == 3:
            self.eltype = 'S3'
        elif len(self.connectivity) == 4:
            self.eltype = 'S4'
        else:
            raise NotImplementedError

    def _generate_data(self):
        return '{0}, {1}\n'.format(self.key+1, ','.join(str(nk+1) for nk in self.connectivity))

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
    def __init__(self):
        super(MembraneElement, self).__init__()
        raise NotImplementedError

# ==============================================================================
# 3D elements
# ==============================================================================

class SolidElement(SolidElementBase):

    def __init__(self, connectivity, section, eltype=None, elset=None, thermal=None):
        super(SolidElement, self).__init__(connectivity, section, thermal)
        if not elset:
            self.elset = self.section
        else:
            self.elset = elset

        if not eltype:
            eltypes = {4: 'C3D4', 6: 'C3D6', 8: 'C3D8'}
            self.eltype = eltypes[len(self.connectivity)]
        else:
            self.eltype = eltype

    def _generate_data(self):
        return '{0}, {1}\n'.format(self.key+1, ','.join(str(nk+1) for nk in self.connectivity))


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
    from compas_fea2.backends.abaqus.model.nodes import Node
    from compas_fea2.backends.abaqus.model.materials import ElasticIsotropic
    from compas_fea2.backends.abaqus.model.sections import SolidSection
    from compas_fea2.backends.abaqus import SolidElement

    nodes = [Node([i, 3, 4]) for i in range(4)]
    mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)
    sec = SolidSection(name='section_A', material='mat_A')
    print(sec._generate_data())
    b = SolidElement(connectivity=nodes, section=sec)

    print(b)
    print(b._generate_data())
