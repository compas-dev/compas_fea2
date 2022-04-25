from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.constraints import OptimisationConstraint


class OpenseesOptimisationConstraint(OptimisationConstraint):
    def __init__(self, design_response, relative=False, name=None, **kwargs):
        super(OpenseesOptimisationConstraint, self).__init__(design_response, relative, name=name, **kwargs)
        raise NotADirectoryError()
