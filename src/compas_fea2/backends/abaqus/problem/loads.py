from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem import LoadBase
from compas_fea2.backends._base.problem import PrestressLoadBase
from compas_fea2.backends._base.problem import PointLoadBase
from compas_fea2.backends._base.problem import LineLoadBase
from compas_fea2.backends._base.problem import AreaLoadBase
from compas_fea2.backends._base.problem import GravityLoadBase
from compas_fea2.backends._base.problem import ThermalLoadBase
from compas_fea2.backends._base.problem import TributaryLoadBase
from compas_fea2.backends._base.problem import HarmonicPointLoadBase
from compas_fea2.backends._base.problem import HarmonicPressureLoadBase
from compas_fea2.backends._base.problem import AcousticDiffuseFieldLoadBase


# Author(s): Francesco Ranaudo (github.com/franaudo)


__all__ = [
    # 'PrestressLoad',
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

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']

# class PrestressLoad(PrestressLoadBase):
#     NotImplemented
#     # def __init__(self, name, elements, sxx):
#     #     super(PrestressLoad, self).__init__(name, elements, sxx)


class PointLoad(PointLoadBase):
    # TODO: add the possibility to apply the load to a node and not just to a node set
    def __init__(self, name, lset, x=None, y=None, z=None, xx=None, yy=None, zz=None, modify=False, follow=False):
        super(PointLoad, self).__init__(
            name=name, nodes=None, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz)

        self.lset = lset
        if modify:
            self.op = 'NEW'
        else:
            self.op = 'MOD'
        if follow:
            self.follow = ', follower'
        else:
            self.follow = ''

        self._jobdata = self._generate_data()

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file.

        Returns
        -------
        str

        Examples
        --------
        >>>
        """
        return self._jobdata

    def _generate_data(self):
        data_section = []
        line = ("** Name: {} Type: Concentrated Force\n"
                "*Cload, OP={}{}").format(self.name, self.op, self.follow)
        data_section.append(line)
        c = 1
        for dof in dofs:
            if self.components[dof]:
                line = """{}, {}, {}""".format(
                    self.lset, c, self.components[dof])
                data_section.append(line)
            c += 1
        return '\n'.join(data_section) + '\n'


class LineLoad(LineLoadBase):

    def __init__(self, name, elements, x, y, z, xx, yy, zz, axes):
        super(LineLoad, self).__init__(name, elements, x, y, z, xx, yy, zz, axes)
        raise NotImplementedError


class AreaLoad(AreaLoadBase):

    def __init__(self, name, elements, x, y, z, axes):
        super(AreaLoad, self).__init__(name, elements, x, y, z, axes)
        raise NotImplementedError


class GravityLoad(GravityLoadBase):

    def __init__(self, name, g, x, y, z):
        super(GravityLoad, self).__init__(name, g, x, y, z)
        self.lset = None

    def _generate_data(self):
        return ("** Name: {} Type: Gravity\n"
                "*Dload\n"
                ", GRAV, {}, {}, {}, {}\n").format(self.name, self.g, self.components['x'],
                                                   self.components['y'], self.components['z'])


class ThermalLoad(ThermalLoadBase):

    def __init__(self, name, elements, temperature):
        super(ThermalLoad, self).__init__(name, elements, temperature)
        raise NotImplementedError


class TributaryLoad(TributaryLoadBase):

    def __init__(self, structure, name, mesh, x, y, z, axes):
        super(TributaryLoad, self).__init__(structure, name, mesh, x, y, z, axes)
        raise NotImplementedError


class HarmoniPointLoadBase(HarmonicPointLoadBase):

    def __init__(self, name, nodes, x, y, z, xx, yy, zz):
        super(HarmoniPointLoadBase, self).__init__(name, nodes, x, y, z, xx, yy, zz)
        raise NotImplementedError


class HarmonicPressureLoad(HarmonicPressureLoadBase):
    def __init__(self, name, elements, pressure, phase):
        super(HarmonicPressureLoad, self).__init__(name, elements, pressure, phase)
        raise NotImplementedError


class AcousticDiffuseFieldLoad(AcousticDiffuseFieldLoadBase):
    def __init__(self, name, elements, air_density, sound_speed, max_inc_angle):
        super(AcousticDiffuseFieldLoad, self).__init__(name, elements, air_density, sound_speed, max_inc_angle)
        raise NotImplementedError
