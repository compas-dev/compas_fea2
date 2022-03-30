from pathlib import Path
from compas_fea2.problem import Problem


class OpenseesProblem(Problem):
    """OpenSees implementation of the :class:`Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, model, author=None, description=None, **kwargs):
        super(OpenseesProblem, self).__init__(model=model, author=author, description=description, **kwargs)

    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    # =========================================================================
    #                         Results methods
    # =========================================================================
