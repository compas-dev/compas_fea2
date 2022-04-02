from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import QuasiStaticStep
from compas_fea2.problem import DirectCyclicStep


class OpenseesQuasiStaticStep(QuasiStaticStep):
    def __init__(self, name=None, **kwargs):
        super(OpenseesQuasiStaticStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError()


class OpenseesDirectCyclicStep(DirectCyclicStep):
    def __init__(self, name=None, **kwargs):
        super(OpenseesDirectCyclicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError()
