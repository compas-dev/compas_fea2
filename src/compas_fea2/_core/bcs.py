
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'cGeneralDisplacement',
    'cFixedDisplacement',
    'cPinnedDisplacement',
    'cFixedDisplacementXX',
    'cFixedDisplacementYY',
    'cFixedDisplacementZZ',
    'cRollerDisplacementX',
    'cRollerDisplacementY',
    'cRollerDisplacementZ',
    'cRollerDisplacementXY',
    'cRollerDisplacementYZ',
    'cRollerDisplacementXZ'
]


class cGeneralDisplacement(object):

    """ Initialises the base GeneralDisplacement object.

    Parameters
    ----------
    name : str
        Name of the Displacement object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    x : float
        Value of x translation.
    y : float
        Value of y translation.
    z : float
        Value of z translation.
    xx : float
        Value of xx rotation.
    yy : float
        Value of yy rotation.
    zz : float
        Value of zz rotation.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    nodes : str
        Node set string or nodes list the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.

    """

    def __init__(self, name, nodes, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):

        self.__name__   = 'GeneralDisplacement'
        self.name       = name
        self.nodes      = nodes
        self.components = {'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}
        self.axes       = axes


    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['name', 'nodes', 'components', 'axes']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


class cFixedDisplacement(cGeneralDisplacement):

    """ A fixed nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacement object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.

    """

    def __init__(self, name, nodes, axes='global'):
        cGeneralDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__   = 'FixedDisplacement'
        self.components = {'x': 0, 'y': 0, 'z': 0, 'xx': 0, 'yy': 0, 'zz': 0}


class cPinnedDisplacement(cGeneralDisplacement):

    """ A pinned nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the PinnedDisplacement object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.

    """

    def __init__(self, name, nodes, axes='global'):
        cGeneralDisplacement.__init__(self, name=name, nodes=nodes, x=0, y=0, z=0, axes=axes)

        self.__name__ = 'PinnedDisplacement'


class cFixedDisplacementXX(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition clamped in XX.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacementXX object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'FixedDisplacementXX'
        self.components['xx'] = 0


class cFixedDisplacementYY(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition clamped in YY.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacementYY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'FixedDisplacementYY'
        self.components['yy'] = 0


class cFixedDisplacementZZ(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition clamped in ZZ.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacementZZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'FixedDisplacementZZ'
        self.components['zz'] = 0


class cRollerDisplacementX(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition released in X.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementX object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'RollerDisplacementX'
        self.components['x'] = None


class cRollerDisplacementY(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition released in Y.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'RollerDisplacementY'
        self.components['y'] = None


class cRollerDisplacementZ(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition released in Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementZ object.
    nodes : str
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'RollerDisplacementZ'
        self.components['z'] = None


class cRollerDisplacementXY(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition released in X and Y.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'RollerDisplacementXY'
        self.components['x'] = None
        self.components['y'] = None


class cRollerDisplacementYZ(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition released in Y and Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementYZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'RollerDisplacementYZ'
        self.components['y'] = None
        self.components['z'] = None


class cRollerDisplacementXZ(cPinnedDisplacement):

    """ A pinned nodal displacement boundary condition released in X and Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """

    def __init__(self, name, nodes, axes='global'):
        cPinnedDisplacement.__init__(self, name=name, nodes=nodes, axes=axes)

        self.__name__ = 'RollerDisplacementXZ'
        self.components['x'] = None
        self.components['z'] = None
