from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from compas_fea2.optimisation.problem import TopOptSensitivity
from compas_fea2.backends.abaqus.job.send_job import launch_optimisation


class AbaqusTopOptSensitivity(TopOptSensitivity):
    """Abaqus implementation of :class:`TopOptSensitivity`\n"""
    __doc__ += TopOptSensitivity.__doc__

    def __init__(self, problem, design_variables, vf, lc='ALL,ALL,All', name=None, **kwargs):
        super(AbaqusTopOptSensitivity).__init__(problem, design_variables, vf, lc, name=name, **kwargs)

    def _generate_jobdata(self):
        return f"""!
OPTIMIZE
  ID_NAME        = {self._name}
  DV             = {self._design_variables._name}
  OBJ_FUNC       = {self._objective_function._name}
  CONSTRAINT     = {self._constraints['vf']._name}
  STRATEGY       = {self._strategy}
END_
"""

    def solve(self, path='C:/temp', output=True, save=False):
        super().solve(path, save)
        launch_optimisation(self, output)
