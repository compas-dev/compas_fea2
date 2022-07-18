from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# TODO remove dataclasses
from dataclasses import dataclass
from compas_fea2.optimisation.parameters import OptimisationParameters, SmoothingParameters


@dataclass
class AbaqusOptimisationParameters(OptimisationParameters):

    def _generate_jobdata(self, opti_problem_name):
        return f"""!
OPT_PARAM
  ID_NAME = optimisation_parameters
  OPTIMIZE = {opti_problem_name}
  AUTO_FROZEN = {self.auto_frozen or 'LOAD'}
  DENSITY_UPDATE = {self.density_update or 'NORMAL'}
  DENSITY_LOWER = {self.density_lower or 0.001}
  DENSITY_UPPER = {self.density_upper or 1.}
  DENSITY_MOVE = {self.density_move or 0.25}
  MAT_PENALTY = {self.mat_penalty or 3}
  STOP_CRITERION_LEVEL = {self.stop_criterion_level or 'BOTH'}
  STOP_CRITERION_OBJ = {self.stop_criterion_obj or 0.001}
  STOP_CRITERION_DENSITY = {self.stop_criterion_density or 0.005}
  STOP_CRITERION_ITER = {self.stop_criterion_iter or 4}
  SUM_Q_FACTOR = {self.sum_q_factor or 6.}
END_
! Stop
STOP
  ID_NAME        = global_stop
  ITER_MAX       = {self.iter_max}
END_
"""


@dataclass
class AbaqusSmoothingParameters(SmoothingParameters):

    def _generate_jobdata(self):
        return f"""!
SMOOTH
  id_name = ISO_SMOOTHING_0_3
  task = {'ALL_ITERATIONS' if self.all else self.task}
  iso_value = {self.iso_value or 0.3}
  SELF_INTERSECTION_CHECK = runtime
  smooth_cycles = {self.smooth_cycles or 10}
  reduction_rate = 60
  reduction_angle = 5.0
  format = stl
END_
"""
