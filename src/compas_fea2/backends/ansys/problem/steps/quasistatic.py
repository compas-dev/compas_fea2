from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps.quasistatic import DirectCyclicStep
from compas_fea2.problem.steps.quasistatic import QuasiStaticStep


class AnsysDirectCyclicStep(DirectCyclicStep):
    """ Ansys implementation of :class:`.DirectCyclicStep`.\n
    """
    __doc__ += DirectCyclicStep.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysDirectCyclicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysQuasiStaticStep(QuasiStaticStep):
    """ Ansys implementation of :class:`.QuasiStaticStep`.\n
    """
    __doc__ += QuasiStaticStep.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysQuasiStaticStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
