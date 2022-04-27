from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

# TODO: make units independent using the utilities function


class _Load(FEAData):
    """Initialises base Load object.

    Parameters
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    components : dict
        Load components.
    axes : str, optional
        Load applied via 'local' or 'global' axes, by default 'global'.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    components : dict
        Load components. These differ according to each Load type
    axes : str, optional
        Load applied via 'local' or 'global' axes, by default 'global'.
    """

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(_Load, self).__init__(name=name, **kwargs)
        self._axes = axes
        self._components = components
        for component, attr in self._components.items():
            if attr:
                setattr(self, '_'+component, attr)

    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value

    @property
    def components(self):
        return self._components


class PointLoad(_Load):
    """Concentrated forces and moments [units:N, Nm] applied to node(s).

    Parameters
    ----------
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

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
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

    def __init__(self, x, y, z, xx, yy, zz, axes, name=None, **kwargs):
        super(PointLoad, self).__init__(components={
            'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}, axes=axes, name=name, **kwargs)


class LineLoad(_Load):
    """Distributed line forces and moments [units:N/m or Nm/m] applied to element(s).

    Parameters
    ----------
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

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
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

    def __init__(self, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global', name=None, **kwargs):
        super(LineLoad, self).__init__(components={
            'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}, axes=axes, name=name, **kwargs)


class AreaLoad(_Load):
    """Distributed area force [e.g. units:N/m2] applied to element(s).

    Parameters
    ----------
    elements : str, list
        Elements set or elements the load is applied to.
    x : float
        x component of area load.
    y : float
        y component of area load.
    z : float
        z component of area load.

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    elements : str, list
        Elements set or elements the load is applied to.
    x : float
        x component of area load.
    y : float
        y component of area load.
    z : float
        z component of area load.
    """

    def __init__(self, x=0, y=0, z=0, axes='local', name=None, **kwargs):
        super(AreaLoad, self).__init__(components={'x': x, 'y': y, 'z': z}, axes=axes, name=name, **kwargs)


class GravityLoad(_Load):
    """Gravity load [units:N/m3] applied to element(s).

    Parameters
    ----------
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

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
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

    def __init__(self, g, x, y, z, name=None, **kwargs):
        super(GravityLoad, self).__init__(components={'x': x, 'y': y, 'z': z}, axes='global', name=name, **kwargs)
        self._g = g

    @property
    def g(self):
        return self._g


class PrestressLoad(_Load):
    """Prestress load"""

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(TributaryLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class TributaryLoad(_Load):
    """Tributary load"""

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(TributaryLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class HarmonicPointLoad(_Load):
    """"""

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(HarmonicPointLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class HarmonicPressureLoad(_Load):
    """"""

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(HarmonicPressureLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError