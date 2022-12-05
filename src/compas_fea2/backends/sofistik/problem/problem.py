from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.problem import Problem

class SofistikProblem(Problem):
    """Sofistik implementation of :class:`compas_fea2.problem.problem.Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, name=None, description=None, **kwargs):
        super(SofistikProblem, self).__init__(name=name, description=description, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

