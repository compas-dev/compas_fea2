from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.problem import TopOptSensitivity


class OpenseesTopOptSensitivity(TopOptSensitivity):

    def __init__(self, problem, design_variables, vf, lc='ALL,ALL,All', name=None, **kwargs):
        super(OpenseesTopOptSensitivity, self).__init__(problem, design_variables, vf, lc, name=name, **kwargs)
        raise NotImplementedError
