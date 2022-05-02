from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

from dataclasses import dataclass

# NOTE check here: https://abaqus-docs.mit.edu/2017/English/TsoCmdMap/tso-r-cmd-optParam.htm


class OptimisationParameters(FEAData):
    """Parameters for the optimisation.

    Parameters
    ----------
    optimisation_task_name : str
        reference to the optimisation task name.
    auto_frozen :  str
        automatically removes the elements with applied loads from the optimisation variables.

    """

    def __init__(self, name=None):
        super(OptimisationParameters, self).__init__(name=name)
        self.optimisation_task_name: str = None  #: reference to the optimisation task name
        self.auto_frozen: str = None  #: automatically removes the elements with applied loads from the optimisation variables
        self.density_update: str = None
        self.density_lower: str = None
        self.density_upper: str = None
        self.density_move: str = None
        self.mat_penalty: str = None
        self.stop_criterion_level: str = None
        self.stop_criterion_obj: str = None
        self.stop_criterion_density: str = None
        self.stop_criterion_iter: str = None
        self.sum_q_factor: str = None
        self.name: str = 'Parameters'
        self.iter_max: str = 50


class SmoothingParameters(FEAData):
    """Parameters for the postprocess of the optimisation results.

    Note
    ----
    Check `here <https://help.3ds.com/2021/english/dssimulia_established/TsoCmdMap/tso-r-cmd-smooth.htm?contextscope=all&id=bf76aa40b0cf490c9956162db0f11695>`_.

    Parameters
    ----------
    task : str
        type of smoothing.

        - ``iso`` : Isosurface of a topology optimization result.
        - ``surface`` : Surface of the initial model or the result of shape or bead optimization.

    all : bool
        if ``True``, postprocess all iterations.
    iso_value : float
        Isovalue; is used to determine the positions on the element
        edges where the new nodes are created. Larger values lead to models with
        smaller volume. Not used if ``tast = surface``. Value between 0 and 1.
    smooth_cycles : int
        Number of smoothing cycles: if set to 0, no smoothing is performed.
        Larger values lead to smoother models, but might cause the narrowing
        of thin components. Not used if `task = surface`. Nonnegative integer value.
    """

    def __init__(self, name=None):
        super().__init__(name=name)
        self.task: str = None
        self.all: bool = None
        self.iso_value: float = None
        self.smooth_cycles: int = None
