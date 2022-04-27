from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.parameters import OptimisationParameters
from compas_fea2.optimisation.parameters import SmoothingParameters


class AnsysOptimisationParameters(OptimisationParameters):
    """ Ansys implementation of :class:`.OptimisationParameters`.\n
    """
    __doc__ += OptimisationParameters.__doc__

    def __init__(self, optimisation_task_name: str = None, auto_frozen: str = None, density_update: str = None, density_lower: str = None, density_upper: str = None, density_move: str = None, mat_penalty: str = None, stop_criterion_level: str = None, stop_criterion_obj: str = None, stop_criterion_density: str = None, stop_criterion_iter: str = None, sum_q_factor: str = None, name: str = 'Parameters', iter_max: str = 50) -> None:
        super(AnsysOptimisationParameters, self).__init__(optimisation_task_name=optimisation_task_name, auto_frozen=auto_frozen, density_update=density_update, density_lower=density_lower, density_upper=density_upper, density_move=density_move,
                                                          mat_penalty=mat_penalty, stop_criterion_level=stop_criterion_level, stop_criterion_obj=stop_criterion_obj, stop_criterion_density=stop_criterion_density, stop_criterion_iter=stop_criterion_iter, sum_q_factor=sum_q_factor, name=name, iter_max=iter_max)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysSmoothingParameters(SmoothingParameters):
    """ Ansys implementation of :class:`.SmoothingParameters`.\n
    """
    __doc__ += SmoothingParameters.__doc__

    def __init__(self, task: str, all: bool, iso_value: float, smooth_cycles: int) -> None:
        super(AnsysSmoothingParameters, self).__init__(
            task=task, all=all, iso_value=iso_value, smooth_cycles=smooth_cycles)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
