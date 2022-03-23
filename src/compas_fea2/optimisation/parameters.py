from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

from dataclasses import dataclass

# NOTE check here: https://abaqus-docs.mit.edu/2017/English/TsoCmdMap/tso-r-cmd-optParam.htm


@dataclass
class OptimisationParameters():
    """Parameters for the optimisation.

    Args:
        optimisation_task_name (str): reference to the optimisation task name.
        auto_frozen (str): automatically removes the elements with applied loads from the optimisation variables.

    """
    optimisation_task_name: str = None  #: reference to the optimisation task name
    auto_frozen: str = None  #: automatically removes the elements with applied loads from the optimisation variables
    density_update: str = None
    density_lower: str = None
    density_upper: str = None
    density_move: str = None
    mat_penalty: str = None
    stop_criterion_level: str = None
    stop_criterion_obj: str = None
    stop_criterion_density: str = None
    stop_criterion_iter: str = None
    sum_q_factor: str = None
    name: str = 'Parameters'
    iter_max: str = 50


@dataclass
class SmoothingParameters():
    """Parameters for the postprocess of the optimisation results.

    Note
    ----
    Check `here <https://help.3ds.com/2021/english/dssimulia_established/TsoCmdMap/tso-r-cmd-smooth.htm?contextscope=all&id=bf76aa40b0cf490c9956162db0f11695>`_.


    Args:
        task (str): type of smoothing.

            - ``iso`` : Isosurface of a topology optimization result.
            - ``surface`` : Surface of the initial model or the result of shape or bead optimization.

        all (bool): if ``True``, postprocess all iterations.
        iso_value (float): Isovalue; is used to determine the positions on the element
            edges where the new nodes are created. Larger values lead to models with
            smaller volume. Not used if ``tast = surface``. Value between 0 and 1.
        smooth_cycles (int) : Number of smoothing cycles: if set to 0, no smoothing is performed.
            Larger values lead to smoother models, but might cause the narrowing
            of thin components. Not used if `task = surface`. Nonnegative integer value.
    """
    task: str
    all: bool
    iso_value: float
    smooth_cycles: int
