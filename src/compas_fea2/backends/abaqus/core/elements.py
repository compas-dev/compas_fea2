from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2._core import cNode
from compas_fea2._core import cElement
from compas_fea2._core import cMassElement
from compas_fea2._core import cBeamElement
from compas_fea2._core import cSpringElement
from compas_fea2._core import cTrussElement
from compas_fea2._core import cStrutElement
from compas_fea2._core import cTieElement
from compas_fea2._core import cShellElement
from compas_fea2._core import cMembraneElement
from compas_fea2._core import cFaceElement
from compas_fea2._core import cSolidElement
from compas_fea2._core import cPentahedronElement
from compas_fea2._core import cTetrahedronElement
from compas_fea2._core import cHexahedronElement


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

class Node(cNode):

    """ Initialises base Node object.

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


class Element(cElement):

    """ Initialises base Element object.

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

    def __init__(self, nodes, number, thermal, axes):
        super(Element, self).__init__(nodes, number, thermal, axes)


# ==============================================================================
# 0D elements
# ==============================================================================

class MassElement(cMassElement):

    """ A 0D element for concentrated point mass.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(MassElement, self).__init__()


# ==============================================================================
# 1D elements
# ==============================================================================

class BeamElement(cBeamElement):

    """ A 1D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(BeamElement, self).__init__()


class SpringElement(cSpringElement):

    """ A 1D spring element.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(SpringElement, self).__init__()


class TrussElement(cTrussElement):

    """ A 1D element that resists axial loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(TrussElement, self).__init__()


class StrutElement(cStrutElement):

    """ A truss element that resists axial compressive loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(StrutElement, self).__init__()


class TieElement(cTieElement):

    """ A truss element that resists axial tensile loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(TieElement, self).__init__()


# ==============================================================================
# 2D elements
# ==============================================================================

class ShellElement(cShellElement):

    """ A 2D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(ShellElement, self).__init__()


class FaceElement(cFaceElement):

    """ A 2D Face element used for special loading cases.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(FaceElement, self).__init__()


class MembraneElement(cMembraneElement):

    """ A shell element that resists only axial loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(MembraneElement, self).__init__()


# ==============================================================================
# 3D elements
# ==============================================================================

class SolidElement(cSolidElement):

    """ A 3D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(SolidElement, self).__init__()


class PentahedronElement(cPentahedronElement):

    """ A Solid element with 5 faces (extruded triangle).

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(PentahedronElement, self).__init__()


class TetrahedronElement(cTetrahedronElement):

    """ A Solid element with 4 faces.

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(TetrahedronElement, self).__init__()


class HexahedronElement(cHexahedronElement):

    """ A Solid cuboid element with 6 faces (extruded rectangle).

    Parameters
    ----------
    None

    """

    def __init__(self):
        super(HexahedronElement, self).__init__()
