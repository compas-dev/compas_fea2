from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps.dynamic import DynamicStep


class AnsysDynamicStep(DynamicStep):
    """ Ansys implementation of :class:`.DynamicStep`.\n
    """
    __doc__ += DynamicStep.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysDynamicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
