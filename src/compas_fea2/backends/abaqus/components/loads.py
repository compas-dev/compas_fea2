from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._core import LoadBase
from compas_fea2.backends._core import PrestressLoadBase
from compas_fea2.backends._core import PointLoadBase
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
    'PrestressLoad',
    'PointLoad',
    'LineLoad',
    'AreaLoad',
    'GravityLoad',
    'ThermalLoad',
    'TributaryLoad',
    'HarmoniPointLoadBase',
    'HarmonicPressureLoad',
    'AcousticDiffuseFieldLoad'
]

dofs    = ['x',  'y',  'z',  'xx', 'yy', 'zz']

def _write_load_data(obj, f):
    line = """** Name: {} Type: Concentrated force
*Cload, OP={0}\n""".format(obj.name, obj.op)
    f.write(line)
    c=1
    for dof in dofs:
        if dof in obj.components.keys() and obj.components[dof]!=None:
            if not obj.components[dof]:
                line = """{}, {}, {}\n""".format(obj.bset, c, c)
            else:
                line = """{}, {}, {}, {}\n""".format(obj.bset, c, c, obj.components[dof])
            f.write(line)
        c+=1

class PrestressLoad(PrestressLoadBase):
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
    pass
    # def __init__(self, name, elements, sxx):
    #     super(PrestressLoad, self).__init__(name, elements, sxx)


class PointLoad(PointLoadBase):
    def __init__(self, name, nodes, x, y, z, xx, yy, zz):
        super(PointLoad, self).__init__(name, nodes, x, y, z, xx, yy, zz)

    def write_data(self, f):
        _write_load_data(self, f)

class LineLoad(LineLoadBase):
    pass
    # def __init__(self, name, elements, x, y, z, xx, yy, zz, axes):
    #     super(LineLoad, self).__init__(name, elements, x, y, z, xx, yy, zz, axes)


class AreaLoad(AreaLoadBase):
    pass
    # def __init__(self, name, elements, x, y, z, axes):
    #     super(AreaLoad, self).__init__(name, elements, x, y, z, axes)


class GravityLoad(GravityLoadBase):
    pass
    # def __init__(self, name, elements, g, x, y, z):
    #     super(GravityLoad, self).__init__(name, elements, g, x, y, z)


class ThermalLoad(ThermalLoadBase):
    pass
    # def __init__(self, name, elements, temperature):
    #     super(ThermalLoad, self).__init__(name, elements, temperature)


class TributaryLoad(TributaryLoadBase):
    pass
    # def __init__(self, structure, name, mesh, x, y, z, axes):
    #     super(TributaryLoad, self).__init__(structure, name, mesh, x, y, z, axes)


class HarmoniPointLoadBase(HarmonicPointLoadBase):
    pass
    # def __init__(self, name, nodes, x, y, z, xx, yy, zz):
    #     super(HarmoniPointLoadBase, self).__init__(name, nodes, x, y, z, xx, yy, zz)


class HarmonicPressureLoad(HarmonicPressureLoadBase):
    pass
    # def __init__(self, name, elements, pressure, phase):
    #     super(HarmonicPressureLoad, self).__init__(name, elements, pressure, phase)


class AcousticDiffuseFieldLoad(AcousticDiffuseFieldLoadBase):
    pass
    # def __init__(self, name, elements, air_density, sound_speed, max_inc_angle):
    #     super(AcousticDiffuseFieldLoad, self).__init__(name, elements, air_density, sound_speed, max_inc_angle)
