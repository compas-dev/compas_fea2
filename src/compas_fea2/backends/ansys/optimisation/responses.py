from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.responses import DesignResponse
from compas_fea2.optimisation.responses import EnergyStiffnessResponse
from compas_fea2.optimisation.responses import VolumeResponse


class AnsysDesignResponse(DesignResponse):
    """ Ansys implementation of :class:`.DesignResponse`.\n
    """
    __doc__ += DesignResponse.__doc__

    def __init__(self, group, group_operator, name=None, **kwargs):
        super(AnsysDesignResponse, self).__init__(group=group, group_operator=group_operator, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysEnergyStiffnessResponse(EnergyStiffnessResponse):
    """ Ansys implementation of :class:`.EnergyStiffnessResponse`.\n
    """
    __doc__ += EnergyStiffnessResponse.__doc__

    def __init__(self, group, group_operator, lc, name=None, **kwargs) -> None:
        super(AnsysEnergyStiffnessResponse, self).__init__(group=group,
                                                           group_operator=group_operator, lc=lc, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysVolumeResponse(VolumeResponse):
    """ Ansys implementation of :class:`.VolumeResponse`.\n
    """
    __doc__ += VolumeResponse.__doc__

    def __init__(self, group, group_operator, name=None, **kwargs):
        super(AnsysVolumeResponse, self).__init__(group=group, group_operator=group_operator, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
