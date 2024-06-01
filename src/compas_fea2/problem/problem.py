from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import centroid_points_weighted
from compas.geometry import sum_vectors

from compas_fea2.base import FEAData
from compas_fea2.job.input_file import InputFile
from compas_fea2.model.elements import _Element1D
from compas_fea2.model.elements import _Element3D
from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import Step
from compas_fea2.results import DisplacementFieldResults
from compas_fea2.results import ReactionFieldResults
from compas_fea2.results import StressFieldResults
from compas_fea2.results.database import ResultsDatabase
from compas_fea2.utilities._utils import timer


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

    def __init__(self, name=None, description=None, **kwargs):
        super(Problem, self).__init__(name=name, **kwargs)
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
        if os.path.exists(self.path_db):
            return ResultsDatabase(self.path_db)

    @property
    def displacement_field(self):
        return DisplacementFieldResults(problem=self)

    @property
    def reaction_field(self):
        return ReactionFieldResults(problem=self)

    @property
    def temperature_field(self):
        raise NotImplementedError

    @property
    def stress_field(self):
        return StressFieldResults(problem=self)

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

        summary = """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Problem: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

description: {}

Steps (in order of application)
-------------------------------
{}

Analysis folder path : {}

""".format(
            self._name, self.description or "N/A", steps_data, self.path or "N/A"
        )
        print(summary)
        return summary

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    # @timer(message="Finished writing input file in")
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
        if not step:
            step = self.steps_order[-1]
        reactions = self.reaction_field
        return reactions.get_limits_absolute(step)

    def get_min_max_reactions_component(self, component, step=None):
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
    def show(
        self,
        scale_factor=1.0,
        parts=None,
        elements=True,
        solid=False,
        draw_nodes=True,
        node_labels=True,
        draw_bcs=1.0,
        draw_constraints=True,
        **kwargs,
    ):
        """Visualise the model in the viewer.

        Parameters
        ----------
        width : int, optional
            _description_, by default 1600
        height : int, optional
            _description_, by default 900
        scale_factor : _type_, optional
            _description_, by default 1.
        parts : _type_, optional
            _description_, by default None
        solid : bool, optional
            _description_, by default True
        draw_nodes : bool, optional
            _description_, by default False
        node_labels : bool, optional
            _description_, by default False
        draw_bcs : _type_, optional
            _description_, by default 1.
        draw_constraints : bool, optional
            _description_, by default True

        """

        from compas_fea2.model.elements import BeamElement
        from compas_fea2.model.elements import ShellElement
        from compas_fea2.UI.viewer import FEA2Viewer

        # v = FEA2Viewer(self.model, scale_factor=scale_factor)
        v = FEA2Viewer(self.model, camera={})

        # parts = parts or self.model.parts

        # if draw_bcs:
        #     v.draw_bcs(self.model, parts, draw_bcs)

        # # if draw_constraints:
        # #     v.draw_constraint(self.constraints)
        # for part in parts:
        #     v.draw_solid_elements(filter(lambda x: isinstance(x, _Element3D), part.elements), draw_nodes)
        #     v.draw_shell_elements(filter(lambda x: isinstance(x, ShellElement), part.elements), draw_nodes)
        #     v.draw_beam_elements(filter(lambda x: isinstance(x, BeamElement), part.elements), draw_nodes)

        # if kwargs.get("draw_loads", None):
        #     for step in self.steps:
        #         v.draw_loads(step, scale_factor=kwargs["draw_loads"])
        bm =  [p for p in self.model.parts][0].boundary_mesh
        v.draw_mesh(bm)
        v.show()

    def show_nodes_field_vector(self, field_results, component=None, vector_sf=1.0, model_sf=1.0, step=None, **kwargs):
        """Display a given vector field.

        Parameters
        ----------
        field : str
            The field to display, e.g. 'U' for displacements.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        component : str
            The compoenet of the field to display, e.g. 'U3' for displacements
            along the 3 axis.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        step : :class:`compas_fea2.problem.Step`, optional
            The step to show the results of, by default None.
            if not provided, the last step of the analysis is used.
        deformed : bool, optional
            Choose if to display on the deformed configuration or not, by default False
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Options
        -------
        draw_loads : float
            Displays the loads at the step scaled by the given value
        draw_bcs : float
            Displays the bcs of the model scaled by the given value
        bound : float
            limit the results to the given value

        Raises
        ------
        ValueError
            _description_

        """
        from compas_fea2.UI.viewer import FEA2Viewer

        if not step:
            step = self.steps_order[-1]

        # Display results
        v = FEA2Viewer(self.model, scale_factor=model_sf)
        v.draw_nodes_field_vector(field_results, component, step=step, vector_sf=vector_sf, **kwargs)

        opacity = kwargs.get("opacity", 0.5)
        for part in self.model.parts:
            v.draw_mesh(part.discretized_boundary_mesh, opacity=opacity)

        if kwargs.get("draw_bcs", None):
            v.draw_bcs(self.model, scale_factor=kwargs["draw_bcs"])

        if kwargs.get("draw_loads", None):
            v.draw_loads(step, scale_factor=kwargs["draw_loads"])

        if kwargs.get("draw_reactions", None):
            v.draw_reactions(step, scale_factor=kwargs["draw_reactions"])
        v.show()

    def show_nodes_field_contour(self, field_results, component, step=None, model_sf=1.0, **kwargs):
        """Display a contour plot of a given field and component. The field must
        de defined at the nodes of the model (e.g displacement field).

        Parameters
        ----------
        field : str
            The field to display, e.g. 'U' for displacements.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        component : str
            The compoenet of the field to display, e.g. 'U3' for displacements
            along the 3 axis.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        step : :class:`compas_fea2.problem.Step`, optional
            The step to show the results of, by default None.
            if not provided, the last step of the analysis is used.
        deformed : bool, optional
            Choose if to display on the deformed configuration or not, by default False
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Options
        -------
        draw_loads : float
            Displays the loads at the step scaled by the given value
        draw_bcs : float
            Displays the bcs of the model scaled by the given value
        bound : float
            limit the results to the given value

        Raises
        ------
        ValueError
            _description_

        """
        from compas_fea2.UI.viewer import FEA2Viewer

        if not step:
            step = self.steps_order[-1]

        # Display results
        v = FEA2Viewer(self.model, scale_factor=model_sf)
        v.draw_nodes_field_contour(field_results=field_results, component=component, step=step, **kwargs)

        if kwargs.get("draw_bcs", None):
            v.draw_bcs(self.model, scale_factor=kwargs["draw_bcs"])

        if kwargs.get("draw_loads", None):
            v.draw_loads(step, scale_factor=kwargs["draw_loads"])

        if kwargs.get("draw_reactions", None):
            v.draw_reactions(step, scale_factor=kwargs["draw_reactions"])
        v.show()

    def show_elements_field_vector(self, field_results, vector_sf=1.0, model_sf=1.0, step=None, **kwargs):
        """Display a given vector field.

        Parameters
        ----------
        field : str
            The field to display, e.g. 'U' for displacements.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        component : str
            The compoenet of the field to display, e.g. 'U3' for displacements
            along the 3 axis.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        step : :class:`compas_fea2.problem.Step`, optional
            The step to show the results of, by default None.
            if not provided, the last step of the analysis is used.
        deformed : bool, optional
            Choose if to display on the deformed configuration or not, by default False
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Options
        -------
        draw_loads : float
            Displays the loads at the step scaled by the given value
        draw_bcs : float
            Displays the bcs of the model scaled by the given value
        bound : float
            limit the results to the given value

        Raises
        ------
        ValueError
            _description_

        """
        from compas_fea2.UI.viewer import FEA2Viewer

        if not step:
            step = self.steps_order[-1]

        # Display results

        v = FEA2Viewer(self.model, scale_factor=model_sf)
        v.draw_elements_field_vector(field_results=field_results, step=step, vector_sf=vector_sf, **kwargs)

        opacity = kwargs.get("opacity", 0.5)
        for part in self.model.parts:
            v.draw_mesh(part.discretized_boundary_mesh, opacity=opacity)
            # v.draw_solid_elements(filter(lambda x: isinstance(x, _Element3D), part.elements), opacity=0.5)
            # v.draw_shell_elements(filter(lambda x: isinstance(x, _Element2D), part.elements), opacity=0.5)
            v.draw_beam_elements(filter(lambda x: isinstance(x, _Element1D), part.elements), opacity=0.5)

        if kwargs.get("draw_bcs", None):
            v.draw_bcs(self.model, scale_factor=kwargs["draw_bcs"])

        if kwargs.get("draw_loads", None):
            v.draw_loads(step, scale_factor=kwargs["draw_loads"])

        if kwargs.get("draw_reactions", None):
            v.draw_reactions(step, scale_factor=kwargs["draw_reactions"])
        v.show()

    def show_deformed(self, step=None, scale_factor=1.0, original=0.5, opacity=0.5, **kwargs):
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
        from compas_fea2.UI.viewer import FEA2Viewer

        v = FEA2Viewer(self.model)

        if not step:
            step = self.steps_order[-1]

        if original:
            for part in step.model.parts:
                try:
                    v.draw_mesh(part.discretized_boundary_mesh, opacity=original)
                except Exception:
                    print("No mesh found")
                # v.draw_nodes_field_vector(step=step, field_name='U', vector_sf=scale_factor)

        v.draw_deformed(step, scale_factor=scale_factor, opacity=opacity)

        if kwargs.get("draw_bcs", None):
            v.draw_bcs(self.model, scale_factor=kwargs["draw_bcs"])

        if kwargs.get("draw_loads", None):
            v.draw_loads(step, scale_factor=kwargs["draw_loads"])

        if kwargs.get("draw_reactions", None):
            v.draw_reactions(step=step, scale_factor=kwargs["draw_reactions"])
        v.show()

    def show_reactions(self, vector_sf=1.0, model_sf=1.0, step=None, group_nodes=False, **kwargs):
        self.show_nodes_field_vector(field_name="RF", vector_sf=vector_sf, model_sf=model_sf, step=step, **kwargs)

    def show_stress_contours(self, stress_type="von_mises_stress", side=None, step=None, model_sf=1.0, **kwargs):
        stresses = self.stress_field
        if not step:
            step = self.steps_order[-1]
        nodes_stress = {}
        for stress in stresses.results(step):
            for node in stress.location.nodes:
                if node not in nodes_stress:
                    nodes_stress[node] = 2.0

                if not isinstance(stress.location, _Element3D):
                    func = stress_type + "_" + side
                else:
                    func = stress_type
                # nodes_stress[node] += min(stress.principal_stresses_values_top)/len(stress.location.nodes)
                # nodes_stress[node] += min(stress.principal_stresses_values_top)/len(stress.location.nodes)
                nodes_stress[node] += getattr(stress, func) / len(stress.location.nodes)

        from compas_fea2.UI.viewer import FEA2Viewer

        if not step:
            step = self.steps_order[-1]

        # Display results
        v = FEA2Viewer(self.model, scale_factor=model_sf)

        v.draw_nodes_contour(model=self.model, nodes_values=nodes_stress, **kwargs)

        if kwargs.get("draw_bcs", None):
            v.draw_bcs(self.model, scale_factor=kwargs["draw_bcs"])

        if kwargs.get("draw_loads", None):
            v.draw_loads(step, scale_factor=kwargs["draw_loads"])

        if kwargs.get("draw_reactions", None):
            v.draw_reactions(step, scale_factor=kwargs["draw_reactions"])
        v.show()
