from compas_fea2.problem import Problem

from compas_fea2.backends.abaqus.job import launch_process
from compas_fea2.backends.abaqus.job import launch_optimisation
from compas_fea2.utilities._utils import timer


class AbaqusProblem(Problem):
    """Abaqus implementation of :class:`Problem`.\n"""
    __doc__ += Problem.__doc__

    def __init__(self, model, author=None, description=None, **kwargs):
        super(AbaqusProblem, self).__init__(model=model, author=author, description=description, **kwargs)

    # =========================================================================
    #                         Analysis methods
    # =========================================================================
    @timer(message='Analysis completed in')
    def analyse(self, path, exe=None, cpus=1, output=True, overwrite=True, save=False):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str
            Path to the folder where the input file is saved.
        exe : str, optional
            Full terminal command to bypass subprocess defaults, by default ``None``.
        cpus : int, optional
            Number of CPU cores to use, by default ``1``.
        output : bool, optional
            Print terminal output, by default ``True``.
        save : bool, optional
            Save structure to .cfp before the analysis, by default ``False``.
        overwrite : bool, optional
            Overwrite existing analysis files, by default ``True``.

        Returns
        -------
        None

        """
        super().analyse(path, save)
        launch_process(self, exe=exe, output=output, overwrite=overwrite, cpus=cpus)

    # =============================================================================
    #                               Job data
    # =============================================================================
    @timer(message='Problem generated in ')
    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return '\n'.join([step._generate_jobdata() for step in self.steps])
