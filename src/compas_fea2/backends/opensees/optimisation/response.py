from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.responses import VolumeResponse, EnergyStiffnessResponse


class OpenseesVolumeResponse(VolumeResponse):
    def __init__(self, group, group_operator, name=None, **kwargs):
        super(OpenseesVolumeResponse, self).__init__(group, group_operator, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesEnergyStiffnessResponse(EnergyStiffnessResponse):
    def __init__(self, group, group_operator, lc, name=None, **kwargs):
        super(OpenseesEnergyStiffnessResponse, self).__init__(group, group_operator, lc, name=name, **kwargs)
        raise NotImplementedError()
