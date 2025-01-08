from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas_fea2.problem.displacements import GeneralDisplacement
from compas_fea2.problem.fields import _PrescribedField
from compas_fea2.problem.loads import Load
from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput

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
    Steps can be introduced for example to change the output requests or to change
    loads, boundary conditions, analysis procedure, etc. There is no limit on the
    number of steps in an analysis.

    Developer-only class.

    """

    def __init__(self, name=None, **kwargs):
        super(Step, self).__init__(name=name, **kwargs)
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
        return self.problem._registration

    @property
    def field_outputs(self):
        return self._field_outputs

    @property
    def load_cases(self):
        return self._load_cases

    @property
    def patterns(self):
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
        for pattern in self.patterns:
            if pattern.load_case in combination.load_cases:
                factor = combination.factors[pattern.load_case]
                for node, load in pattern.node_load:
                    factored_load = factor * load

                    node.loads.setdefault(self, {}).setdefault(combination, {})[pattern] = factored_load
                    if node.total_load:
                        node.total_load += factored_load
                    else:
                        node.total_load = factored_load

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
        #FIXME: this is a hack  - need to fix this
        # if isinstance(output, FieldOutput):
        #     self._field_outputs.add(output)
        # elif isinstance(output, HistoryOutput):
        #     self._history_outputs.add(output)
        # else:
        #     raise TypeError("{!r} is not an _Output.".format(output))
        return output

    # ==========================================================================
    #                             Results methods
    # ==========================================================================


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

    def __init__(self, max_increments, initial_inc_size, min_inc_size, time, nlgeom=False, modify=False, restart=False, name=None, **kwargs):
        super(GeneralStep, self).__init__(name=name, **kwargs)

        self._max_increments = max_increments
        self._initial_inc_size = initial_inc_size
        self._min_inc_size = min_inc_size
        self._time = time
        self._nlgeom = nlgeom
        self._modify = modify
        self._restart = restart

    @property
    def displacements(self):
        return list(filter(lambda p: isinstance(p.load, GeneralDisplacement), self._patterns))

    @property
    def loads(self):
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
