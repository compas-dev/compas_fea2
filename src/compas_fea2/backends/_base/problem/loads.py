from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase

# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez),
#            Francesco Ranaudo (github.com/franaudo)

# TODO: make units independent using the utilities function


__all__ = [
    'LoadBase',
    'PrestressLoadBase',
    'PointLoadBase',
    # 'PointLoadsBase',
    'LineLoadBase',
    'AreaLoadBase',
    'GravityLoadBase',
    # 'ThermalLoadBase',
    'TributaryLoadBase',
    'HarmonicPointLoadBase',
    'HarmonicPressureLoadBase',
    'AcousticDiffuseFieldLoadBase'
]


class LoadBase(FEABase):
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
        self.__name__ = 'LoadObject'
        self._name = name
        self._axes = axes
        self._components = components
        for c, a in self._components.items():
            setattr(self, '_'+c, a)
        # self._x = None
        # self._y = None
        # self._z = None
        # self._xx = None
        # self._yy = None
        # self._zz = None

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    @property
    def name(self):
        """str : Name of the Load object."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

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

    # @property
    # def nodes(self):
    #     """str, list : Node set or node keys the load is applied to."""  # TODO change
    #     return self._nodes

    # @property
    # def elements(self):
    #     """str, list : Element set or element keys the load is applied to."""  # TODO change
    #     return self._elements


class PrestressLoadBase(LoadBase):
    """Pre-stress [units: N/m2] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the PrestressLoad object.
    elements : str, list
        Element set or element keys the prestress is applied to.
    sxx : float
        Value of prestress for axial stress component sxx.
    """

    def __init__(self, name, elements, sxx=0):
        super(PrestressLoadBase).__init__(self, name=name, components={'sxx': sxx}, elements=elements, axes='local')
        self.__name__ = 'PrestressLoad'


class PointLoadBase(LoadBase):
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

    def __init__(self, name, nodes, x, y, z, xx, yy, zz, axes):
        LoadBase.__init__(self, name=name, components={'x': x, 'y': y, 'z': z,
                                                       'xx': xx, 'yy': yy, 'zz': zz}, axes=axes)
        self.__name__ = 'PointLoad'
        self._nodes = nodes

    @property
    def nodes(self):
        """The nodes property."""
        return self._nodes


# TODO prevent the user from assigning to a point
class LineLoadBase(LoadBase):
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
        LoadBase.__init__(self, name=name, components={'x': x, 'y': y, 'z': z,
                                                       'xx': xx, 'yy': yy, 'zz': zz}, elements=elements, axes=axes)
        self.__name__ = 'LineLoad'
        self._elements = elements

        @property
        def elements(self):
            """The elements property."""
            return self._elements


class AreaLoadBase(LoadBase):
    """Distributed area force [units:N/m2] applied to element(s).

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

    Attributes
    ----------
    name : str
        Name of the Load object.
    axes : str
        Load applied via 'local' or 'global' axes.
    components : dict
        Load components.
    elements : str, list
        Element set or element keys the load is applied to.
    """

    def __init__(self, name, elements, x=0, y=0, z=0, axes='local'):
        LoadBase.__init__(self, name=name, components={'x': x, 'y': y, 'z': z}, elements=elements, axes=axes)
        self.__name__ = 'AreaLoad'


class GravityLoadBase(LoadBase):
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
        LoadBase.__init__(self, components={'x': x, 'y': y, 'z': z}, name=name, axes='global')
        self.__name__ = 'GravityLoad'
        self.g = g


# class ThermalLoadBase(object):
#     """Thermal load.

#     Parameters
#     ----------
#     name : str
#         Name of the ThermalLoad object.
#     elements : str, list
#         Element set or element keys the load is applied to.
#     temperature : float
#         Temperature to apply to elements.

#     Attributes
#     ----------
#     name : str
#         Name of the ThermalLoad object.
#     elements : str, list
#         Element set or element keys the load is applied to.
#     temperature : float
#         Temperature to apply to elements.
#     """

#     def __init__(self, name, elements, temperature):
#         self.__name__ = 'ThermalLoad'
#         self.name = name
#         self.elements = elements
#         self.temperature = temperature

# # TODO: this should be a method of the Model object...or something in that direction


class TributaryLoadBase(LoadBase):
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
        LoadBase.__init__(self, name=name, components=components, nodes=nodes, axes=axes)
        self.__name__ = 'TributaryLoad'


class HarmonicPointLoadBase(LoadBase):
    """Harmonic concentrated forces and moments [units:N, Nm] applied to node(s).

    Parameters
    ----------
    name : str
        Name of the HarmoniPointLoadBase object.
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
        LoadBase.__init__(self, name=name, components={'x': x, 'y': y,
                                                       'z': z, 'xx': xx, 'yy': yy, 'zz': zz}, nodes=nodes, axes='global')
        self.__name__ = 'HarmoniPointLoadBase'


class HarmonicPressureLoadBase(LoadBase):
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
        LoadBase.__init__(self, name=name, components={'pressure': pressure,
                                                       'phase': phase}, elements=elements, axes='global')
        self.__name__ = 'HarmonicPressureLoad'


class AcousticDiffuseFieldLoadBase(LoadBase):
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
        LoadBase.__init__(self, name=name, components={
                          'air_density': air_density, 'sound_speed': sound_speed, 'max_inc_angle': max_inc_angle},
                          elements=elements, axes='global')
        self.__name__ = 'AcousticDiffuseFieldLoad'
