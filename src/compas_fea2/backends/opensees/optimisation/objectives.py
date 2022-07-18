from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.objectives import ObjectiveFunction


class OpenseesObjectiveFunction(ObjectiveFunction):
    def __init__(self, design_respone, target, name=None, **kwargs):
        super(OpenseesObjectiveFunction, self).__init__(design_respone, target, name=name, **kwargs)
        raise NotImplementedError
