from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from copy import deepcopy
from importlib.metadata import metadata
from json import load
from typing import Type
import compas_fea2

from compas_fea2.base import FEAData

from compas_fea2.model.nodes import Node
from compas_fea2.model.elements import _Element

from compas_fea2.problem.loads import _Load
from compas_fea2.problem.loads import GravityLoad
from compas_fea2.problem.loads import PointLoad

from compas_fea2.problem.patterns import Pattern

from compas_fea2.problem.displacements import GeneralDisplacement

from compas_fea2.problem.fields import _PrescribedField
from compas_fea2.problem.fields import PrescribedTemperatureField

from compas_fea2.problem.outputs import _Output
from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput

from compas.geometry import Vector
from compas.geometry import sum_vectors
from compas_fea2.utilities._utils import timer

import copy

# ==============================================================================
#                                Base Steps
# ==============================================================================


class _Step(FEAData):
    """Initialises base Step object.

    Note
    ----
    Stpes are registered to a :class:`compas_fea2.problem.Problem`.

    Note
    ----
    A ``compas_fea2`` analysis is based on the concept of ``steps``,
    which are the sequence of modification of the state of the model. Steps
    can be introduced for example to change the output requests or to change loads,
    boundary conditions, analysis procedure, etc. There is no limit on the number
    of steps in an analysis.

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

    """

    def __init__(self, name=None, problem=None, **kwargs):
        super(_Step, self).__init__(name=name, **kwargs)
        self._problem = problem
        self._field_outputs = set()
        self._history_outputs = set()
        self._results = None

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
    def history_outputs(self):
        return self._history_outputs

    @property
    def results(self):
        return self._results

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
        if isinstance(output, FieldOutput):
            self._field_outputs.add(output)
        elif isinstance(output, HistoryOutput):
            self._history_outputs.add(output)
        else:
            raise TypeError('{!r} is not an _Output.'.format(output))
        return output

    # ==========================================================================
    #                             Results methods
    # ==========================================================================
    @timer(message='Step results copied in the model in ')
    def _store_results_in_model(self, fields=None):
        """Copy the results for the step in the model object at the nodal and
        element level.

        Parameters
        ----------
        results : dict
            results dictionary.

        Returns
        -------
        None

        """
        from compas_fea2.results.sql_wrapper import create_connection, get_database_table, get_all_field_results
        import sqlalchemy as db

        engine, connection, metadata = create_connection(self.problem.path_results)
        FIELDS = get_database_table(engine, metadata, 'fiedls')
        if not fields:
            field_column = FIELDS.query.all()
            fields=[field for field in field_column.field]

        for field in fields:
            field_table = get_database_table(engine, metadata, field)
            _, results = get_all_field_results(engine, metadata, field, field_table)
            for row in results:
                part = self.problem.model.find_part_by_name(row[0])
                if row[2] == 'NODAL':
                    node_element = part.find_node_by_key(row[3])
                else:
                    raise NotImplementedError('elements not supported yet')

                node_element._results.setdefault(self.problem, {})[self] = res_field


        step_results = results[self.name]
        # Get part results
        for part_name, part_results in step_results.items():
            # Get node/element results
            for result_type, nodes_elements_results in part_results.items():
                if result_type not in ['nodes', 'elements']:
                    continue
                # nodes_elements = getattr(self.model.find_part_by_name(part_name, casefold=True), result_type)
                func = getattr(self.model.find_part_by_name(part_name, casefold=True),
                               'find_{}_by_key'.format(result_type[:-1]))
                # Get field results
                for key, res_field in nodes_elements_results.items():
                    node_element = func(key)
                    if not node_element:
                        continue
                    if fields and not res_field in fields:
                        continue
                    node_element._results.setdefault(self.problem, {})[self] = res_field

# ==============================================================================
#                                General Steps
# ==============================================================================


class _GeneralStep(_Step):
    """General Step object for use in a general static, dynamic or
    multiphysics analysis.

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
        super(_GeneralStep, self).__init__(name=name, **kwargs)

        self._max_increments = max_increments
        self._initial_inc_size = initial_inc_size
        self._min_inc_size = min_inc_size
        self._time = time
        self._nlgeom = nlgeom
        self._modify = modify
        self._restart = restart

        self._patterns = set()

    def __rmul__(self, other):
        if not isinstance(other, (float, int)):
            raise TypeError('Step multiplication only allowed with real numbers')
        step_copy = copy.copy(self)
        step_copy._patterns = set()
        for pattern in self._patterns:
            pattern_copy = copy.copy(pattern)
            load_copy = copy.copy(pattern.load)
            pattern_copy._load = other*load_copy
            step_copy.add_pattern(pattern_copy)
        return step_copy

    @property
    def displacements(self):
        return list(filter(lambda p: isinstance(p.load, GeneralDisplacement), self._patterns))

    @property
    def loads(self):
        return list(filter(lambda p: isinstance(p.load, _Load), self._patterns))

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

    # =========================================================================
    #                           Loads methods
    # =========================================================================

    def add_pattern(self, load_pattern):
        # type: (_Load, Node | _Element) -> _Load
        """Add a general load pattern to the Step object.

        Warning
        -------
        The *load* and the *keys* must be consistent (you should not assing a
        line load to a node). Consider using specific methods to assign load,
        such as ``add_point_load``, ``add_line_load``, etc.

        Parameters
        ----------
        load : obj
            any ``compas_fea2`` :class:`compas_fea2.problem._Load` subclass object
        location : var
            Location where the load is applied

        Returns
        -------
        None
        """

        if not isinstance(load_pattern, Pattern):
            raise TypeError('{!r} is not a LoadPattern.'.format(load_pattern))

        if self.problem:
            if self.model:
                if not list(load_pattern.distribution).pop().model == self.model:
                    raise ValueError('The load pattern is applied to a valid reagion of {!r}'.format(self.model))

        # store location in step
        self._patterns.add(load_pattern)
        load_pattern._registration = self

        return load_pattern

    def add_patterns(self, load_patterns):
        # type: (_Load, Node | _Element) -> list(_Load)
        """Add a load to multiple locations.

        Parameters
        ----------
        load : :class:`_Load`
            Load to assign to the node
        location : [var]
            Locations where the load is applied

        Returns
        -------
        load : [:class:`_Load`]
            Load to assign to the node
        """
        return [self.add_pattern(load_pattern) for load_pattern in load_patterns]
