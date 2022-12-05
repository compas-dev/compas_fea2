import os
from pathlib import Path
from compas_fea2.problem import Problem
from compas_fea2.problem import _Step

from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process

from compas_fea2.backends.abaqus.results import odb_extract
from compas_fea2.backends.abaqus.job.input_file import AbaqusInputFile, AbaqusRestartInputFile


class AbaqusProblem(Problem):
    """Abaqus implementation of :class:`Problem`.\n"""
    __doc__ += Problem.__doc__

    def __init__(self, name=None, description=None, **kwargs):
        super(AbaqusProblem, self).__init__(name=name, description=description, **kwargs)

    # =========================================================================
    #                         Analysis methods
    # =========================================================================
    def _build_command(self, path, name, **kwargs):
        # Set options
        option_keywords = []
        overwrite_kw = ''
        user_sub_kw = ''
        exe_kw = 'abaqus'
        if kwargs.get('overwrite', None):
            option_keywords.append('ask_delete=OFF')
        if kwargs.get('user_mat', None):
            raise NotImplementedError
            umat_path = problem.materials[user_mat].sub_path
            user_sub_kw = 'user={}'.format(umat_path)
        if kwargs.get('exe', None):
            raise NotImplementedError()
            raise NotADirectoryError()
            exe_kw = exe
        if kwargs.get('oldjob', None):
            option_keywords.append('oldjob={}'.format(kwargs['oldjob']))
        if kwargs.get('cpus', None):
            option_keywords.append('cpus={}'.format(kwargs['cpus']))

        return 'cd {} && abaqus job={} interactive resultsformat=odb {}'.format(
            path, name, ' '.join(option_keywords))
        # return 'cd {} && {} {} cpus={} job={} interactive resultsformat=odb {}'.format(
        #     path, exe_kw, user_sub_kw, cpus, name, overwrite_kw)

    @timer(message='Finished writing input file in')
    def write_restart_file(self, path, start, steps):
        # type: (str, float, list(_Step)) -> AbaqusRestartInputFile
        """Writes the abaqus input file.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.
        restart : dict
            parameters for the restart option

        Returns
        -------
        None
        """
        if not path.exists():
            raise ValueError("No analysis results found for {!r}".format(self))
        restart_file = AbaqusRestartInputFile.from_problem(problem=self, start=start, steps=steps)
        restart_file.write_to_file(self.path)
        return restart_file

    @timer(message='Analysis completed in')
    def analyse(self, path, exe=None, cpus=1, verbose=False, overwrite=True, user_mat=None, *args, **kwargs):
        """Runs the analysis through abaqus.

        Parameters
        ----------
        path : str, :class:`pathlib.Path`
            Path to the analysis folder. A new folder with the name
            of the problem will be created at this location for all the required
            analysis files.
        save : bool
            Save structure to .cfp before the analysis.
        exe : str, optional
            Full terminal command to bypass subprocess defaults, by default ``None``.
        cpus : int, optional
            Number of CPU cores to use, by default ``1``.
        output : bool, optional
            Print terminal output, by default ``True``.
        overwrite : bool, optional
            Overwrite existing analysis files, by default ``True``.
        restart : bool, optional
            If `True`, save additional files for restarting the analysis later,
            by default `False`

        Returns
        -------
        None

        """
        print('\nBegin the analysis...')
        self._check_analysis_path(path)
        self.write_input_file()
        cmd = self._build_command(overwrite=overwrite, user_mat=user_mat, exe=exe,
                                  path=self.path, name=self.name, cpus=cpus)
        for line in launch_process(cmd_args=cmd, cwd=self.path, verbose=verbose):
            print(line)

    @timer(message='Analysis completed in')
    def restart_analysis(self, start, steps, exe=None, cpus=1, output=True, overwrite=True):
        # type: (Problem, float, list(_Step), str, int, bool, bool) -> None
        """Runs the analysis through abaqus.

        Parameters
        ----------
        start : float
            Time-step increment.
        steps : [:class:`compas_fea2.problem.Step`]
            List of steps to add to the orignal problem.
        exe : str, optional
            Full terminal command to bypass subprocess defaults, by default ``None``.
        cpus : int, optional
            Number of CPU cores to use, by default ``1``.
        output : bool, optional
            Print terminal output, by default ``True``.
        overwrite : bool, optional
            Overwrite existing analysis files, by default ``True``.

        Returns
        -------
        None

        """
        if not self.path:
            raise AttributeError('No analysis path found! Are you sure you analysed this problem?')
        restart_file = self.write_restart_file(path=self.path, start=start, steps=steps)
        cmd = self._build_command(overwrite=overwrite, user_mat=None, exe=exe,
                                  path=self.path, name=restart_file._job_name, cpus=cpus, oldjob=self.name)
        print('\n\n*** RESTARTING PREVIOUS JOB ***\n')
        for line in launch_process(cmd_args=cmd, cwd=self.path, verbose=output):
            print(line)

    @timer(message='Analysis and extraction completed in')
    def analyse_and_extract(self, path, exe=None, cpus=1, output=True, overwrite=True, user_mat=None, fields=None, *args, **kwargs):
        """_summary_

        Parameters
        ----------
        path : _type_
            _description_
        exe : _type_, optional
            _description_, by default None
        cpus : int, optional
            _description_, by default 1
        output : bool, optional
            _description_, by default True
        overwrite : bool, optional
            _description_, by default True
        user_mat : _type_, optional
            _description_, by default None
        database_path : _type_, optional
            _description_, by default None
        database_name : _type_, optional
            _description_, by default None
        fields : [str], optional
            Output fields to extract from the odb file, by default None, which
            means that all available fields are extracted.

        Returns
        -------
        _type_
            _description_
        """
        self.analyse(path, exe=exe, cpus=cpus, verbose=output, overwrite=overwrite, user_mat=user_mat)
        return self.convert_results_to_sqlite(fields=fields)

    # ==========================================================================
    # Extract results
    # ==========================================================================
    @timer(message='Data extracted from Abaqus .odb file in')
    def convert_results_to_sqlite(self, database_path=None, database_name=None, fields=None):
        """Extract data from the Abaqus .odb file and store into a SQLite database.

        Parameters
        ----------
        fields : list
            Output fields to extract, by default 'None'. If `None` all available
            fields will be extracted, which might require considerable time.

        Returns
        -------
        None

        """
        print('\nExtracting data from Abaqus .odb file...')
        database_path = database_path or self.path
        database_name = database_name or self.name
        args = ['abaqus', 'python', Path(odb_extract.__file__), ','.join(fields) if fields else 'None',
                database_path, database_name]
        for line in launch_process(cmd_args=args, cwd=database_path, verbose=True):
            print(line)

        return Path(database_path).joinpath('{}-results.db'.format(database_name))

    @timer(message='Data extracted from Abaqus .odb file in')
    def convert_results_to_json(self, database_path=None, database_name=None, fields=None):
        """Extract data from the Abaqus .odb file.

        Parameters
        ----------
        fields : list
            Output fields to extract, by default 'None'. If `None` all available
            fields will be extracted, which might require considerable time.

        Note
        ----
        The results are serialized according to the following schema:
        {
            Step1:{Part1:{"nodes":{nodekey1:{field1: value1,
                                              field2: value2,
                                              ..},
                                      nodekey2:{...},
                                      ...
                                    },
                           "elements":{elementkey1:{field1: value1,
                                                    field2: value2,
                                                    ...},
                                       elementkey2:{...},
                                       ...
                                       }
                           },
                     Part2:{...},
                     ...
                     },
            Step2:{...},
            ...
        }

        Returns
        -------
        None

        """
        raise NotImplementedError()
        print('\nExtracting data from Abaqus .odb file...')
        database_path = database_path or self.path
        database_name = database_name or self.name
        args = ['abaqus', 'python', Path(odb_extract.__file__), ','.join(fields) if fields else 'None',
                database_path, database_name]
        for line in launch_process(cmd_args=args, cwd=database_path, verbose=True):
            print(line)

        return Path(database_path).joinpath('{}-results.db'.format(database_name))

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
