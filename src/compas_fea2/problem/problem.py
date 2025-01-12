from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path

from compas.colors import Color
from compas.colors import ColorMap
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import centroid_points_weighted
from compas.geometry import sum_vectors

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

    # =========================================================================
    #                           Loads methods
    # =========================================================================

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
        input_file = InputFile.from_problem(self)
        input_file.write_to_file(path)
        return input_file

    def _check_analysis_path(self, path):
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
        if path:
            self.model.path = path
            self.path = self.model.path.joinpath(self.name)
        if not self.path and not self.model.path:
            raise AttributeError("You must provide a path for storing the model and the analysis results.")
        return self.path

    def analyse(self, path=None, *args, **kwargs):
        """Analyse the problem in the selected backend.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.

        """
        raise NotImplementedError("this function is not available for the selected backend")

    def analyze(self, *args, **kwargs):
        """American spelling of the analyse method"""
        self.analyse(*args, **kwargs)

    def analyse_and_extract(self, path=None, *args, **kwargs):
        """Analyse the problem in the selected backend and extract the results
        from the native database system to SQLite.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.
        """
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
    #                         Results methods - reactions
    # =========================================================================
    def get_total_reaction(self, step=None):
        """Compute the total reaction vector

        Parameters
        ----------
        step : :class:`compas_fea2.problem._Step`, optional
            The analysis step, by default the last step.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The resultant vector.
        :class:`compas.geometry.Point`
            The application point.
        """
        if not step:
            step = self.steps_order[-1]
        reactions = self.reaction_field
        locations, vectors, vectors_lengths = [], [], []
        for reaction in reactions.results(step):
            locations.append(reaction.location.xyz)
            vectors.append(reaction.vector)
            vectors_lengths.append(reaction.vector.length)
        return Vector(*sum_vectors(vectors)), Point(*centroid_points_weighted(locations, vectors_lengths))

    def get_min_max_reactions(self, step=None):
        """Get the minimum and maximum reaction values for the last step.

        Parameters
        ----------
        step : _type_, optional
            _description_, by default None
        """
        if not step:
            step = self.steps_order[-1]
        reactions = self.reaction_field
        return reactions.get_limits_absolute(step)

    def get_min_max_reactions_component(self, component, step=None):
        """Get the minimum and maximum reaction values for the last step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_, optional
            _description_, by default None
        """
        if not step:
            step = self.steps_order[-1]
        reactions = self.reaction_field
        return reactions.get_limits_component(component, step)

    # def get_total_moment(self, step=None):
    #     if not step:
    #         step = self.steps_order[-1]
    #     vector, location = self.get_total_reaction(step)

    #     return sum_vectors([reaction.vector for reaction in reactions.results])

    # =========================================================================
    #                         Results methods - displacements
    # =========================================================================

    # =========================================================================
    #                         Viewer methods
    # =========================================================================
    def show(self, fast=True, scale_model=1.0, show_parts=True, show_bcs=1.0, show_loads=1.0, **kwargs):
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

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.config.vectorsize = 0.2
        viewer.add_model(self.model, show_parts=show_parts, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        # if show_loads:
        #     register(step.__class__, FEA2StepObject, context="Viewer")
        #     viewer.viewer.scene.add(step, step=step, scale_factor=show_loads)
        viewer.show()
        viewer.scene.clear()

    def show_principal_stress_vectors(self, step=None, components=None, scale_model=1, scale_results=1, show_loads=True, show_bcs=True, **kwargs):
        """Display the principal stress results for a given step.

        Parameters
        ----------
        step : _type_, optional
            _description_, by default None
        components : _type_, optional
            _description_, by default None
        scale_model : int, optional
            _description_, by default 1
        scale_results : int, optional
            _description_, by default 1
        show_loads : bool, optional
            _description_, by default True
        show_bcs : bool, optional
            _description_, by default True
        """

        from compas.scene import register
        from compas.scene import register_scene_objects

        from compas_fea2.UI.viewer import FEA2ModelObject
        from compas_fea2.UI.viewer import FEA2StepObject
        from compas_fea2.UI.viewer import FEA2StressFieldResultsObject
        from compas_fea2.UI.viewer import FEA2Viewer

        if not step:
            step = self.steps_order[-1]

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.viewer.config.vectorsize = 0.2

        register_scene_objects()  # This has to be called before registering the model object

        register(self.model.__class__.__bases__[-1], FEA2ModelObject, context="Viewer")
        viewer.viewer.scene.add(self.model, model=self.model, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)

        register(self.stress_field.__class__.__bases__[-1], FEA2StressFieldResultsObject, context="Viewer")
        viewer.viewer.scene.add(self.stress_field, field=self.stress_field, step=step, scale_factor=scale_results, components=components, **kwargs)

        if show_loads:
            register(step.__class__, FEA2StepObject, context="Viewer")
            viewer.viewer.scene.add(step, step=step, scale_factor=show_loads)

        viewer.viewer.show()

    def show_deformed(self, step=None, opacity=1, show_bcs=1, scale_results=1, scale_model=1, show_loads=0.1, show_original=False, **kwargs):
        """Display the structure in its deformed configuration.

        Parameters
        ----------
        step : :class:`compas_fea2.problem._Step`, optional
            The Step of the analysis, by default None. If not provided, the last
            step is used.

        Returns
        -------
        None

        """
        if not step:
            step = self.steps_order[-1]

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)

        if show_original:
            viewer.add_model(self.model, fast=True, opacity=show_original, show_bcs=False, **kwargs)
        # TODO create a copy of the model first
        displacements = step.problem.displacement_field
        for displacement in displacements.results(step):
            vector = displacement.vector.scaled(scale_results)
            displacement.node.xyz = sum_vectors([Vector(*displacement.location.xyz), vector])
        viewer.add_model(self.model, fast=True, opacity=opacity, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        viewer.viewer.show()

    def show_displacements(self, step=None, fast=True, show_bcs=1, scale_model=1, show_loads=0.1, component=None, show_vectors=True, show_contours=True, **kwargs):
        """Display the displacement field results for a given step.

        Parameters
        ----------
        step : _type_, optional
            _description_, by default None
        scale_model : int, optional
            _description_, by default 1
        show_loads : bool, optional
            _description_, by default True
        component : _type_, optional
            _description_, by default

        """
        if not step:
            step = self.steps_order[-1]

        if not step.displacement_field:
            raise ValueError("No displacement field results available for this step")

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.add_model(self.model, fast=fast, show_parts=True, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        viewer.add_displacement_field(step.displacement_field, fast=fast, step=step, component=component, show_vectors=show_vectors, show_contours=show_contours, **kwargs)
        if show_loads:
            viewer.add_step(step, show_loads=show_loads)
        viewer.show()
        viewer.scene.clear()

    def show_reactions(self, step=None, show_bcs=1, scale_model=1, show_loads=0.1, component=None, show_vectors=1, show_contours=False, **kwargs):
        """Display the reaction field results for a given step.

        Parameters
        ----------
        step : _type_, optional
            _description_, by default None
        scale_model : int, optional
            _description_, by default 1
        show_bcs : bool, optional
            _description_, by default True
        component : _type_, optional
            _description_, by default
        translate : _type_, optional
            _description_, by default -1
        scale_results : _type_, optional
            _description_, by default 1
        """
        from compas.scene import register
        from compas.scene import register_scene_objects

        from compas_fea2.UI.viewer import FEA2ModelObject
        from compas_fea2.UI.viewer import FEA2ReactionFieldResultsObject
        from compas_fea2.UI.viewer import FEA2StepObject
        from compas_fea2.UI.viewer import FEA2Viewer

        if not step:
            step = self.steps_order[-1]

        if not step.problem.reaction_field:
            raise ValueError("No reaction field results available for this step")

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.viewer.config.vectorsize = 0.2

        register_scene_objects()  # This has to be called before registering the model object

        register(self.model.__class__, FEA2ModelObject, context="Viewer")
        viewer.viewer.scene.add(self.model, model=self.model, show_parts=True, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)

        register(step.problem.reaction_field.__class__, FEA2ReactionFieldResultsObject, context="Viewer")
        viewer.viewer.scene.add(
            step.problem.reaction_field, field=step.problem.reaction_field, step=step, component=component, show_vectors=show_vectors, show_contour=show_contours, **kwargs
        )

        if show_loads:
            register(step.__class__, FEA2StepObject, context="Viewer")
            viewer.viewer.scene.add(step, step=step, scale_factor=show_loads)

        viewer.viewer.show()

    def show_stress_contour(self, step=None, stresstype="vonmieses", high=None, low=None, cmap=None, side=None, scale_model=1.0, show_bcs=True, **kwargs):
        from compas.scene import register
        from compas.scene import register_scene_objects

        from compas_fea2.UI.viewer import FEA2ModelObject
        from compas_fea2.UI.viewer import FEA2Viewer

        register_scene_objects()  # This has to be called before registering the model object
        register(self.model.__class__.__bases__[-1], FEA2ModelObject, context="Viewer")

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.viewer.scene.add(self.model, model=self.model, opacity=0.3, show_bcs=show_bcs, show_parts=True)

        if not step:
            step = self.steps_order[-1]
        field_locations = list(self.stress_field.locations(step, point=True))
        field_results = list(getattr(self.stress_field, stresstype)(step))

        # # Get values
        min_value = high or min(field_results)
        max_value = low or max(field_results)
        cmap = cmap or ColorMap.from_palette("hawaii")
        points = []
        for n, v in zip(field_locations, field_results):
            if kwargs.get("bound", None):
                if v >= kwargs["bound"][1] or v <= kwargs["bound"][0]:
                    color = Color.red()
                else:
                    color = cmap(v, minval=min_value, maxval=max_value)
            else:
                color = cmap(v, minval=min_value, maxval=max_value)
            points.append((n, {"pointcolor": color, "pointsize": 20}))

        viewer.viewer.scene.add(points, name=f"{stresstype} Contour")
        viewer.viewer.show()

    def show_mode_shape(
        self, step, mode, fast=True, opacity=1, scale_results=1, scale_model=1.0, show_bcs=True, show_original=0.25, show_contour=False, show_vectors=False, **kwargs
    ):

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)

        if show_original:
            viewer.add_model(self.model, show_parts=True, fast=True, opacity=show_original, show_bcs=False, **kwargs)

        shape = step.problem.modal_shape(mode)
        if show_vectors:
            viewer.add_mode_shape(shape, fast=fast, step=step, component=None, show_vectors=show_vectors, show_contour=show_contour, **kwargs)

        # TODO create a copy of the model first
        for displacement in shape.results(step):
            vector = displacement.vector.scaled(scale_results)
            displacement.node.xyz = sum_vectors([Vector(*displacement.location.xyz), vector])

        if show_contour:
            viewer.add_mode_shape(shape, fast=fast, step=step, component=None, show_vectors=show_vectors, show_contour=show_contour, **kwargs)
        viewer.add_model(self.model, fast=fast, opacity=opacity, show_bcs=show_bcs, **kwargs)
        viewer.show()
