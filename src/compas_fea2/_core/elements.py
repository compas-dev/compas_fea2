from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

# TODO add the property class here

__all__ = [
    'cNode',
    'cElement',
    'cMassElement',
    'cBeamElement',
    'cSpringElement',
    'cTrussElement',
    'cStrutElement',
    'cTieElement',
    'cShellElement',
    'cMembraneElement',
    'cFaceElement',
    'cSolidElement',
    'cPentahedronElement',
    'cTetrahedronElement',
    'cHexahedronElement',
]


# ==============================================================================
# General
# ==============================================================================

class cNode(object):

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

        self.__name__ = 'Node'
        self.key      = key
        self.x        = xyz[0]
        self.y        = xyz[1]
        self.z        = xyz[2]
        self.ex       = ex
        self.ey       = ey
        self.ez       = ez
        self.mass     = mass


    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['key', 'x', 'y', 'z', 'ex', 'ey', 'ez', 'mass']:
            print('{0:<5} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.key)


class cElement(object):

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

    def __init__(self, nodes=None, number=None, thermal=None, axes={}):

        self.__name__         = 'Element'
        self.nodes            = nodes
        self.number           = number
        self.thermal          = thermal
        self.axes             = axes
        self.element_property = None


    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['nodes', 'number', 'thermal', 'axes', 'element_property']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.number)


# ==============================================================================
# 0D elements
# ==============================================================================

class cMassElement(cElement):

    """ A 0D element for concentrated point mass.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cElement.__init__(self)

        self.__name__ = 'MassElement'


# ==============================================================================
# 1D elements
# ==============================================================================

class cBeamElement(cElement):

    """ A 1D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cElement.__init__(self)

        self.__name__ = 'BeamElement'


class cSpringElement(cElement):

    """ A 1D spring element.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cElement.__init__(self)

        self.__name__ = 'SpringElement'


class cTrussElement(cElement):

    """ A 1D element that resists axial loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cElement.__init__(self)

        self.__name__ = 'TrussElement'


class cStrutElement(cTrussElement):

    """ A truss element that resists axial compressive loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cTrussElement.__init__(self)

        self.__name__ = 'StrutElement'


class cTieElement(cTrussElement):

    """ A truss element that resists axial tensile loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cTrussElement.__init__(self)

        self.__name__ = 'TieElement'


# ==============================================================================
# 2D elements
# ==============================================================================

class cShellElement(cElement):

    """ A 2D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cElement.__init__(self)

        self.__name__ = 'ShellElement'


class cFaceElement(cElement):

    """ A 2D Face element used for special loading cases.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cElement.__init__(self)

        self.__name__ = 'FaceElement'


class cMembraneElement(cShellElement):

    """ A shell element that resists only axial loads.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cShellElement.__init__(self)

        self.__name__ = 'MembraneElement'


# ==============================================================================
# 3D elements
# ==============================================================================

class cSolidElement(cElement):

    """ A 3D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cElement.__init__(self)

        self.__name__ = 'SolidElement'


class cPentahedronElement(cSolidElement):

    """ A Solid element with 5 faces (extruded triangle).

    Parameters
    ----------
    None

    """

    def __init__(self):
        cSolidElement.__init__(self)

        self.__name__ = 'PentahedronElement'


class cTetrahedronElement(cSolidElement):

    """ A Solid element with 4 faces.

    Parameters
    ----------
    None

    """

    def __init__(self):
        cSolidElement.__init__(self)

        self.__name__ = 'TetrahedronElement'


class cHexahedronElement(cSolidElement):

    """ A Solid cuboid element with 6 faces (extruded rectangle).

    Parameters
    ----------
    None

    """

    def __init__(self):
        cSolidElement.__init__(self)

        self.__name__ = 'HexahedronElement'
