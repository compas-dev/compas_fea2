from compas_fea2.optimisation.variables import DesignVariables


class AbaqusDesignVariables(DesignVariables):
    def __init__(self, name, variables) -> None:
        super().__init__(name, variables)

    def _generate_jobdata(self):
        return f"""!
DV_TOPO
  ID_NAME        = {self._name}
  EL_GROUP       = {self._variables}
END_
"""
