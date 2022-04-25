from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from compas_fea2.problem import Problem


class OpenseesProblem(Problem):
    """OpenSees implementation of the :class:`Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, model, author=None, description=None, **kwargs):
        super(OpenseesProblem, self).__init__(model=model, author=author, description=description, **kwargs)
        # FIXME move these to the Steps
        self.tolerance = None
        self.iterations = None
        self.increments = None  # self.increments =1./increments
    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    # =========================================================================
    #                         Results methods
    # =========================================================================
