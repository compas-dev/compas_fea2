from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.constraints import OptimisationConstraint


class AnsysOptimisationConstraint(OptimisationConstraint):
    """ Ansys implementation of :class:`.OptimisationConstraint`.\n
    """
    __doc__ += OptimisationConstraint.__doc__

    def __init__(self, design_response, relative=False, name=None, **kwargs):
        super(AnsysOptimisationConstraint, self).__init__(
            design_response=design_response, relative=relative, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
