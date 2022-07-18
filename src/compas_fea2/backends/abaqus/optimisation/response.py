from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.responses import VolumeResponse, EnergyStiffnessResponse


class AbaqusVolumeResponse(VolumeResponse):
    """Abaqus implementation of :class:`VolumeResponse`\n"""
    __doc__ += VolumeResponse.__doc__

    def __init__(self, group, group_operator, name=None, **kwargs):
        super(AbaqusVolumeResponse, self).__init__(group, group_operator, name=name, **kwargs)

    def _generate_jobdata(self):
        return f"""!
DRESP
  ID_NAME        = {self._name}
  TYPE           = {self._type}
  DEF_TYPE       = SYSTEM
  UPDATE         = EVER
  EL_GROUP       = {self._group}
  GROUP_OPER     = {self._group_operator}
END_
"""


class AbaqusEnergyStiffnessResponse(EnergyStiffnessResponse):
    """Abaqus implementation of :class:`EnergyStiffnessResponse`\n"""
    __doc__ += EnergyStiffnessResponse.__doc__

    def __init__(self, group, group_operator, lc, name=None, **kwargs):
        super(AbaqusEnergyStiffnessResponse, self).__init__(group, group_operator, lc, name=name, **kwargs)

    def _generate_jobdata(self):
        return f"""!
DRESP
  ID_NAME        = {self._name}
  TYPE           = {self._type}
  DEF_TYPE       = SYSTEM
  EL_GROUP       = {self._group}
  GROUP_OPER     = {self._group_operator}
  LC_SET         = {self._lc}
END_
"""
