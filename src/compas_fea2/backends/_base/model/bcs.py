from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'GeneralBCBase',
    'FixedBCBase',
    'PinnedBCBase',
    'FixedBCXXBase',
    'FixedBCYYBase',
    'FixedBCZZBase',
    'RollerBCXBase',
    'RollerBCYBase',
    'RollerBCZBase',
    'RollerBCXYBase',
    'RollerBCYZBase',
    'RollerBCXZBase'
]


class GeneralBCBase(FEABase):
    """Initialises the base GeneralBC object.

    Parameters
    ----------
    name : str
        Name of the BC object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to. #TODO change
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
    """

    def __init__(self, name, nodes, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        self.__name__ = 'GeneralBC'
        self._name = name
        self._nodes = nodes
        self._x = x
        self._y = y
        self._z = z
        self._xx = xx
        self._yy = yy
        self._zz = zz

        self._components = {a: getattr(self, '_'+a) for a in ['x', 'y', 'z', 'xx', 'yy', 'zz']}
        self._axes = axes

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    @property
    def name(self):
        """str :  Name of the BC object."""
        return self._name

    @property
    def nodes(self):
        """str, list : Node set string or nodes list the displacement is applied to."""
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @property
    def x(self):
        """float : Value of x translation."""
        return self._x

    @property
    def y(self):
        """float : Value of y translation.."""
        return self._y

    @property
    def z(self):
        """float : Value of z translation."""
        return self._z

    @property
    def xx(self):
        """float : Value of xx rotation."""
        return self._xx

    @property
    def yy(self):
        """float : Value of yy rotation."""
        return self._yy

    @property
    def zz(self):
        """float : Value of zz rotation."""
        return self._zz

    @property
    def components(self):
        """dict : Values of x, y, z, xx, yy, zz degrees-of-freedom."""
        return self._components

    @property
    def axes(self):
        """str : 'local' or 'global' coordinate axes."""
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value

    def _set_component_attribute(self):
        """set the components attribute from the components dictionary
        """
        for c, a in self.components:
            setattr(self, c, a)


class FixedBCBase(GeneralBCBase):
    """A fixed nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the FixedBC object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    """

    def __init__(self, name, nodes, axes='global'):
        super(FixedBCBase, self).__init__(name=name, nodes=nodes, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes=axes)
        self.__name__ = 'FixedBC'


class PinnedBCBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the PinnedBC object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    """

    def __init__(self, name, nodes, axes='global'):
        super(PinnedBCBase, self).__init__(name=name, nodes=nodes, x=0, y=0, z=0, axes=axes)
        self.__name__ = 'PinnedBC'


class FixedBCXXBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition clamped in XX.

    Parameters
    ----------
    name : str
        Name of the FixedBCXX object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(FixedBCXXBase, self).__init__(name=name, nodes=nodes, x=0, y=0, z=0, xx=0, axes=axes)
        self.__name__ = 'FixedBCXX'


class FixedBCYYBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition clamped in YY.

    Parameters
    ----------
    name : str
        Name of the FixedBCYY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(FixedBCYYBase, self).__init__(name=name, nodes=nodes, x=0, y=0, z=0, yy=0, axes=axes)
        self.__name__ = 'FixedBCYY'


class FixedBCZZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition clamped in ZZ.

    Parameters
    ----------
    name : str
        Name of the FixedBCZZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(FixedBCZZBase, self).__init__(name=name, nodes=nodes, x=0, y=0, z=0, zz=0, axes=axes)
        self.__name__ = 'FixedBCZZ'


class RollerBCXBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in X.

    Parameters
    ----------
    name : str
        Name of the RollerBCX object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(RollerBCXBase, self).__init__(name=name, nodes=nodes, y=0, z=0, axes=axes)
        self.__name__ = 'RollerBCX'


class RollerBCYBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in Y.

    Parameters
    ----------
    name : str
        Name of the RollerBCY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(RollerBCYBase, self).__init__(name=name, nodes=nodes, x=0, z=0, zz=0, axes=axes)
        self.__name__ = 'RollerBCY'


class RollerBCZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in Z.

    Parameters
    ----------
    name : str
        Name of the RollerBCZ object.
    nodes : str
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(RollerBCZBase, self).__init__(name=name, nodes=nodes, x=0, y=0, axes=axes)
        self.__name__ = 'RollerBCZ'


class RollerBCXYBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in X and Y.

    Parameters
    ----------
    name : str
        Name of the RollerBCXY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(RollerBCXYBase, self).__init__(name=name, nodes=nodes, z=0, axes=axes)

        self.__name__ = 'RollerBCXY'


class RollerBCYZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in Y and Z.

    Parameters
    ----------
    name : str
        Name of the RollerBCYZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(RollerBCYZBase, self).__init__(name=name, nodes=nodes, x=0, axes=axes)
        self.__name__ = 'RollerBCYZ'


class RollerBCXZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in X and Z.

    Parameters
    ----------
    name : str
        Name of the RollerBCXZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.
    """

    def __init__(self, name, nodes, axes='global'):
        super(RollerBCXZBase, self).__init__(name=name, nodes=nodes, z=0, axes=axes)
        self.__name__ = 'RollerBCXZ'
