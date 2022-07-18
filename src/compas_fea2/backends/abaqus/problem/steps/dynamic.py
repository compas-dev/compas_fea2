from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import DynamicStep


class AbaqusDynamicStep(DynamicStep):
    def __init__(self, name=None, **kwargs):
        super(AbaqusDynamicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError
