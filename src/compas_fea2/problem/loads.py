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

    Notes
    -----
    Loads are registered to a :class:`compas_fea2.problem.Pattern`.

    """

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", **kwargs):
        super(Load, self).__init__(**kwargs)
        self.axes = axes
        self.x = x
        self.y = y
        self.z = z
        self.xx = xx
        self.yy = yy
        self.zz = zz

    @property
    def components(self):
        return {i: getattr(self, i) for i in ["x", "y", "z", "xx", "yy", "zz"]}

    @components.setter
    def components(self, value):
        for k, v in value:
            setattr(self, k, v)

    @property
    def pattern(self):
        return self._registration

    @property
    def step(self):
        return self.pattern._registration

    @property
    def problem(self):
        return self.step._registration

    @property
    def model(self):
        return self.problem._registration


class ConcentratedLoad(Load):
    """Concentrated forces and moments [units:N, Nm].

    Parameters
    ----------
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

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", **kwargs):
        super(ConcentratedLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, **kwargs)

    def __mul__(self, factor):
        if isinstance(factor, (float, int)):
            new_components = {k: (self.components[k] or 0) * factor for k in self.components}
            return ConcentratedLoad(**new_components, axes=self.axes)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, ConcentratedLoad):
            new_components = {k: (self.components[k] or 0) + (other.components[k] or 0) for k in self.components}
            return ConcentratedLoad(**new_components, axes=self.axes)
        else:
            raise NotImplementedError

    def __radd__(self, other):
        return self.__add__(other)


class PressureLoad(Load):
    """Distributed area force [e.g. units:N/m2] applied to element(s).

    Parameters
    ----------
    elements : str, list
        Elements set or elements the load is applied to.
    x : float
        x component of force / area.
    y : float
        y component of force / area.
    z : float
        z component of force / area.

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    elements : str, list
        Elements set or elements the load is applied to.
    x : float
        x component of force / area.
    y : float
        y component of force / area.
    z : float
        z component of force / area.
    """

    def __init__(self, x=0, y=0, z=0, axes="local", **kwargs):
        super(PressureLoad, self).__init__(components={"x": x, "y": y, "z": z}, axes=axes, **kwargs)
        raise NotImplementedError


class GravityLoad(Load):
    """Gravity load [units:N/m3] applied to element(s).

    Parameters
    ----------
    elements : str, list
        Element set or element keys the load is applied to.
    g : float
        Value of gravitational acceleration.
    x : float, optional
        Factor to apply to x direction, by default 0.
    y : float, optional
        Factor to apply to y direction, by default 0.
    z : float, optional
        Factor to apply to z direction, by default -1.

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

    Notes
    -----
    By default gravity is supposed to act along the negative `z` axis.

    """

    def __init__(self, g, x=0, y=0, z=-1, **kwargs):
        super(GravityLoad, self).__init__(x=x, y=y, z=z, axes="global", **kwargs)
        self._g = g

    @property
    def g(self):
        return self._g

    @property
    def vector(self):
        return [self.g * self.x, self.g * self.y, self.g * self.z]

    @property
    def components(self):
        components = {i: self.vector[j] for j, i in enumerate(["x", "y", "z"])}
        components.update({i: 0 for i in ["xx", "yy", "zz"]})
        return components

    def __mul__(self, factor):
        if isinstance(factor, (float, int)):
            new_components = {k: (getattr(self, k) or 0) * factor for k in ["x", "y", "z"]}
            return GravityLoad(self.g, **new_components)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)


class PrestressLoad(Load):
    """Prestress load"""

    def __init__(self, components, axes="global", **kwargs):
        super(TributaryLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError


class ThermalLoad(Load):
    """Thermal load"""

    def __init__(self, components, axes="global", **kwargs):
        super(ThermalLoad, self).__init__(components, axes, **kwargs)


class TributaryLoad(Load):
    """Tributary load"""

    def __init__(self, components, axes="global", **kwargs):
        super(TributaryLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError


class HarmonicPointLoad(Load):
    """"""

    def __init__(self, components, axes="global", **kwargs):
        super(HarmonicPointLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError


class HarmonicPressureLoad(Load):
    """"""

    def __init__(self, components, axes="global", **kwargs):
        super(HarmonicPressureLoad, self).__init__(components, axes, **kwargs)
        raise NotImplementedError
