import importlib
from pathlib import Path
from compas_fea2._base.optimisation.problem import TopOptSensitivityBase
from compas_fea2.backends.abaqus.job.input_file import ParametersFile
from compas_fea2.backends.abaqus.job.input_file import InputFile
from compas_fea2.backends.abaqus.job.send_job import launch_optimisation


class TopOptSensitivity(TopOptSensitivityBase):

    def __init__(self, problem, design_variables, vf, lc='ALL,ALL,All', **kwargs):
        super().__init__(problem, design_variables, vf, lc, **kwargs)

    def write_parameters_file(self, path, output, smooth):
        """Writes the abaqus parameters file for the optimisation.

        Parameters
        ----------
        path : str, path
            path to the folder where the file will be written
        output : bool
            Print terminal output.

        Returns
        -------
        None
        """
        par_file = ParametersFile.from_problem(self, smooth)
        par = par_file.write_to_file(path)
        if output:
            print(par)

    def solve(self, path='C:/temp', cpus=1, output=True, save=False, smooth=None):
        """Run Topology Optimisation procedure

        Warning
        -------
        ToscaStructure cannot read a model made of parts and assemblies. The model
        is automatically flatten and in case of incompatibilities, the names of
        nodes, elements and groups are automatically changed by the software. Check
        the input file automatically generated in the optimisation folder.

        Parameters
        ----------
        path : str, optional
            folder location where the optimisation results will be saved, by default 'C:/temp'
        cpus : int
            number of cpus used by the solver.
        output : bool, optional
            if ``True`` provides detailed output in the terminal, by default True
        save : bool, optional
            save results, by default False. CURRENTLY NOT IMPLEMENTED!
        smooth : obj, optional
            if a :class:`SmoothingParametersBase` subclass object is passed, the
            optimisation results will be postprocessed and smoothed, by defaut
            ``None`` (no smoothing)
        """
        self._path = path if isinstance(path, Path) else Path(path)
        self._problem._path = self._path
        if not self._path.exists():
            self._path.mkdir()
        if save:
            raise NotImplementedError()
        self._problem.write_input_file(output)
        self.write_parameters_file(self._path, output, smooth)
        launch_optimisation(self, cpus, output)

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
