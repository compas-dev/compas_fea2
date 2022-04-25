from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.problem import Problem

class AnsysProblem(Problem):
    """ Ansys implementation of :class:`.Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, model, name=None, author=None, description=None, **kwargs):
        super(AnsysProblem, self).__init__(model=model, name=name, author=author, description=description, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

