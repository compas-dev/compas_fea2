from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.objectives import ObjectiveFunction

class AnsysObjectiveFunction(ObjectiveFunction):
    """Ansys implementation of :class:`compas_fea2.optimisation.objectives.ObjectiveFunction`.\n
    """
    __doc__ += ObjectiveFunction.__doc__

    def __init__(self, design_response, target, name=None, **kwargs):
        super(AnsysObjectiveFunction, self).__init__(design_response=design_response, target=target, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

