from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase

# TODO: make units independent using the utilities function


class Load(FEABase):
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
        for c, a in self._components.items():
            if a:
                setattr(self, '_'+c, a)

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


class PrestressLoad(Load):
    """Pre-stress [units: N/m2] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the PrestressLoad object.
    sxx : float,
        Value of prestress for axial stress component sxx.
    axes : str, optional
        Load applied via 'local' or 'global' axes, by default 'local'.

    """

    def __init__(self, name, elements, sxx=0, axes='local'):
        super(PrestressLoad).__init__(self, name=name, components={'sxx': sxx}, axes='local')


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
        super(PointLoad, self).__init__(name=name, components={'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}, axes=axes)


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

    def __init__(self, name, elements, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global'):
        super(LineLoad, self).__init__(name=name, components={'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}, axes=axes)


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

    def __init__(self, name, elements, x=0, y=0, z=0, axes='local'):
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


#  FIXME remove the nodes/elements from the loads below
class TributaryLoad(Load):
    """Tributary area loads applied to nodes.

    Parameters
    ----------
    structure : obj
        Structure class.
    name : str
        Name of the TributaryLoad object.
    mesh : str
        Tributary Mesh datastructure.
    x : float
        x component of area load.
    y : float
        y component of area load.
    z : float
        z component of area load.
    axes : str
        TributaryLoad applied via 'local' or 'global' axes.

    Note
    ----
    - The load components are loads per unit area [N/m2].
    - Currently only supports 'global' axis.

    """

    def __init__(self, structure, name, mesh, x=0, y=0, z=0, axes='global'):
        nodes = []
        components = {}
        for key in mesh.vertices():
            node = structure.check_node_exists(mesh.vertex_coordinates(key))
            if node is not None:
                A = mesh.vertex_area(key)
                nodes.append(node)
                components[node] = {'x': x * A, 'y': y * A, 'z': z * A}
        super(TributaryLoad, self).__init__(name=name, components=components, nodes=nodes, axes=axes)


class HarmonicPointLoad(Load):
    """Harmonic concentrated forces and moments [units:N, Nm] applied to node(s).

    Parameters
    ----------
    name : str
        Name of the HarmoniPointLoad object.
    nodes : str, list
        Node set or node keys the load is applied to.
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

    """

    def __init__(self, name, nodes, x=0, y=0, z=0, xx=0, yy=0, zz=0):
        components = {'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}
        super(HarmonicPointLoad, self).__init__(name=name, components=components, nodes=nodes, axes='global')


class HarmonicPressureLoad(Load):
    """Harmonic pressure loads [units:N/m2] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the HarmonicPressureLoad object.
    elements : str, list
        Elements set or element keys the load is applied to.
    pressure : float
        Normal acting pressure to be applied to the elements.
    phase : float
        Phase angle in radians.

    """

    def __init__(self, name, elements, pressure=0, phase=None):
        components = {'pressure': pressure, 'phase': phase}
        super(HarmonicPressureLoad, self).__init__(name=name, components=components, elements=elements, axes='global')


class AcousticDiffuseFieldLoad(Load):
    """Acoustic Diffuse field loads applied to elements.

    Parameters
    ----------
    name : str
        Name of the HarmonicPressureLoad object.
    elements : str, list
        Elements set or element keys the load is applied to.
    air_density : float
        Density of the acoustic fluid (defaults to air at 20 degrees).
    sound_speed : float
        Speed of sound (defaults to air at 20 degrees)
    max_inc_angle: float
        Maximum angle with the positive z axis for the randon incident plane waves

    """

    def __init__(self, name, elements, air_density=1.225, sound_speed=340, max_inc_angle=90):
        components = {'air_density': air_density, 'sound_speed': sound_speed, 'max_inc_angle': max_inc_angle}
        super(AcousticDiffuseFieldLoad, self).__init__(name=name, components=components, elements=elements, axes='global')
