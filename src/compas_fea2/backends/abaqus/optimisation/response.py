from compas_fea2.optimisation.responses import VolumeResponse, EnergyStiffnessResponse


class AbaqusVolumeResponse(VolumeResponse):
    def __init__(self, group, group_operator) -> None:
        super().__init__(group, group_operator)

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
    def __init__(self, group, group_operator, lc) -> None:
        super().__init__(group, group_operator, lc)

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
