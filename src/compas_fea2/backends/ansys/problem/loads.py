from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.loads import AreaLoad
from compas_fea2.problem.loads import GravityLoad
from compas_fea2.problem.loads import HarmonicPointLoad
from compas_fea2.problem.loads import HarmonicPressureLoad
from compas_fea2.problem.loads import LineLoad
from compas_fea2.problem.loads import PointLoad
from compas_fea2.problem.loads import PrestressLoad
from compas_fea2.problem.loads import TributaryLoad

class AnsysAreaLoad(AreaLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.AreaLoad`.\n
    """
    __doc__ += AreaLoad.__doc__

    def __init__(self, x=0, y=0, z=0, axes='local', name=None, **kwargs):
        super(AnsysAreaLoad, self).__init__(x=x, y=y, z=z, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysGravityLoad(GravityLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.GravityLoad`.\n
    """
    __doc__ += GravityLoad.__doc__

    def __init__(self, g, x, y, z, name=None, **kwargs):
        super(AnsysGravityLoad, self).__init__(g=g, x=x, y=y, z=z, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysHarmonicPointLoad(HarmonicPointLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.HarmonicPointLoad`.\n
    """
    __doc__ += HarmonicPointLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AnsysHarmonicPointLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysHarmonicPressureLoad(HarmonicPressureLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.HarmonicPressureLoad`.\n
    """
    __doc__ += HarmonicPressureLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AnsysHarmonicPressureLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysLineLoad(LineLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.LineLoad`.\n
    """
    __doc__ += LineLoad.__doc__

    def __init__(self, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global', name=None, **kwargs):
        super(AnsysLineLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysPointLoad(PointLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.PointLoad`.\n
    """
    __doc__ += PointLoad.__doc__

    def __init__(self, x, y, z, xx, yy, zz, axes, name=None, **kwargs):
        super(AnsysPointLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysPrestressLoad(PrestressLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.PrestressLoad`.\n
    """
    __doc__ += PrestressLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AnsysPrestressLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysTributaryLoad(TributaryLoad):
    """Ansys implementation of :class:`compas_fea2.problem.loads.TributaryLoad`.\n
    """
    __doc__ += TributaryLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(AnsysTributaryLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

