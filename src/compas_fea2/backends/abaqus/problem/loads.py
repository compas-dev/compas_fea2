from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem import PrestressLoadBase
from compas_fea2.backends._base.problem import PointLoadBase
from compas_fea2.backends._base.problem import LineLoadBase
from compas_fea2.backends._base.problem import AreaLoadBase
from compas_fea2.backends._base.problem import GravityLoadBase
# from compas_fea2.backends._base.problem import ThermalLoadBase
from compas_fea2.backends._base.problem import TributaryLoadBase
from compas_fea2.backends._base.problem import HarmonicPointLoadBase
from compas_fea2.backends._base.problem import HarmonicPressureLoadBase
from compas_fea2.backends._base.problem import AcousticDiffuseFieldLoadBase

from compas_fea2.backends._base.model import NodesGroupBase
from compas_fea2.backends._base.model import ElementsGroupBase

# Author(s): Francesco Ranaudo (github.com/franaudo)


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class PrestressLoad(PrestressLoadBase):
    NotImplemented


class PointLoad(PointLoadBase):
    """PointLoad class for Abaqus.

    Parameters
    ----------
    name : str
        Name of the PointLoad object.
    x : float, optional
        x component of force, by default `0.`.
    y : float, optional
        y component of force, by default `0.`.
    z : float, optional
        z component of force, by default `0.`.
    xx : float, optional
        xx component of moment, by default `0.`.
    yy : float, optional
        yy component of moment, by default `0.`.
    zz : float, optional
        zz component of moment, by default `0.`.
    axes : str, optional
        Load applied via 'local' or 'global' axes, by default 'global'.
    modify : bool, optional
        if `True`
    follow : bool, optional
        if `True` the load follows the deformation of the element.
    """

    def __init__(self, name, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=False, follow=False):
        super(PointLoad, self).__init__(name=name, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes)

        self._op = 'NEW' if modify else 'MOD'
        self._follow = ', follower' if follow else ''

    def _generate_jobdata(self, instance, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = [f'** Name: {self.name} Type: Concentrated Force\n',
                        f'*Cload, OP={self._op}{self._follow}']
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if self.components[dof]:
                    data_section += [f'{instance}.{node+1}, {comp}, {self.components[dof]}']
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

    def __init__(self, name, g=9.81, x=0., y=0., z=-1.):
        super(GravityLoad, self).__init__(name, g, x, y, z)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return ("** Name: {} Type: Gravity\n"
                "*Dload\n"
                ", GRAV, {}, {}, {}, {}\n").format(self.name, self.g, self.components['x'],
                                                   self.components['y'], self.components['z'])


# class ThermalLoad(ThermalLoadBase):

#     def __init__(self, name, elements, temperature):
#         super(ThermalLoad, self).__init__(name, elements, temperature)
#         raise NotImplementedError


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
