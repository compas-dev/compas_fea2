from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.bcs import _BoundaryCondition
from compas_fea2.model.bcs import FixedBC
from compas_fea2.model.bcs import ClampBCXX
from compas_fea2.model.bcs import ClampBCYY
from compas_fea2.model.bcs import ClampBCZZ
from compas_fea2.model.bcs import PinnedBC
from compas_fea2.model.bcs import RollerBCX
from compas_fea2.model.bcs import RollerBCXY
from compas_fea2.model.bcs import RollerBCXZ
from compas_fea2.model.bcs import RollerBCY
from compas_fea2.model.bcs import RollerBCYZ
from compas_fea2.model.bcs import RollerBCZ


class AnsysBoundaryCondition(_BoundaryCondition):
    """Ansys implementation of :class:`compas_fea2.model.bcs._BoundaryCondition`.\n
    """
    __doc__ += _BoundaryCondition.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysBoundaryCondition, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysFixedBC(FixedBC):
    """Ansys implementation of :class:`compas_fea2.model.bcs.FixedBC`.\n
    """
    __doc__ += FixedBC.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysFixedBC, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysClampBCXX(ClampBCXX):
    """Ansys implementation of :class:`compas_fea2.model.bcs.FixedBCXX`.\n
    """
    __doc__ += ClampBCXX.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysClampBCXX, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysClampBCYY(ClampBCYY):
    """Ansys implementation of :class:`compas_fea2.model.bcs.FixedBCYY`.\n
    """
    __doc__ += ClampBCYY.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysClampBCYY, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysClampBCZZ(ClampBCZZ):
    """Ansys implementation of :class:`compas_fea2.model.bcs.FixedBCZZ`.\n
    """
    __doc__ += ClampBCZZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysClampBCZZ, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysPinnedBC(PinnedBC):
    """Ansys implementation of :class:`compas_fea2.model.bcs.PinnedBC`.\n
    """
    __doc__ += PinnedBC.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysPinnedBC, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysRollerBCX(RollerBCX):
    """Ansys implementation of :class:`compas_fea2.model.bcs.RollerBCX`.\n
    """
    __doc__ += RollerBCX.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysRollerBCX, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysRollerBCXY(RollerBCXY):
    """Ansys implementation of :class:`compas_fea2.model.bcs.RollerBCXY`.\n
    """
    __doc__ += RollerBCXY.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysRollerBCXY, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysRollerBCXZ(RollerBCXZ):
    """Ansys implementation of :class:`compas_fea2.model.bcs.RollerBCXZ`.\n
    """
    __doc__ += RollerBCXZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysRollerBCXZ, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysRollerBCY(RollerBCY):
    """Ansys implementation of :class:`compas_fea2.model.bcs.RollerBCY`.\n
    """
    __doc__ += RollerBCY.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysRollerBCY, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysRollerBCYZ(RollerBCYZ):
    """Ansys implementation of :class:`compas_fea2.model.bcs.RollerBCYZ`.\n
    """
    __doc__ += RollerBCYZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysRollerBCYZ, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysRollerBCZ(RollerBCZ):
    """Ansys implementation of :class:`compas_fea2.model.bcs.RollerBCZ`.\n
    """
    __doc__ += RollerBCZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysRollerBCZ, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
