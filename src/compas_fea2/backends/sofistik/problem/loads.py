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
from compas_fea2.problem.loads import ThermalLoad
from compas_fea2.problem.loads import TributaryLoad


class SofistikAreaLoad(AreaLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.AreaLoad`.\n
    """
    __doc__ += AreaLoad.__doc__

    def __init__(self, x=0, y=0, z=0, axes='local', name=None, **kwargs):
        super(SofistikAreaLoad, self).__init__(x=x, y=y, z=z, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class SofistikGravityLoad(GravityLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.GravityLoad`.\n
    """
    __doc__ += GravityLoad.__doc__

    def __init__(self, g, x=0, y=0, z=-1, name=None, **kwargs):
        super(SofistikGravityLoad, self).__init__(g=g, x=x, y=y, z=z, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class SofistikHarmonicPointLoad(HarmonicPointLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.HarmonicPointLoad`.\n
    """
    __doc__ += HarmonicPointLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(SofistikHarmonicPointLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class SofistikHarmonicPressureLoad(HarmonicPressureLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.HarmonicPressureLoad`.\n
    """
    __doc__ += HarmonicPressureLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(SofistikHarmonicPressureLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class SofistikLineLoad(LineLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.LineLoad`.\n
    """
    __doc__ += LineLoad.__doc__

    def __init__(self, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global', name=None, **kwargs):
        super(SofistikLineLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class SofistikPointLoad(PointLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.PointLoad`.\n
    """
    __doc__ += PointLoad.__doc__

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', name=None, **kwargs):
        super(SofistikPointLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)
    
    #FIXME

    #Put Outside of the SofistikPointLoad the generation of the string "LC {} TITL 'point load'"

    def _generate_jobdata(self, nodes):
        loadcase_data_section = ["LC {} TITL 'point load'".format(i+1) for i in range(len(nodes))] #self.name
        node_def_data_section = ["NODE NO {} TYPE VV {} {} {} {} {} {}".format(node.key+1,
                                                                            "P1 {}".format(self.x) if self.x else "",
                                                                            "P2 {}".format(self.y) if self.y else "",
                                                                            "P3 {}".format(self.z) if self.z else "",
                                                                            "P4 {}".format(self.yy) if self.xx else "",
                                                                            "P5 {}".format(self.yy) if self.yy else "",
                                                                            "P6 {}".format(self.zz) if self.zz else "") for node in nodes]
        job_data = []
        for i in range(len(nodes)):
            job_data.append(loadcase_data_section[i])
            job_data.append(node_def_data_section[i])
        return '\n'.join(job_data)

class SofistikPrestressLoad(PrestressLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.PrestressLoad`.\n
    """
    __doc__ += PrestressLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(SofistikPrestressLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class SofistikThermalLoad(ThermalLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.ThermalLoad`.\n
    """
    __doc__ += ThermalLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(SofistikThermalLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class SofistikTributaryLoad(TributaryLoad):
    """Sofistik implementation of :class:`compas_fea2.problem.loads.TributaryLoad`.\n
    """
    __doc__ += TributaryLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(SofistikTributaryLoad, self).__init__(components=components, axes=axes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
