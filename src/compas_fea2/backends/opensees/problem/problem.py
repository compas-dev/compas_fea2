from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from compas_fea2.backends._base.problem import ProblemBase

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

    # TODO: try to make this an abstract method of the base class

    def analyse(self, path='C:/temp', exe=None, cpus=1, output=True, overwrite=True, user_mat=False, save=False):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str
            Path to the folder where the input file is saved.
        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        output : bool
            Print terminal output.
        user_mat : str TODO: REMOVE!
            Name of the material defined through a subroutine (currently only one material is supported)
        save : bool
            Save structure to .cfp before file writing.

        Returns
        -------
        None

        """
        self.path = path if isinstance(path, Path) else Path(path)
        if not self.path.exists():
            self.path.mkdir()

        if save:
            self.save_to_cfp()

        self.write_input_file(output)
        launch_process(self, exe, output, overwrite, user_mat)

    def optimise(self, path='C:/temp', output=True, save=False):
        self.path = path if isinstance(path, Path) else Path(path)
        if not self.path.exists():
            self.path.mkdir()

        if save:
            self.save_to_cfp()

        self.write_input_file(output)
        self.write_parameters_file(output)
        launch_optimisation(self, output)

    # =========================================================================
    #                         Results methods
    # =========================================================================
