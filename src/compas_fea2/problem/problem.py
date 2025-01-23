from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path

from compas_fea2.base import FEAData
from compas_fea2.job.input_file import InputFile
from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import Step
from compas_fea2.results.database import ResultsDatabase

from compas_fea2.UI.viewer import FEA2Viewer


class Problem(FEAData):
    """A Problem is a collection of analysis steps (:class:`compas_fea2.problem._Step)
    applied in a specific sequence.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    describption : str, optional
        Brief description of the Problem, , by default ``None``.
        This will be added to the input file and can be useful for future reference.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    model : :class:`compas_fea2.model.Model`
        Model object to analyse.
    describption : str
        Brief description of the Problem. This will be added to the input file and
        can be useful for future reference.
    steps : list of :class:`compas_fea2.problem._Step`
        list of analysis steps in the order they are applied.
    path : str, :class:`pathlib.Path`
        Path to the analysis folder where all the files will be saved.
    path_db : str, :class:`pathlib.Path`
        Path to the SQLite database where the results are stored.
    results : :class:`compas_fea2.results.Results`
        Results object with the analyisis results.

    Notes
    -----
    Problems are registered to a :class:`compas_fea2.model.Model`.

    Problems can also be used as canonical `load combinations`, where each `load`
    is actually a `factored step`. For example, a typical load combination such
    as 1.35*DL+1.50LL can be applied to the model by creating the Steps DL and LL,
    factoring them (see :class:`compas_fea2.problem.Step documentation) and adding
    them to Problme

    While for linear models the sequence of the steps is irrelevant, it is not the
    case for non-linear models.

    Warnings
    --------
    Factore Steps are new objects! check the :class:`compas_fea2.problem._Step
    documentation.

    """

    def __init__(self, description=None, **kwargs):
        super(Problem, self).__init__(**kwargs)
        self.description = description
        self._path = None
        self._path_db = None
        self._steps = set()
        self._steps_order = []  # TODO make steps a list

    @property
    def model(self):
        return self._registration

    @property
    def steps(self):
        return self._steps

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value if isinstance(value, Path) else Path(value)
        self._path_db = os.path.join(self._path, "{}-results.db".format(self.name))

    @property
    def path_db(self):
        return self._path_db

    @property
    def results_db(self):
        return ResultsDatabase(self)

    @property
    def steps_order(self):
        return self._steps_order

    @steps_order.setter
    def steps_order(self, value):
        for step in value:
            if not self.is_step_in_problem(step, add=False):
                raise ValueError("{!r} must be previously added to {!r}".format(step, self))
        self._steps_order = value

    @property
    def input_file(self):
        return InputFile(self)

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def find_step_by_name(self, name):
        # type: (str) -> Step
        """Find if there is a step with the given name in the problem.

        Parameters
        ----------
        name : str

        Returns
        -------
        :class:`compas_fea2.problem._Step`

        """
        for step in self.steps:
            if step.name == name:
                return step

    def is_step_in_problem(self, step, add=True):
        """Check if a :class:`compas_fea2.problem._Step` is defined in the Problem.

        Parameters
        ----------
        step : :class:`compas_fea2.problem._Step`
            The Step object to find.

        Returns
        -------
        :class:`compas_fea2.problem._Step`

        Raises
        ------
        ValueError
            if `step` is a string and the step is not defined in the problem
        TypeError
            `step` must be either an instance of a `compas_fea2` Step class or the
            name of a Step already defined in the Problem.
        """

        if not isinstance(step, Step):
            raise TypeError("{!r} is not a Step".format(step))
        if step not in self.steps:
            print("{!r} not found".format(step))
            if add:
                step = self.add_step(step)
                print("{!r} added to the Problem".format(step))
                return step
            return False
        return True

    def add_step(self, step):
        # # type: (_Step) -> Step
        """Adds a :class:`compas_fea2.problem._Step` to the problem. The name of
        the Step must be unique

        Parameters
        ----------
        Step : :class:`compas_fea2.problem._Step`
            The analysis step to add to the problem.

        Returns
        -------
        :class:`compas_fea2.problem._Step`
        """
        if not isinstance(step, Step):
            raise TypeError("You must provide a valid compas_fea2 Step object")

        if self.find_step_by_name(step):
            raise ValueError("There is already a step with the same name in the model.")

        step._key = len(self._steps)
        self._steps.add(step)
        step._registration = self
        self._steps_order.append(step)
        return step

    def add_static_step(self, step=None, **kwargs):
        # # type: (_Step) -> Step
        """Adds a :class:`compas_fea2.problem._Step` to the problem. The name of
        the Step must be unique

        Parameters
        ----------
        Step : :class:`compas_fea2.problem.StaticStep`, optional
            The analysis step to add to the problem, by default None.
            If not provided, a :class:`compas_fea2.problem.StaticStep` with default
            attributes is created.

        Returns
        -------
        :class:`compas_fea2.problem._Step`
        """
        if step:
            if not isinstance(step, StaticStep):
                raise TypeError("You must provide a valid compas_fea2 Step object")

            if self.find_step_by_name(step):
                raise ValueError("There is already a step with the same name in the model.")
        else:
            step = StaticStep(**kwargs)

        step._key = len(self._steps)
        self._steps.add(step)
        step._registration = self
        self._steps_order.append(step)
        return step

    def add_steps(self, steps):
        """Adds multiple :class:`compas_fea2.problem._Step` objects to the problem.

        Parameters
        ----------
        steps : list[:class:`compas_fea2.problem._Step`]
            List of steps objects in the order they will be applied.

        Returns
        -------
        list[:class:`compas_fea2.problem._Step`]
        """
        return [self.add_step(step) for step in steps]

    def define_steps_order(self, order):
        """Defines the order in which the steps are applied during the analysis.

        Parameters
        ----------
        order : list
            List contaning the names of the analysis steps in the order in which
            they are meant to be applied during the analysis.

        Returns
        -------
        None

        Warning
        -------
        Not implemented yet!
        """
        for step in order:
            if not isinstance(step, Step):
                raise TypeError("{} is not a step".format(step))
        self._steps_order = order

    def add_linear_perturbation_step(self, lp_step, base_step):
        """Add a linear perturbation step to a previously defined step.

        Parameters
        ----------
        lp_step : obj
            :class:`compas_fea2.problem.LinearPerturbation` subclass instance
        base_step : str
            name of a previously defined step which will be used as starting conditions
            for the application of the linear perturbation step.

        Notes
        -----
        Linear perturbartion steps do not change the history of the problem (hence
        following steps will not consider their effects).

        """
        raise NotImplementedError

    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):
        # type: () -> str
        """Prints a summary of the Problem object.

        Parameters
        ----------
        None

        Returns
        -------
        str
            Problem summary
        """
        steps_data = "\n".join([f"{step.name}" for step in self.steps])

        summary = f"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Problem: {self._name}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

description: {self.description or "N/A"}

Steps (in order of application)
-------------------------------
{steps_data}

Analysis folder path : {self.path or "N/A"}

"""
        print(summary)
        return summary

    # =========================================================================
    #                         Analysis methods
    # =========================================================================
    def write_input_file(self, path=None):
        # type: (Path |str) -> None
        """Writes the input file.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.

        Returns
        -------
        :class:`compas_fea2.job.InputFile`
            The InputFile objects that generates the input file.
        """
        path = path or self.path
        if not isinstance(path, Path):
            path = Path(path)
        if not path.exists():
            path.mkdir(parents=True)
        return self.input_file.write_to_file(path)

    def _check_analysis_path(
        self,
        path,
        erase_data=False,
    ):
        """Check the analysis path and adds the correct folder structure.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path where the input file will be saved.

        Returns
        -------
        :class:`pathlib.Path`
            Path where the input file will be saved.

        """
        self.model.path = path
        self.path = self.model.path.joinpath(self.name)
        if os.path.exists(self.path):
            # Check if the folder is an FEA2 results folder
            is_fea2_folder = any(fname.endswith("-results.db") for fname in os.listdir(self.path))
            if is_fea2_folder:
                if not erase_data:
                    user_input = input(f"The directory {self.path} already exists and contains FEA2 results. Do you want to delete its contents? (y/n): ")
                    asw = user_input.lower()
                else:
                    asw = "y"
                if asw == "y":
                    for root, dirs, files in os.walk(self.path):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for dir in dirs:
                            os.rmdir(os.path.join(root, dir))
                else:
                    print(f"WARNING: The directory {self.path} already exists and contains FEA2 results. Duplicated results expected.")
            else:
                print(f"The directory {self.path} is not recognized as an FEA2 results folder. No files were deleted.")
        else:
            os.makedirs(self.path)
        return self.path

    def analyse(self, path=None, erase_data=False, *args, **kwargs):
        """Analyse the problem in the selected backend.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.

        """
        raise NotImplementedError("this function is not available for the selected backend")

    def analyze(self, path=None, erase_data=False, *args, **kwargs):
        """American spelling of the analyse method"""
        self.analyse(path=path, *args, **kwargs)

    def analyse_and_extract(self, path=None, erase_data=False, *args, **kwargs):
        """Analyse the problem in the selected backend and extract the results
        from the native database system to SQLite.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.
        """
        if path:
            self.path = path
        raise NotImplementedError("this function is not available for the selected backend")

    def restart_analysis(self, *args, **kwargs):
        """Continue a previous analysis from a given increement with additional
        steps.

        Parameters
        ----------
        problem : :class:`compas_fea2.problme.Problem`
            The problem (already analysed) to continue.
        start : float
            Time-step increment.
        steps : [:class:`compas_fea2.problem.Step`]
            List of steps to add to the orignal problem.

        Raises
        ------
        ValueError
            _description_

        Notes
        -----
        For abaqus, you have to specify to save specific files during the original
        analysis by passing the `restart=True` option.

        """
        raise NotImplementedError("this function is not available for the selected backend")

    # =========================================================================
    #                         Results methods - general
    # =========================================================================

    # =========================================================================
    #                         Results methods - displacements
    # =========================================================================

    # =========================================================================
    #                         Viewer methods
    # =========================================================================
    def show(self, steps=None, fast=True, scale_model=1.0, show_parts=True, show_bcs=1.0, show_loads=1.0, **kwargs):
        """Visualise the model in the viewer.

        Parameters
        ----------
        scale_model : float, optional
            Scale factor for the model, by default 1.0
        show_bcs : float, optional
            Scale factor for the boundary conditions, by default 1.0
        show_loads : float, optional
            Scale factor for the loads, by default 1.0

        """
        if not steps:
            steps = self.steps_order

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.config.vectorsize = 0.2
        viewer.add_model(self.model, show_parts=show_parts, opacity=0.5, show_bcs=show_bcs, **kwargs)

        for step in steps:
            viewer.add_step(step, show_loads=show_loads)

        viewer.show()
        viewer.scene.clear()
