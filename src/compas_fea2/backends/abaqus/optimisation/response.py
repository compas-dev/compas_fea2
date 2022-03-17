from compas_fea2._base.optimisation.response import VolumeResponseBase, EnergyStiffnessResponseBase


class VolumeResponse(VolumeResponseBase):
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


class EnergyStiffnessResponse(EnergyStiffnessResponseBase):
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
