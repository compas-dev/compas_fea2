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


class OpenseesPointLoad(PointLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.PointLoad`.\n
    """
    __doc__ += PointLoad.__doc__

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', name=None, **kwargs):
        super(OpenseesPointLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)

    def _generate_jobdata(self):
        jobdata = []
        for node in self.nodes:
            jobdata.append('load {} {}'.format(node, ' '.join([str(self.components[dof]) for dof in dofs])))
        return '\n'.join(jobdata)


class OpenseesLineLoad(LineLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.LineLoad`.\n
    """
    __doc__ += LineLoad.__doc__

    def __init__(self, elements, x, y, z, xx, yy, zz, axes, name=None, **kwargs):
        super(OpenseesLineLoad, self).__init__(elements, x, y, z, xx, yy, zz, axes, name=name, **kwargs)
        raise NotImplementedError


class OpenseesAreaLoad(AreaLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.AreaLoad`.\n
    """
    __doc__ += AreaLoad.__doc__

    def __init__(self, elements, x, y, z, axes, name=None, **kwargs):
        super(OpenseesAreaLoad, self).__init__(elements, x, y, z, axes, name=name, **kwargs)
        raise NotImplementedError


class OpenseesGravityLoad(GravityLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.GravityLoad`.\n
    """
    __doc__ += GravityLoad.__doc__

    def __init__(self, g=9.81, x=0., y=0., z=-1., name=None, **kwargs):
        super(OpenseesGravityLoad, self).__init__(g, x, y, z, name=name, **kwargs)
        raise NotImplementedError


class OpenseesPrestressLoad(PrestressLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.PrestressLoad`.\n
    """
    __doc__ += PrestressLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesPrestressLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class OpenseesTributaryLoad(TributaryLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.TributaryLoad`.\n
    """
    __doc__ += TributaryLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesTributaryLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class OpenseesHarmonicPointLoad(HarmonicPointLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.HarmonicPointLoad`.\n
    """
    __doc__ += HarmonicPointLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesHarmonicPointLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class OpenseesHarmonicPressureLoad(HarmonicPressureLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.HarmonicPressureLoad`.\n
    """
    __doc__ += HarmonicPressureLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesHarmonicPressureLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError
