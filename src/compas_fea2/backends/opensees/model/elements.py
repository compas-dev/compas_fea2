from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base.model import NodeBase
from compas_fea2.backends._base.model import ElementBase
from compas_fea2.backends._base.model import MassElementBase
from compas_fea2.backends._base.model import BeamElementBase
from compas_fea2.backends._base.model import SpringElementBase
from compas_fea2.backends._base.model import TrussElementBase
from compas_fea2.backends._base.model import StrutElementBase
from compas_fea2.backends._base.model import TieElementBase
from compas_fea2.backends._base.model import ShellElementBase
from compas_fea2.backends._base.model import MembraneElementBase
from compas_fea2.backends._base.model import FaceElementBase
from compas_fea2.backends._base.model import SolidElementBase
from compas_fea2.backends._base.model import PentahedronElementBase
from compas_fea2.backends._base.model import TetrahedronElementBase
from compas_fea2.backends._base.model import HexahedronElementBase


# Francesco Ranaudo (github.com/franaudo)

# TODO add the property class here

__all__ = [
    'Node',
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

class Node(NodeBase):
    """Initialises base Node object.

    Parameters
    ----------
    key : int
        Node key number.
    xyz : list
        [x, y, z] co-ordinates of the node.
    ex : list
        Node's local x axis.
    ey : list
        Node's local y axis.
    ez : list
        Node's local z axis.
    mass : float
        Mass in kg associated with the node.

    Attributes
    ----------
    key : int
        Node key number.
    x : float
        x co-ordinates of the node.
    y : float
        y co-ordinates of the node.
    z : float
        z co-ordinates of the node.
    ex : list
        Node's local x axis.
    ey : list
        Node's local y axis.
    ez : list
        Node's local z axis.
    mass : float
        Mass in kg associated with the node.

    """
    def __init__(self, key, xyz, ex, ey, ez, mass):
        super(Node, self).__init__(key, xyz, ex, ey, ez, mass)


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
    pass
    # def __init__(self, nodes, number, thermal, axes):
    #     super(Element, self).__init__(nodes, number, thermal, axes)


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

    """ A 2D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(ShellElement, self).__init__()


class FaceElement(FaceElementBase):

    """ A 2D Face element used for special loading cases.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(FaceElement, self).__init__()


class MembraneElement(MembraneElementBase):

    """ A shell element that resists only axial loads.

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

    """ A 3D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(SolidElement, self).__init__()


class PentahedronElement(PentahedronElementBase):

    """ A Solid element with 5 faces (extruded triangle).

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(PentahedronElement, self).__init__()


class TetrahedronElement(TetrahedronElementBase):

    """ A Solid element with 4 faces.

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(TetrahedronElement, self).__init__()


class HexahedronElement(HexahedronElementBase):

    """ A Solid cuboid element with 6 faces (extruded rectangle).

    Parameters
    ----------
    None

    """
    pass
    # def __init__(self):
    #     super(HexahedronElement, self).__init__()
