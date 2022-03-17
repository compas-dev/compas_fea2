from pathlib import Path
from compas_fea2.problem import ProblemBase


class Problem(ProblemBase):
    """OpenSees implementation of the :class:`ProblemBase`.\n
    """
    __doc__ += ProblemBase.__doc__

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
