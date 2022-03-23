import importlib
from pathlib import Path
from compas_fea2.optimisation.problem import TopOptSensitivity
from compas_fea2.backends.abaqus.job.input_file import AbaqusParametersFile
from compas_fea2.backends.abaqus.job.input_file import AbaqusInputFile
from compas_fea2.backends.abaqus.job.send_job import launch_optimisation


class AbaqusTopOptSensitivity(TopOptSensitivity):

    def __init__(self, problem, design_variables, vf, lc='ALL,ALL,All', **kwargs):
        super().__init__(problem, design_variables, vf, lc, **kwargs)

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
