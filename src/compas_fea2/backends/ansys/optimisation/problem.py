from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.problem import OptimisationProblem
from compas_fea2.optimisation.problem import TopOptController
from compas_fea2.optimisation.problem import TopOptSensitivity


class AnsysOptimisationProblem(OptimisationProblem):
    """ Ansys implementation of :class:`.OptimisationProblem`.\n
    """
    __doc__ += OptimisationProblem.__doc__

    def __init__(self, problem, design_variables, design_responses, objective_function, dv_constraints, constraints, strategy, parameters, name=None, **kwargs):
        super(AnsysOptimisationProblem, self).__init__(problem=problem, design_variables=design_variables, design_responses=design_responses,
                                                       objective_function=objective_function, dv_constraints=dv_constraints, constraints=constraints, strategy=strategy, parameters=parameters, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysTopOptController(TopOptController):
    """ Ansys implementation of :class:`.TopOptController`.\n
    """
    __doc__ += TopOptController.__doc__

    def __init__(self, problem, design_variables, design_responses, objective_function, dv_constraints, constraints, strategy, parameters, name=None, **kwargs):
        super(AnsysTopOptController, self).__init__(problem=problem, design_variables=design_variables, design_responses=design_responses,
                                                    objective_function=objective_function, dv_constraints=dv_constraints, constraints=constraints, strategy=strategy, parameters=parameters, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysTopOptSensitivity(TopOptSensitivity):
    """ Ansys implementation of :class:`.TopOptSensitivity`.\n
    """
    __doc__ += TopOptSensitivity.__doc__

    def __init__(self, problem, design_variables, vf, lc, **kwargs):
        super(AnsysTopOptSensitivity, self).__init__(problem=problem,
                                                     design_variables=design_variables, vf=vf, lc=lc, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
