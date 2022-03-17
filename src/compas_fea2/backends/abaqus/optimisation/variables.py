from compas_fea2._base.optimisation.variables import DesignVariablesBase


class DesignVariables(DesignVariablesBase):
    def __init__(self, name, variables) -> None:
        super().__init__(name, variables)

    def _generate_jobdata(self):
        return f"""!
DV_TOPO
  ID_NAME        = {self._name}
  EL_GROUP       = {self._variables}
END_
"""
