from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.bcs import ClampBCXX
from compas_fea2.model.bcs import ClampBCYY
from compas_fea2.model.bcs import ClampBCZZ
from compas_fea2.model.bcs import FixedBC
from compas_fea2.model.bcs import GeneralBC
from compas_fea2.model.bcs import PinnedBC
from compas_fea2.model.bcs import RollerBCX
from compas_fea2.model.bcs import RollerBCXY
from compas_fea2.model.bcs import RollerBCXZ
from compas_fea2.model.bcs import RollerBCY
from compas_fea2.model.bcs import RollerBCYZ
from compas_fea2.model.bcs import RollerBCZ

def _generate_jobdata(obj, nodes):
    """Generate the data for the input file for any bc.

    Parameters
    ----------
    obj : :class:`compas_fea2.model.bcs._BoundaryCondition`
        The boundary condition
    nodes : [:class:`compas_fea2.model.nodes.Node]
        The nodes where the boundary condition is applied.

    Returns
    -------
    str
        input file data string
    """
    comp = {'x':'PX','y':'PY','z':'PZ','xx':'MX','yy':'MY','zz':'MZ'}
    return "\n".join(["NODE NO {} FIX {}".format(node.key+1,
                                           ','.join([comp[c] for c in comp if getattr(obj, c)]))
                for node in nodes])

class SofistikClampBCXX(ClampBCXX):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.ClampBCXX`.\n
    """
    __doc__ += ClampBCXX.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikClampBCXX, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikClampBCYY(ClampBCYY):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.ClampBCYY`.\n
    """
    __doc__ += ClampBCYY.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikClampBCYY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikClampBCZZ(ClampBCZZ):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.ClampBCZZ`.\n
    """
    __doc__ += ClampBCZZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikClampBCZZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikFixedBC(FixedBC):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.FixedBC`.\n
    """
    __doc__ += FixedBC.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikFixedBC, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikGeneralBC(GeneralBC):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.GeneralBC`.\n
    """
    __doc__ += GeneralBC.__doc__

    def __init__(self, name=None, x=False, y=False, z=False, xx=False, yy=False, zz=False, **kwargs):
        super(SofistikGeneralBC, self).__init__(name=name, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class SofistikPinnedBC(PinnedBC):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.PinnedBC`.\n
    """
    __doc__ += PinnedBC.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikPinnedBC, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikRollerBCX(RollerBCX):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.RollerBCX`.\n
    """
    __doc__ += RollerBCX.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikRollerBCX, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikRollerBCXY(RollerBCXY):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.RollerBCXY`.\n
    """
    __doc__ += RollerBCXY.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikRollerBCXY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikRollerBCXZ(RollerBCXZ):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.RollerBCXZ`.\n
    """
    __doc__ += RollerBCXZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikRollerBCXZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikRollerBCY(RollerBCY):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.RollerBCY`.\n
    """
    __doc__ += RollerBCY.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikRollerBCY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikRollerBCYZ(RollerBCYZ):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.RollerBCYZ`.\n
    """
    __doc__ += RollerBCYZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikRollerBCYZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

class SofistikRollerBCZ(RollerBCZ):
    """Sofistik implementation of :class:`compas_fea2.model.bcs.RollerBCZ`.\n
    """
    __doc__ += RollerBCZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikRollerBCZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)

