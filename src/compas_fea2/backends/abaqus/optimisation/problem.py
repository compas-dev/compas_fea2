from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from compas_fea2.optimisation.problem import TopOptSensitivity
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process


class AbaqusTopOptSensitivity(TopOptSensitivity):
    """Abaqus implementation of :class:`TopOptSensitivity`\n"""
    __doc__ += TopOptSensitivity.__doc__

    def __init__(self, problem, design_variables, vf, lc='ALL,ALL,All', name=None, **kwargs):
        super(AbaqusTopOptSensitivity).__init__(problem, design_variables, vf, lc, name=name, **kwargs)

    def _generate_jobdata(self):
        return f"""!
OPTIMIZE
  ID_NAME        = {self._name}
  DV             = {self._design_variables._name}
  OBJ_FUNC       = {self._objective_function._name}
  CONSTRAINT     = {self._constraints['vf']._name}
  STRATEGY       = {self._strategy}
END_
"""

    @timer(message='Optimisation completed in')
    def solve(self, path, cpus=1, output=True, overwrite=True, save=False):
        """ Run the topology optimisation through Tosca.

        Note
        ----
        https://abaqus-docs.mit.edu/2017/English/TsoUserMap/tso-c-usr-control-start-commandLine.htm
        http://194.167.201.93/English/TsoUserMap/tso-c-usr-control-tp-cmdline.htm#tso-c-usr-control-tp-cmdline

        Parameters
        ----------
        problem : obj
            :class:`OptimisationProblem` subclass object.
        output : bool
            Print terminal output.

        Returns
        -------
        None

        """
        super().solve(path, save)

        if overwrite:
            raise NotImplementedError
            overwrite_kw = 'ask_delete=OFF'

        # cmd = f'cd {self.path} && abaqus optimization task=c:/code/myrepos/from_compas/fea2/temp/topopt_hypar_gmsh/hypar.par job=c:/temp/test_opt interactive'
        cmd = 'cd {} && ToscaStructure --job {} -scpus {} --loglevel NOTICE --solver abaqus --ow'.format(
            self._path, self._name, cpus)
        for line in launch_process(cmd_args=cmd, cwd=self.path, output=output):
            print(line)

    def smooth_optimisation(self, output):
        raise NotImplementedError
