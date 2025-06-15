import os
import shutil
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

from compas_fea2.base import FEAData
from compas_fea2.job.input_file import InputFile
from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import Step
from compas_fea2.results.database import ResultsDatabase


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

    def __init__(self, description: Optional[str] = None, **kwargs):
        super(Problem, self).__init__(**kwargs)
        self.description = description
        self._path = None
        self._path_db = None
        self._steps = set()
        self._steps_order = []  # TODO make steps a list
        self._rdb = None

    @property
    def model(self) -> "Model":  # noqa: F821
        return self._registration

    @property
    def steps(self) -> set:
        return self._steps

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, value: Union[str, Path]):
        self._path = value if isinstance(value, Path) else Path(value)
        self._path_db = os.path.join(self._path, "{}-results.db".format(self.name))

    @property
    def path_db(self) -> str:
        return self._path_db

    @property
    def rdb(self) -> ResultsDatabase:
        return self._rdb or ResultsDatabase.sqlite(self)

    @rdb.setter
    def rdb(self, value: str):
        if not hasattr(ResultsDatabase, value):
            raise ValueError("Invalid ResultsDatabase option")
        self._rdb = getattr(ResultsDatabase, value)(self)

    @property
    def steps_order(self) -> List[Step]:
        return self._steps_order

    @steps_order.setter
    def steps_order(self, value: List[Step]):
        for step in value:
            if not self.is_step_in_problem(step, add=False):
                raise ValueError("{!r} must be previously added to {!r}".format(step, self))
        self._steps_order = value

    @property
    def input_file(self) -> InputFile:
        return InputFile(self)

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def find_step_by_name(self, name: str) -> Optional[Step]:
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

    def is_step_in_problem(self, step: Step, add: bool = True) -> Union[bool, Step]:
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

    def add_step(self, step: Step) -> Step:
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

    def add_static_step(self, **kwargs) -> Step:
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

        step = StaticStep(**kwargs)

        step._key = len(self._steps)
        self._steps.add(step)
        step._registration = self
        self._steps_order.append(step)
        return step

    def add_steps(self, steps: List[Step]) -> List[Step]:
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

    def define_steps_order(self, order: List[Step]):
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

    def add_linear_perturbation_step(self, lp_step: "LinearPerturbation", base_step: str):  # noqa: F821
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

    def summary(self) -> str:
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
    def write_input_file(self, path: Optional[Union[Path, str]] = None) -> InputFile:
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

    def _check_analysis_path(self, path: Path, erase_data: bool = False) -> Path:
        """Check and prepare the analysis path, ensuring the correct folder structure.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path where the input file will be saved.
        erase_data : bool, optional
            If True, automatically erase the folder's contents if it is recognized as an FEA2 results folder. Default is False.

        Returns
        -------
        :class:`pathlib.Path`
            Path where the input file will be saved.

        Raises
        ------
        ValueError
            If the folder is not a valid FEA2 results folder and `erase_data` is True but not confirmed by the user.
        """

        def _delete_folder_contents(folder_path: Path):
            """Helper method to delete all contents of a folder."""
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    os.remove(Path(root) / file)
                for dir in dirs:
                    shutil.rmtree(Path(root) / dir)

        if not isinstance(path, Path):
            path = Path(path)

        # Prepare the main and analysis paths
        self.model.path = path
        self.path = self.model.path.joinpath(self.name)

        if self.path.exists():
            # Check if the folder contains FEA2 results
            is_fea2_folder = any(fname.endswith("-results.db") for fname in os.listdir(self.path))

            if is_fea2_folder:
                if not erase_data:
                    user_input = input(f"The directory {self.path} already exists and contains FEA2 results. Do you want to delete its contents? (Y/n): ").strip().lower()
                    erase_data = user_input in ["y", "yes", ""]

                if erase_data:
                    _delete_folder_contents(self.path)
                    print(f"All contents of {self.path} have been deleted.")
                else:
                    print(f"WARNING: The directory {self.path} already exists and contains FEA2 results. Duplicated results expected.")
            else:
                # Folder exists but is not an FEA2 results folder
                if erase_data and erase_data == "armageddon":
                    _delete_folder_contents(self.path)
                else:
                    user_input = (
                        input(f"ATTENTION! The directory {self.path} already exists and might NOT be a FEA2 results folder. Do you want to DELETE its contents? (y/N): ")
                        .strip()
                        .lower()
                    )
                    if user_input in ["y", "yes"]:
                        _delete_folder_contents(self.path)
                        print(f"All contents of {self.path} have been deleted.")
                    else:
                        raise ValueError(f"The directory {self.path} exists but is not recognized as a valid FEA2 results folder, and its contents were not cleared.")
        else:
            # Create the directory if it does not exist
            self.path.mkdir(parents=True, exist_ok=True)

        return self.path

    def analyse(self, path: Optional[Union[Path, str]] = None, erase_data: bool = False, *args, **kwargs):
        """Analyse the problem in the selected backend.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.

        """
        # generate keys
        self.model.assign_keys()
        raise NotImplementedError("this function is not available for the selected backend")

    def analyze(self, path: Optional[Union[Path, str]] = None, erase_data: bool = False, *args, **kwargs):
        """American spelling of the analyse method"""
        self.analyse(path=path, *args, **kwargs)

    def extract_results(self, path: Optional[Union[Path, str]] = None, erase_data: Optional[Union[bool, str]] = False, *args, **kwargs):
        """Extract the results from the native database system to SQLite.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path to the folder where the results are saved.
        erase_data : bool, optional
            If True, automatically erase the folder's contents if it is recognized as an FEA2 results folder. Default is False.
            Pass "armageddon" to erase all contents of the folder without checking.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.
        """
        if path:
            self.path = path
        raise NotImplementedError("this function is not available for the selected backend")

    def analyse_and_extract(self, path: Optional[Union[Path, str]] = None, erase_data: bool = False, *args, **kwargs):
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
    def show(
        self, steps: Optional[List[Step]] = None, fast: bool = True, scale_model: float = 1.0, show_parts: bool = True, show_bcs: float = 1.0, show_loads: float = 1.0, **kwargs
    ):
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
        from compas_fea2.UI.viewer import FEA2Viewer

        if not steps:
            steps = self.steps_order

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.config.vectorsize = 0.2
        viewer.add_model(self.model, show_parts=show_parts, opacity=0.5, show_bcs=show_bcs, **kwargs)

        for step in steps:
            viewer.add_step(step, show_loads=show_loads)

        viewer.show()
        viewer.scene.clear()

    @property
    def __data__(self) -> dict:
        """Returns a dictionary representation of the Problem object."""
        return {
            "description": self.description,
            "steps": [step.__data__() for step in self.steps],
            "path": str(self.path),
            "path_db": str(self.path_db),
        }

    @classmethod
    def __from_data__(cls, data: dict) -> "Problem":
        """Creates a Problem object from a dictionary representation."""
        problem = cls(description=data.get("description"))
        problem.path = data.get("path")
        problem._path_db = data.get("path_db")
        problem._steps = set(Step.__from_data__(step_data) for step_data in data.get("steps", []))
        problem._steps_order = list(problem._steps)
        return problem
