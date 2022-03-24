from pathlib import Path
from compas_fea2.problem import Problem


class Problem(Problem):
    """OpenSees implementation of the :class:`Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, name, model, author=None, description=None):
        super(Problem, self).__init__(name=name, model=model, author=author, description=description)

    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    # =========================================================================
    #                         Results methods
    # =========================================================================
