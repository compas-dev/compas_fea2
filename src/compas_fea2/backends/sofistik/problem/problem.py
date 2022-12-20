from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess

from compas_fea2.problem.problem import Problem
from compas_fea2.problem import _Step

from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process
from compas_fea2.backends.sofistik import SOFISTIK_PATH

class SofistikProblem(Problem):
    """Sofistik implementation of :class:`compas_fea2.problem.problem.Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, name=None, description=None, **kwargs):
        super(SofistikProblem, self).__init__(name=name, description=description, **kwargs)

    def _generate_jobdata(self):
        return """
$ STEPS
{}

$ ANALYSIS
+prog ase
head analysis
syst prob line
lc no 1000  titl 'linear analysis test load'
lcc no 1  fact 1.0
end

+prog aqb
head stresses
stre
lc 1000
beam type beam
end
        """.format('\n'.join([step._generate_jobdata() for step in self.steps]))


    @timer(message='Analysis completed in')
    def analyse(self, path, shell=True, exe=None, verbose=False, *args, **kwargs):
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
        path = self._check_analysis_path(path)
        input_file = self.write_input_file(path)

        sofistik_path = exe or SOFISTIK_PATH
        solver = "sps.exe" if shell else "wps.exe"
        solver_path = os.path.join(sofistik_path, solver)

        popenargs = [solver_path, input_file.path]
        if verbose:
            popenargs.append("-b")
        process = subprocess.run(popenargs)
        return process.returncode



