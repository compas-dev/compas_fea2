from compas_fea2.problem import Problem

# from compas_fea2.backends.abaqus.job import launch_process
# from compas_fea2.backends.abaqus.job import launch_optimisation
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process


class AbaqusProblem(Problem):
    """Abaqus implementation of :class:`Problem`.\n"""
    __doc__ += Problem.__doc__

    def __init__(self, model, author=None, description=None, **kwargs):
        super(AbaqusProblem, self).__init__(model=model, author=author, description=description, **kwargs)

    # =========================================================================
    #                         Analysis methods
    # =========================================================================
    @timer(message='Analysis completed in')
    def analyse(self, path, exe=None, cpus=1, output=True, overwrite=True, save=False, user_mat=None):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str, :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.
        save : bool
            Save structure to .cfp before the analysis.
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
        self.write_input_file(path)
        if save:
            raise NotImplementedError

        # Set options
        overwrite_kw = ''
        user_sub_kw = ''
        exe_kw = 'abaqus'
        if overwrite:
            overwrite_kw = 'ask_delete=OFF'
        if user_mat:
            raise NotImplementedError
            umat_path = problem.materials[user_mat].sub_path
            user_sub_kw = 'user={}'.format(umat_path)
        if exe:
            raise NotADirectoryError
            exe_kw = exe

        # Analyse
        cmd = 'cd {} && {} {} cpus={} job={} interactive resultsformat=odb {}'.format(
            self.path, exe_kw, user_sub_kw, cpus, self.name, overwrite_kw)
        for line in launch_process(cmd_args=cmd, cwd=self.path, output=output):
            print(line)

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
        return '\n'.join([step._generate_jobdata() for step in self._steps_order])
