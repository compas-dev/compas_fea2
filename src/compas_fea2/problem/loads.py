from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

# TODO: make units independent using the utilities function


class Load(FEAData):
    """Initialises base Load object.

    Parameters
    ----------
    name : str
        Name of the Load object.
    components : dict
        Load components.
    axes : str, optional
        Load applied via 'local' or 'global' axes, by default 'global'.
    """

    def __init__(self, name, components, axes='global'):
        super(Load, self).__init__(name=name)
        self._axes = axes
        self._components = components
        for component, attr in self._components.items():
            if attr:
                setattr(self, '_'+component, attr)

    @property
    def axes(self):
        """str : Load applied via 'local' or 'global' axes."""
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value

    @property
    def components(self):
        """dict : Load components. These differ according to each Load type"""
        return self._components


class PointLoad(Load):
    """Concentrated forces and moments [units:N, Nm] applied to node(s).

    Parameters
    ----------
    name : str
        Name of the PointLoad object.
    nodes : int or list(int), obj
        It can be either a key or a list of keys, or a NodesGroup of the nodes where the load is
        apllied.
    x : float
        x component of force.
    y : float
        y component of force.
    z : float
        z component of force.
    xx : float
        xx component of moment.
    yy : float
        yy component of moment.
    zz : float
        zz component of moment.
    axes : str
        Load applied via 'local' or 'global' axes.

    """

    def __init__(self, name, x, y, z, xx, yy, zz, axes):
        super(PointLoad, self).__init__(name=name, components={
            'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}, axes=axes)


class LineLoad(Load):
    """Distributed line forces and moments [units:N/m or Nm/m] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the LineLoad object.
    nodes : int or list(int), obj
        It can be either a key or a list of keys, or a ElementsGroup of the elements
        where the load is apllied.
    x : float
        x component of force / length.
    y : float
        y component of force / length.
    z : float
        z component of force / length.
    xx : float
        xx component of moment / length.
    yy : float
        yy component of moment / length.
    zz : float
        zz component of moment / length.
    axes : str, optional
        Load applied via 'local' or 'global' axes, by default 'global'.

    """

    def __init__(self, name, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global'):
        super(LineLoad, self).__init__(name=name, components={
            'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}, axes=axes)


class AreaLoad(Load):
    """Distributed area force [e.g. units:N/m2] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the AreaLoad object.
    elements : str, list
        Elements set or elements the load is applied to.
    x : float
        x component of area load.
    y : float
        y component of area load.
    z : float
        z component of area load.

    """

    def __init__(self, name, x=0, y=0, z=0, axes='local'):
        super(AreaLoad, self).__init__(name=name, components={'x': x, 'y': y, 'z': z}, axes=axes)


class GravityLoad(Load):
    """Gravity load [units:N/m3] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the GravityLoad object.
    elements : str, list
        Element set or element keys the load is applied to.
    g : float
        Value of gravitational acceleration.
    x : float
        Factor to apply to x direction.
    y : float
        Factor to apply to y direction.
    z : float
        Factor to apply to z direction.

    """

    def __init__(self, name, g, x, y, z):
        super(GravityLoad, self).__init__(components={'x': x, 'y': y, 'z': z}, name=name, axes='global')
        self._g = g

    @property
    def g(self):
        """The g property."""
        return self._g
