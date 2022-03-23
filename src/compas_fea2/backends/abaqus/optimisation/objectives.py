from compas_fea2.optimisation.objectives import ObjectiveFunction


class AbaqusObjectiveFunction(ObjectiveFunction):
    def __init__(self, name, design_respone, target) -> None:
        super().__init__(name, design_respone, target)

    def _generate_jobdata(self):
        return f"""!
OBJ_FUNC
  ID_NAME        = {self._name}
  TARGET         = {self._target}
  DRESP          = {self._design_response._name}, , {self._design_response._name}
END_
"""
