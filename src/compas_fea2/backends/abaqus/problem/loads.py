from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from compas_fea2.problem import PrestressLoad
from compas_fea2.problem import PointLoad
from compas_fea2.problem import LineLoad
from compas_fea2.problem import AreaLoad
from compas_fea2.problem import GravityLoad
# from compas_fea2.problem import TributaryLoad
# from compas_fea2.problem import HarmonicPointLoad
# from compas_fea2.problem import HarmonicPressureLoad
# from compas_fea2.problem import AcousticDiffuseFieldLoad


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


# class AbaqusPrestressLoad(PrestressLoad):

#     def __init__(self):
#         super(AbaqusPrestressLoad, self).__init__()


class AbaqusPointLoad(PointLoad):
    """PointLoad class Abaqusfor Abaqus.

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
        super(AbaqusPointLoad, self).__init__(name=name, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes)

        self._modify = 'NEW' if modify else 'MOD'
        self._follow = ', follower' if follow else ''

    @property
    def op(self):
        """bool : if `True` create a new PointLoad otherwise modify the existing one, by default ``False``."""
        return self._op

    @property
    def follow(self):
        """bool : if `True` the load follows the deformation of the element."""
        return self._follow

    def _generate_jobdata(self, instance, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        chunks = [nodes[x:x+15] for x in range(0, len(nodes), 15)]  # split data for readibility
        data_section = [f'** Name: {self.name} Type: Concentrated Force',
                        f'*Nset, nset=_aux_{self.name}_{instance}, internal, instance={instance}',
                        '\n'.join([', '.join([str(node+1) for node in chunk]) for chunk in chunks]),
                        f'*Cload, OP={self._op}{self._follow}']
        data_section += [f'_aux_{self.name}_{instance}, {comp}, {self.components[dof]}' for comp,
                         dof in enumerate(dofs, 1) if self.components[dof]]  # FIXME: this should be similar to what happens for the BC or viceversa

        return '\n'.join(data_section) + '\n'


class AbaqusLineLoad(LineLoad):

    def __init__(self, name, elements, x, y, z, xx, yy, zz, axes):
        super(AbaqusLineLoad, self).__init__(name, elements, x, y, z, xx, yy, zz, axes)
        raise NotImplementedError


class AbaqusAreaLoad(AreaLoad):

    def __init__(self, name, elements, x, y, z, axes):
        super(AbaqusAreaLoad, self).__init__(name, elements, x, y, z, axes)
        raise NotImplementedError


class AbaqusGravityLoad(GravityLoad):

    def __init__(self, name, g=9.81, x=0., y=0., z=-1.):
        super(AbaqusGravityLoad, self).__init__(name, g, x, y, z)

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


# class AbaqusTributaryLoad(TributaryLoad):

#     def __init__(self, structure, name, mesh, x, y, z, axes):
#         super(AbaqusTributaryLoad, self).__init__(structure, name, mesh, x, y, z, axes)
#         raise NotImplementedError


# class AbaqusHarmonicPointLoad(HarmonicPointLoad):

#     def __init__(self, name, nodes, x, y, z, xx, yy, zz):
#         super(AbaqusHarmonicPointLoad, self).__init__(name, nodes, x, y, z, xx, yy, zz)
#         raise NotImplementedError


# class AbaqusHarmonicPressureLoad(HarmonicPressureLoad):
#     def __init__(self, name, elements, pressure, phase):
#         super(AbaqusHarmonicPressureLoad, self).__init__(name, elements, pressure, phase)
#         raise NotImplementedError


# class AbaqusAcousticDiffuseFieldLoad(AcousticDiffuseFieldLoad):
#     def __init__(self, name, elements, air_density, sound_speed, max_inc_angle):
#         super(AbaqusAcousticDiffuseFieldLoad, self).__init__(name, elements, air_density, sound_speed, max_inc_angle)
#         raise NotImplementedError
