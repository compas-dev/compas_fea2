from pathlib import Path
from compas_fea2.problem import Problem

from compas_fea2.backends.abaqus.job import AbaqusInputFile
from compas_fea2.backends.abaqus.job import AbaqusParametersFile
from compas_fea2.backends.abaqus.job import launch_process
from compas_fea2.backends.abaqus.job import launch_optimisation


class AbaqusProblem(Problem):
    """Abaqus implementation of the Problem class.

    """
    __doc__ += Problem.__doc__

    def __init__(self, model, author=None, description=None, **kwargs):
        super(AbaqusProblem, self).__init__(model=model, author=author, description=description, **kwargs)

    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    # TODO move to the base class and change to **kwargs
    def set_optimisation_parameters(self, vf, iter_max, cpus):
        self.vf = vf
        self.iter_max = iter_max
        self.cpus = cpus

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    # TODO: try to make this an abstract method of the base class
    # TODO: add cpu parallelization option. Parallel execution requested but no parallel feature present in the setup

    def analyse(self, path, exe=None, cpus=1, output=True, overwrite=True, save=False):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str
            Path to the folder where the input file is saved.
        exe : str, optional
            Full terminal command to bypass subprocess defaults, by default ``None``.
        cpus : int, optional
            Number of CPU cores to use, , by default ``1``.
        output : bool, optional
            Print terminal output, by default ``True``.
        save : bool, optional
            Save structure to .cfp before the analysis, by default ``False``.

        Returns
        -------
        None

        """
        super().analyse(path, save)
        launch_process(self, exe, output, overwrite)

    def optimise(self, path='C:/temp', output=True, save=False):
        super().optimise(path, save)
        launch_optimisation(self, output)

    # =============================================================================
    #                               Job data
    # =============================================================================

    def _generate_jobdata(self):
        return f"""{self._generate_steps_section()}"""

    def _generate_steps_section(self):
        """Generate the content relatitive to the steps section for the input
        file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for step in self.steps:
            section_data.append(step._generate_jobdata())

        return ''.join(section_data)
