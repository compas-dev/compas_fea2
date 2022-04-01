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

    def write_parameters_file(self, output=True):
        """Writes the abaqus parameters file for the optimisation.

        Parameters
        ----------
        output : bool
            Print terminal output.

        Returns
        -------
        None
        """
        par_file = AbaqusParametersFile(self)
        par = par_file.write_to_file(self.path)
        if output:
            print(par)

    # TODO: try to make this an abstract method of the base class
    # TODO: add cpu parallelization option. Parallel execution requested but no parallel feature present in the setup

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

        self.write_input_file(self.path, output)
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
