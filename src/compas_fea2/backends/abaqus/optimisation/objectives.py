from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.objectives import ObjectiveFunction


class AbaqusObjectiveFunction(ObjectiveFunction):
    def __init__(self, design_respone, target, name=None, **kwargs) -> None:
        super(AbaqusObjectiveFunction, self).__init__(name, design_respone, target, name=name, **kwargs)

    def _generate_jobdata(self):
        return f"""!
OBJ_FUNC
  ID_NAME        = {self._name}
  TARGET         = {self._target}
  DRESP          = {self._design_response._name}, , {self._design_response._name}
END_
"""
