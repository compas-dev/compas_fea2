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

class PrestressLoad(PrestressLoadBase):
    NotImplemented
    # def __init__(self, name, elements, sxx):
    #     super(PrestressLoad, self).__init__(name, elements, sxx)


class PointLoad(PointLoadBase):
    def __init__(self, name, lset, x=None, y=None, z=None, xx=None, yy=None, zz=None, modify=False, follow=False):
        super(PointLoad, self).__init__(name=name, nodes=None, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz)

        self.lset = lset
        if modify:
            self.op = 'NEW'
        else:
            self.op = 'MOD'
        if follow:
            self.follow = ', follower'
        else:
            self.follow = ''

        self.data = self._generate_data()

    def _generate_data(self):
        data_section = []
        line = """** Name: {} Type: Concentrated Force
*Cload, OP={}{}""".format(self.name, self.op, self.follow)
        data_section.append(line)
        c=1
        for dof in dofs:
            if self.components[dof]:
                line = """{}, {}, {}""".format(self.lset.name, c, self.components[dof])
                data_section.append(line)
            c+=1
        return '\n'.join(data_section) +'\n'


class LineLoad(LineLoadBase):
    NotImplemented
    # def __init__(self, name, elements, x, y, z, xx, yy, zz, axes):
    #     super(LineLoad, self).__init__(name, elements, x, y, z, xx, yy, zz, axes)


class AreaLoad(AreaLoadBase):
    NotImplemented
    # def __init__(self, name, elements, x, y, z, axes):
    #     super(AreaLoad, self).__init__(name, elements, x, y, z, axes)


class GravityLoad(GravityLoadBase):
    NotImplemented
    # def __init__(self, name, elements, g, x, y, z):
    #     super(GravityLoad, self).__init__(name, elements, g, x, y, z)


class ThermalLoad(ThermalLoadBase):
    NotImplemented
    # def __init__(self, name, elements, temperature):
    #     super(ThermalLoad, self).__init__(name, elements, temperature)


class TributaryLoad(TributaryLoadBase):
    NotImplemented
    # def __init__(self, structure, name, mesh, x, y, z, axes):
    #     super(TributaryLoad, self).__init__(structure, name, mesh, x, y, z, axes)


class HarmoniPointLoadBase(HarmonicPointLoadBase):
    NotImplemented
    # def __init__(self, name, nodes, x, y, z, xx, yy, zz):
    #     super(HarmoniPointLoadBase, self).__init__(name, nodes, x, y, z, xx, yy, zz)


class HarmonicPressureLoad(HarmonicPressureLoadBase):
    NotImplemented
    # def __init__(self, name, elements, pressure, phase):
    #     super(HarmonicPressureLoad, self).__init__(name, elements, pressure, phase)


class AcousticDiffuseFieldLoad(AcousticDiffuseFieldLoadBase):
    NotImplemented
    # def __init__(self, name, elements, air_density, sound_speed, max_inc_angle):
    #     super(AcousticDiffuseFieldLoad, self).__init__(name, elements, air_density, sound_speed, max_inc_angle)
