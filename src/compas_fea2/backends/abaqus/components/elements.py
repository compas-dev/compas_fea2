from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._core import NodeBase
from compas_fea2.backends._core import ElementBase
from compas_fea2.backends._core import MassElementBase
from compas_fea2.backends._core import BeamElementBase
from compas_fea2.backends._core import SpringElementBase
from compas_fea2.backends._core import TrussElementBase
from compas_fea2.backends._core import StrutElementBase
from compas_fea2.backends._core import TieElementBase
from compas_fea2.backends._core import ShellElementBase
from compas_fea2.backends._core import MembraneElementBase
from compas_fea2.backends._core import FaceElementBase
from compas_fea2.backends._core import SolidElementBase
from compas_fea2.backends._core import PentahedronElementBase
from compas_fea2.backends._core import TetrahedronElementBase
from compas_fea2.backends._core import HexahedronElementBase


# Francesco Ranaudo (github.com/franaudo)

# TODO add the property class here

__all__ = [
    'Element',
    'MassElement',
    'BeamElement',
    'SpringElement',
    'TrussElement',
    'StrutElement',
    'TieElement',
    'ShellElement',
    'MembraneElement',
    'FaceElement',
    'SolidElement',
    'PentahedronElement',
    'TetrahedronElement',
    'HexahedronElement',
]


# ==============================================================================
# General
# ==============================================================================

class Element(ElementBase):
    """Initialises base Element object.

    Parameters
    ----------
    nodes : list
        Node keys the element connects to.
    number : int
        Number of the element.
    thermal : bool
        Thermal properties on or off.
    axes : dict
        The local element axes.

    Attributes
    ----------
    nodes : list
        Node keys the element connects to.
    number : int
        Number of the element.
    thermal : bool
        Thermal properties on or off.
    axes : dict
        The local element axes.
    element_property : str
        Element property name

    """
    def __init__(self, key, eltype, nodes_keys, section, elset=None, thermal=None, axes={}):
        super(Element, self).__init__(key, eltype, nodes_keys, section, thermal=None, axes={})
        if not elset:
            self.elset        = self.section.name
        else:
            self.elset        = elset


# ==============================================================================
# 0D elements
# ==============================================================================

class MassElement(MassElementBase):
    """A 0D element for concentrated point mass.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(MassElement, self).__init__()


# ==============================================================================
# 1D elements
# ==============================================================================

class BeamElement(BeamElementBase):
    """A 1D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(BeamElement, self).__init__()


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
    pass
    # def __init__(self):
    #     super(TrussElement, self).__init__()


class StrutElement(StrutElementBase):
    """A truss element that resists axial compressive loads.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(StrutElement, self).__init__()


class TieElement(TieElementBase):
    """A truss element that resists axial tensile loads.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(TieElement, self).__init__()


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


class FaceElement(FaceElementBase):
    """A 2D Face element used for special loading cases.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(FaceElement, self).__init__()


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
    """A 3D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """
    def __init__(self):
        super(SolidElement, self).__init__()

    def write_keyword(self, f):
        etypes = {4: 'C3D4', 6: 'C3D6', 8: 'C3D8'}
        line = "*Element, type={}, elset={}".format(etypes[len(self.nodes)], self.elset)

        f.write(line)

    def write_data(self, f):
        prefix  = ''
        spacer  = self.spacer
        x, y, z = self.xyz
        nkeys   = [str(i + 1) for i in self.nodes_keys]

        line    = '{0}, {1}'.format(self.key, ','.join(nkeys))

        f.write(line)



class PentahedronElement(PentahedronElementBase):
    """A Solid element with 5 faces (extruded triangle).

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(PentahedronElement, self).__init__()


class TetrahedronElement(TetrahedronElementBase):
    """A Solid element with 4 faces.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(TetrahedronElement, self).__init__()


class HexahedronElement(HexahedronElementBase):
    """A Solid cuboid element with 6 faces (extruded rectangle).

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(HexahedronElement, self).__init__()
