from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from compas_fea2.problem import ProblemBase

from compas_fea2.backends.abaqus.job.input_file import InputFile
from compas_fea2.backends.abaqus.job.input_file import ParFile
from compas_fea2.backends.abaqus.job.send_job import launch_process
from compas_fea2.backends.abaqus.job.send_job import launch_optimisation
from compas_fea2.backends.abaqus.problem.outputs import FieldOutput
from compas_fea2.backends.abaqus.problem.outputs import HistoryOutput

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Problem',
]


class Problem(ProblemBase):
    """Initialises the Problem object.

    Parameters
    ----------
    name : str
        Name of the Structure.
    model : obj
        model object.
    """

    def __init__(self, name, model):
        super(Problem, self).__init__(name=name, model=model)

    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    # =========================================================================
    #                         Results methods
    # =========================================================================
