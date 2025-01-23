from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Vector
from compas.geometry import sum_vectors
from compas.geometry import Point
from compas.geometry import centroid_points_weighted

from compas_fea2.base import FEAData
from compas_fea2.problem.displacements import GeneralDisplacement
from compas_fea2.problem.fields import _PrescribedField
from compas_fea2.problem.loads import Load

from compas_fea2.results import DisplacementFieldResults
from compas_fea2.results import ReactionFieldResults
from compas_fea2.results import Stress2DFieldResults
from compas_fea2.results import SectionForcesFieldResults

from compas_fea2.UI import FEA2Viewer

# ==============================================================================
#                                Base Steps
# ==============================================================================


class Step(FEAData):
    """Initialises base Step object.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    field_outputs: :class:`compas_fea2.problem.FieldOutput'
        Field outuputs requested for the step.
    history_outputs: :class:`compas_fea2.problem.HistoryOutput'
        History outuputs requested for the step.
    results : :class:`compas_fea2.results.StepResults`
        The results of the analysis at this step

    Notes
    -----
    Steps are registered to a :class:`compas_fea2.problem.Problem`.

    A ``compas_fea2`` analysis is based on the concept of ``steps``,
    which represent the sequence in which the state of the model is modified.
    Steps can be introduced for example to change loads, boundary conditions,
    analysis procedure, etc. There is no limit on the number of steps in an analysis.

    Developer-only class.
    """

    def __init__(self, **kwargs):
        super(Step, self).__init__(**kwargs)
        self._field_outputs = set()
        self._history_outputs = set()
        self._results = None
        self._key = None

        self._patterns = set()
        self._load_cases = set()
        self._combination = None

    @property
    def problem(self):
        return self._registration

    @property
    def model(self):
        return self.problem.model

    @property
    def field_outputs(self):
        return self._field_outputs

    @property
    def load_cases(self):
        return self._load_cases

    @property
    def load_patterns(self):
        return self._patterns

    @property
    def combination(self):
        return self._combination

    @combination.setter
    def combination(self, combination):
        """Combine the load patterns according to their load case.

        Parameters
        ----------
        combination : :class:`compas_fea2.problem.combinations.LoadCombination`
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        combination._registration = self
        self._combination = combination
        # for case in combination.load_cases:
        #     if case not in self._load_cases:
        #         raise ValueError(f"{case} is not a valid load case.")
        for pattern in self.load_patterns:
            if pattern.load_case in combination.load_cases:
                factor = combination.factors[pattern.load_case]
                for node, load in pattern.node_load:
                    factored_load = factor * load

                    node.loads.setdefault(self, {}).setdefault(combination, {})[pattern] = factored_load
                    if node._total_load:
                        node._total_load += factored_load
                    else:
                        node._total_load = factored_load

    @property
    def history_outputs(self):
        return self._history_outputs

    @property
    def results(self):
        return self._results

    @property
    def key(self):
        return self._key

    def add_output(self, output):
        """Request a field or history output.

        Parameters
        ----------
        output : :class:`compas_fea2.problem._Output`
            The requested output.

        Returns
        -------
        :class:`compas_fea2.problem._Output`
            The requested output.

        Raises
        ------
        TypeError
            if the output is not an instance of an :class:`compas_fea2.problem._Output`.
        """
        output._registration = self
        self._field_outputs.add(output)
        return output

    def add_outputs(self, outputs):
        """Request multiple field or history outputs.

        Parameters
        ----------
        outputs : list(:class:`compas_fea2.problem._Output`)
            The requested outputs.

        Returns
        -------
        list(:class:`compas_fea2.problem._Output`)
            The requested outputs.

        Raises
        ------
        TypeError
            if the output is not an instance of an :class:`compas_fea2.problem._Output`.
        """
        for output in outputs:
            self.add_output(output)

    # ==========================================================================
    #                             Results methods
    # ==========================================================================
    @property
    def displacement_field(self):
        return DisplacementFieldResults(self)

    @property
    def reaction_field(self):
        return ReactionFieldResults(self)

    @property
    def temperature_field(self):
        raise NotImplementedError

    @property
    def stress2D_field(self):
        return Stress2DFieldResults(self)

    @property
    def section_forces_field(self):
        return SectionForcesFieldResults(self)


# ==============================================================================
#                                General Steps
# ==============================================================================


class GeneralStep(Step):
    """General Step object for use as a base class in a general static, dynamic
    or multiphysics analysis.

    Parameters
    ----------
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.
    restart : float, optional
        Frequency at which saving the results for restarting the analysis,
        by default `False`.

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.
    restart : float
        Frequency at which saving the results for restarting the analysis.
    loads : dict
        Dictionary of the loads assigned to each part in the model in the step.
    fields : dict
        Dictionary of the prescribed fields assigned to each part in the model in the step.

    """

    def __init__(self, max_increments, initial_inc_size, min_inc_size, time, nlgeom=False, modify=False, restart=False, **kwargs):
        super(GeneralStep, self).__init__(**kwargs)

        self._max_increments = max_increments
        self._initial_inc_size = initial_inc_size
        self._min_inc_size = min_inc_size
        self._time = time
        self._nlgeom = nlgeom
        self._modify = modify
        self._restart = restart
        self._patterns = set()
        self._load_cases = set()

    @property
    def patterns(self):
        return self._patterns

    @property
    def displacements(self):
        return list(filter(lambda p: isinstance(p.load, GeneralDisplacement), self._patterns))

    @property
    def load_patterns(self):
        return list(filter(lambda p: isinstance(p.load, Load), self._patterns))

    @property
    def fields(self):
        return list(filter(lambda p: isinstance(p.load, _PrescribedField), self._patterns))

    @property
    def max_increments(self):
        return self._max_increments

    @property
    def initial_inc_size(self):
        return self._initial_inc_size

    @property
    def min_inc_size(self):
        return self._min_inc_size

    @property
    def time(self):
        return self._time

    @property
    def nlgeometry(self):
        return self.nlgeom

    @property
    def modify(self):
        return self._modify

    @property
    def restart(self):
        return self._restart

    @restart.setter
    def restart(self, value):
        self._restart = value

    # ==============================================================================
    # Patterns
    # ==============================================================================
    def add_load_pattern(self, load_pattern):
        """Add a general :class:`compas_fea2.problem.patterns.Pattern` to the Step.

        Parameters
        ----------
        load_pattern : :class:`compas_fea2.problem.patterns.Pattern`
            The load pattern to add.

        Returns
        -------
        :class:`compas_fea2.problem.patterns.Pattern`

        """
        from compas_fea2.problem.patterns import Pattern

        if not isinstance(load_pattern, Pattern):
            raise TypeError("{!r} is not a LoadPattern.".format(load_pattern))

        # FIXME: ugly...
        try:
            if self.problem:
                if self.model:
                    if not list(load_pattern.distribution).pop().model == self.model:
                        raise ValueError("The load pattern is not applied to a valid reagion of {!r}".format(self.model))
        except Exception:
            pass

        self._patterns.add(load_pattern)
        self._load_cases.add(load_pattern.load_case)
        load_pattern._registration = self
        return load_pattern

    def add_load_patterns(self, load_patterns):
        """Add multiple :class:`compas_fea2.problem.patterns.Pattern` to the Problem.

        Parameters
        ----------
        load_patterns : list(:class:`compas_fea2.problem.patterns.Pattern`)
            The load patterns to add to the Problem.

        Returns
        -------
        list(:class:`compas_fea2.problem.patterns.Pattern`)

        """
        for load_pattern in load_patterns:
            self.add_load_pattern(load_pattern)

    # ==============================================================================
    # Combination
    # ==============================================================================

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
    # ==============================================================================
    # Visualisation
    # ==============================================================================

    def show_deformed(self, opacity=1, show_bcs=1, scale_results=1, scale_model=1, show_loads=0.1, show_original=False, **kwargs):
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
        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)

        if show_original:
            viewer.add_model(self.model, fast=True, opacity=show_original, show_bcs=False, **kwargs)
        # TODO create a copy of the model first
        displacements = self.displacement_field
        for displacement in displacements.results:
            vector = displacement.vector.scaled(scale_results)
            displacement.node.xyz = sum_vectors([Vector(*displacement.node.xyz), vector])
        viewer.add_model(self.model, fast=True, opacity=opacity, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        if show_loads:
            viewer.add_step(self, show_loads=show_loads)
        viewer.show()

    def show_displacements(self, fast=True, show_bcs=1, scale_model=1, show_loads=0.1, component=None, show_vectors=True, show_contour=True, **kwargs):
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
        if not self.displacement_field:
            raise ValueError("No displacement field results available for this step")

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.add_model(self.model, fast=fast, show_parts=True, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        viewer.add_displacement_field(self.displacement_field, fast=fast, model=self.model, component=component, show_vectors=show_vectors, show_contour=show_contour, **kwargs)
        if show_loads:
            viewer.add_step(self, show_loads=show_loads)
        viewer.show()
        viewer.scene.clear()

    def show_reactions(self, fast=True, show_bcs=1, scale_model=1, show_loads=0.1, component=None, show_vectors=1, show_contour=False, **kwargs):
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
        if not self.reaction_field:
            raise ValueError("No reaction field results available for this step")

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.add_model(self.model, fast=fast, show_parts=True, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        viewer.add_reaction_field(self.reaction_field, fast=fast, model=self.model, component=component, show_vectors=show_vectors, show_contour=show_contour, **kwargs)

        if show_loads:
            viewer.add_step(self, show_loads=show_loads)
        viewer.show()
        viewer.scene.clear()

    def show_stress(self, fast=True, show_bcs=1, scale_model=1, show_loads=0.1, component=None, show_vectors=1, show_contour=False, plane="mid", **kwargs):

        if not self.stress2D_field:
            raise ValueError("No reaction field results available for this step")

        viewer = FEA2Viewer(center=self.model.center, scale_model=scale_model)
        viewer.add_model(self.model, fast=fast, show_parts=True, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        viewer.add_stress2D_field(
            self.stress2D_field, fast=fast, model=self.model, component=component, show_vectors=show_vectors, show_contour=show_contour, plane=plane, **kwargs
        )

        if show_loads:
            viewer.add_step(self, show_loads=show_loads)
        viewer.show()
        viewer.scene.clear()
