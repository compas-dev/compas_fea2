from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import PointLoad
from compas_fea2.problem import LineLoad
from compas_fea2.problem import AreaLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import TributaryLoad
from compas_fea2.problem import PrestressLoad
from compas_fea2.problem import HarmonicPointLoad
from compas_fea2.problem import HarmonicPressureLoad


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class AbaqusPointLoad(PointLoad):
    """Abaqus implementation of :class:`PointLoad`.\n"""
    __doc__ += PointLoad.__doc__
    """
    Additional Parameters
    ---------------------
    modify : bool, optional
        If ``True``, change previous displacements applied at the same location, otherwise
        add the displacement to the previous. By defult is ``True``.
    follow : bool, optional
        if `True` the load follows the deformation of the element.

    Additional Attributes
    ---------------------
    op : bool
        If ``True``, change previous displacements applied at the same location, otherwise
        add the displacement to the previous.
    follow : bool
        if `True` the load follows the deformation of the element.
    """

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=False, follow=False, name=None, **kwargs):
        super(AbaqusPointLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)

        self._modify = ', OP=NEW' if modify else ', OP=MOD'
        self._follow = ', follower' if follow else ''

    @property
    def op(self):
        return self._op

    @property
    def follow(self):
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

        data_section = ['** Name: {} Type: oncentrated Force'.format(self.name),
                        '*Cload{}{}'.format(self._modify, self._follow)]
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if getattr(self, dof):
                    data_section += ['{}.{}, {}, {}'.format(instance, node.key+1, comp, self.components[dof])]
        return '\n'.join(data_section)


class AbaqusLineLoad(LineLoad):
    """Abaqus implementation of :class:`LineLoad`.\n"""
    __doc__ += LineLoad.__doc__

    def __init__(self, elements, x, y, z, xx, yy, zz, axes, name=None, **kwargs):
        super(AbaqusLineLoad, self).__init__(elements, x, y, z, xx, yy, zz, axes, name=name, **kwargs)
        raise NotImplementedError


class AbaqusAreaLoad(AreaLoad):
    """Abaqus implementation of :class:`AreaLoad`.\n"""
    __doc__ += AreaLoad.__doc__

    def __init__(self, elements, x, y, z, axes, name=None, **kwargs):
        super(AbaqusAreaLoad, self).__init__(elements, x, y, z, axes, name=name, **kwargs)
        raise NotImplementedError


class AbaqusGravityLoad(GravityLoad):
    """Abaqus implementation of :class:`GravityLoad`.\n"""
    __doc__ += GravityLoad.__doc__

    def __init__(self, g=9.81, x=0., y=0., z=-1., name=None, **kwargs):
        super(AbaqusGravityLoad, self).__init__(g, x, y, z, name=name, **kwargs)

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
                ", GRAV, {}, {}, {}, {}").format(self.name, self.g, self.components['x'],
                                                 self.components['y'], self.components['z'])


class AbaqusPrestressLoad(PrestressLoad):
    """Abaqus implementation of :class:`PrestressLoad`.\n"""
    __doc__ += PrestressLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AbaqusPrestressLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class AbaqusTributaryLoad(TributaryLoad):
    """Abaqus implementation of :class:`TributaryLoad`.\n"""
    __doc__ += TributaryLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AbaqusTributaryLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class AbaqusHarmonicPointLoad(HarmonicPointLoad):
    """Abaqus implementation of :class:`HarmonicPointLoad`.\n"""
    __doc__ += HarmonicPointLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AbaqusHarmonicPointLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class AbaqusHarmonicPressureLoad(HarmonicPressureLoad):
    """Abaqus implementation of :class:`HarmonicPressureLoad`.\n"""
    __doc__ += HarmonicPressureLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AbaqusHarmonicPressureLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError
