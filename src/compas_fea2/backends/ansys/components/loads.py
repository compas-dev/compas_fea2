
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._core import LoadBase
from compas_fea2.backends._core import PrestressLoadBase
from compas_fea2.backends._core import PointLoadBase
from compas_fea2.backends._core import PointLoadsBase
from compas_fea2.backends._core import LineLoadBase
from compas_fea2.backends._core import AreaLoadBase
from compas_fea2.backends._core import GravityLoadBase
from compas_fea2.backends._core import ThermalLoadBase
from compas_fea2.backends._core import TributaryLoadBase
from compas_fea2.backends._core import HarmonicPointLoadBase
from compas_fea2.backends._core import HarmonicPressureLoadBase
from compas_fea2.backends._core import AcousticDiffuseFieldLoadBase


# Author(s): Francesco Ranaudo (github.com/franaudo)



__all__ = [
    'Load',
    'PrestressLoad',
    'PointLoad',
    'PointLoads',
    'LineLoad',
    'AreaLoad',
    'GravityLoad',
    'ThermalLoad',
    'TributaryLoad',
    'HarmoniPointLoadBase',
    'HarmonicPressureLoad',
    'AcousticDiffuseFieldLoad'
]


class Load(LoadBase):

    """ Initialises base Load object.

    Parameters
    ----------
    name : str
        Name of the Load object.
    axes : str
        Load applied via 'local' or 'global' axes.
    components : dict
        Load components.
    nodes : str, list
        Node set or node keys the load is applied to.
    elements : str, list
        Element set or element keys the load is applied to.

    Attributes
    ----------
    name : str
        Name of the Load object.
    axes : str
        Load applied via 'local' or 'global' axes.
    components : dict
        Load components.
    nodes : str, list
        Node set or node keys the load is applied to.
    elements : str, list
        Element set or element keys the load is applied to.

    """
    pass
    # def __init__(self, name, axes, components, nodes, elements):
    #     super(Load, self).__init__(name, axes, components, nodes, elements)


class PrestressLoad(PrestressLoadBase):

    """ Pre-stress [units: N/m2] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the PrestressLoad object.
    elements : str, list
        Element set or element keys the prestress is applied to.
    sxx : float
        Value of prestress for axial stress component sxx.

    """
    pass
    # def __init__(self, name, elements, sxx):
    #     super(PrestressLoad, self).__init__(name, elements, sxx)


class PointLoad(PointLoadBase):

    """ Concentrated forces and moments [units:N, Nm] applied to node(s).

    Parameters
    ----------
    name : str
        Name of the PointLoad object.
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
    pass
    # def __init__(self, name, nodes, x, y, z, xx, yy, zz):
    #     super(PointLoad, self).__init__(name, nodes, x, y, z, xx, yy, zz)


class PointLoads(PointLoadsBase):

    """ Concentrated forces and moments [units:N, Nm] applied to different nodes.

    Parameters
    ----------
    name : str
        Name of the PointLoads object.
    components : dict
        Node key : components dictionary data.

    """
    pass
    # def __init__(self, name, components):
    #     super(PointLoads, self).__init__(name, components)


class LineLoad(LineLoadBase):

    """ Distributed line forces and moments [units:N/m or Nm/m] applied to element(s).

    Parameters
    ----------
    name : str
        Name of the LineLoad object.
    elements : str, list
        Element set or element keys the load is applied to.
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

    """
    pass
    # def __init__(self, name, elements, x, y, z, xx, yy, zz, axes):
    #     super(LineLoad, self).__init__(name, elements, x, y, z, xx, yy, zz, axes)


class AreaLoad(AreaLoadBase):

    """ Distributed area force [units:N/m2] applied to element(s).

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
    pass
    # def __init__(self, name, elements, x, y, z, axes):
    #     super(AreaLoad, self).__init__(name, elements, x, y, z, axes)


class GravityLoad(GravityLoadBase):

    """ Gravity load [units:N/m3] applied to element(s).

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
    pass
    # def __init__(self, name, elements, g, x, y, z):
    #     super(GravityLoad, self).__init__(name, elements, g, x, y, z)


class ThermalLoad(ThermalLoadBase):

    """ Thermal load.

    Parameters
    ----------
    name : str
        Name of the ThermalLoad object.
    elements : str, list
        Element set or element keys the load is applied to.
    temperature : float
        Temperature to apply to elements.

    """
    pass
    # def __init__(self, name, elements, temperature):
    #     super(ThermalLoad, self).__init__(name, elements, temperature)


class TributaryLoad(TributaryLoadBase):

    """ Tributary area loads applied to nodes.

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

    Notes
    -----
    - The load components are loads per unit area [N/m2].
    - Currently only supports 'global' axis.

    """
    pass
    # def __init__(self, structure, name, mesh, x, y, z, axes):
    #     super(TributaryLoad, self).__init__(structure, name, mesh, x, y, z, axes)


class HarmoniPointLoadBase(HarmonicPointLoadBase):

    """ Harmonic concentrated forces and moments [units:N, Nm] applied to node(s).

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
    pass
    # def __init__(self, name, nodes, x, y, z, xx, yy, zz):
    #     super(HarmoniPointLoadBase, self).__init__(name, nodes, x, y, z, xx, yy, zz)


class HarmonicPressureLoad(HarmonicPressureLoadBase):

    """ Harmonic pressure loads [units:N/m2] applied to element(s).

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
    pass
    # def __init__(self, name, elements, pressure, phase):
    #     super(HarmonicPressureLoad, self).__init__(name, elements, pressure, phase)


class AcousticDiffuseFieldLoad(AcousticDiffuseFieldLoadBase):

    """ Acoustic Diffuse field loads applied to elements.

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
    pass
    # def __init__(self, name, elements, air_density, sound_speed, max_inc_angle):
    #     super(AcousticDiffuseFieldLoad, self).__init__(name, elements, air_density, sound_speed, max_inc_angle)
