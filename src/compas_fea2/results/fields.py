from typing import Iterable

from compas_fea2.base import FEAData
from compas_fea2.model import _Element2D
from compas_fea2.model import _Element3D

from .results import DisplacementResult
from .results import ReactionResult
from .results import ShellStressResult
from .results import SolidStressResult


class FieldResults(FEAData):
    """FieldResults object. This is a collection of Result objects that define a field.

    The objects uses SQLite queries to efficiently retrieve the results from the results database.

    The field results are defined over multiple steps

    You can use FieldResults to visualise a field over a part or the model, or to compute
    global quantiies, such as maximum or minimum values.

    Parameters
    ----------
    field_name : str
        Name of the field.
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    field_name : str
        Name of the field.
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.
    problem : :class:`compas_fea2.problem.Problem`
        The Problem where the Step is registered.
    model : :class:`compas_fea2.problem.Model
        The Model where the Step is registered.
    db_connection : :class:`sqlite3.Connection` | None
        Connection object or None
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.

    Notes
    -----
    FieldResults are registered to a :class:`compas_fea2.problem.Problem`.

    """

    def __init__(self, problem, field_name, name=None, *args, **kwargs):
        super(FieldResults, self).__init__(name, *args, **kwargs)
        self._registration = problem
        self._field_name = field_name
        self._table = self.problem.results_db.get_table(field_name)
        self._components_names = None
        self._invariants_names = None
        self._results_class = None
        self._results_func = None

    @property
    def field_name(self):
        return self._field_name

    @property
    def problem(self):
        return self._registration

    @property
    def model(self):
        return self.problem.model

    @property
    def rdb(self):
        return self.problem.results_db

    @property
    def components_names(self):
        return self._components_names

    @property
    def invariants_names(self):
        return self._invariants_names

    @property
    def results_columns(self):
        return ["step", "part", "key"] + self.components_names

    def _get_db_results(self, members, steps):
        """Get the results for the given members and steps in the database
        format.

        Parameters
        ----------
        members : _type_
            _description_
        steps : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if not isinstance(members, Iterable):
            members = [members]
        if not isinstance(steps, Iterable):
            steps = [steps]

        members_keys = set([member.key for member in members])
        parts_names = set([member.part.name for member in members])
        steps_names = set([step.name for step in steps])

        if isinstance(members[0], _Element3D):
            columns = ["step", "part", "key"] + self._components_names_3d
            field_name = self._field_name_3d
        elif isinstance(members[0], _Element2D):
            columns = ["step", "part", "key"] + self._components_names_2d
            field_name = self._field_name_2d
        else:
            columns = ["step", "part", "key"] + self._components_names
            field_name = self._field_name

        results_set = self.rdb.get_rows(field_name, columns, {"key": members_keys, "part": parts_names, "step": steps_names})
        return results_set

    def _to_result(self, results_set):
        """Convert a set of results in database format to the appropriate
        result object.

        Parameters
        ----------
        results_set : _type_
            _description_

        Returns
        -------
        dic
            Dictiorany grouping the results per Step.
        """
        results = {}
        for r in results_set:
            step = self.problem.find_step_by_name(r[0])
            results.setdefault(step, [])
            part = self.model.find_part_by_name(r[1]) or self.model.find_part_by_name(r[1], casefold=True)
            if not part:
                raise ValueError(f"Part {r[1]} not in model")
            m = getattr(part, self._results_func)(r[2])
            results[step].append(self._results_class(m, *r[3:]))
        return results

    def get_results(self, members, steps):
        """Get the results for the given members and steps.

        Parameters
        ----------
        members : _type_
            _description_
        steps : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        results_set = self._get_db_results(members, steps)
        return self._to_result(results_set)

    def get_max_component(self, component, step):
        """Get the result where a component is maximum for a given step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        :class:`compas_fea2.results.Result`
            The appriate Result object.
        """
        results_set = self.rdb.get_func_row(self.field_name, self.field_name + str(component), "MAX", {"step": [step.name]}, self.results_columns)
        return self._to_result(results_set)[step][0]

    def get_min_component(self, component, step):
        results_set = self.rdb.get_func_row(self.field_name, self.field_name + str(component), "MIN", {"step": [step.name]}, self.results_columns)
        return self._to_result(results_set)[step][0]

    def get_limits_component(self, component, step):
        """Get the result objects with the min and max value of a given
        component in a step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return [self.get_min_component(component, step), self.get_max_component(component, step)]

    def get_limits_absolute(self, step):
        limits = []
        for func in ["MIN", "MAX"]:
            limits.append(self.rdb.get_func_row(self.field_name, "magnitude", func, {"step": [step.name]}, self.results_columns))
        return [self._to_result(limit)[step][0] for limit in limits]

    def get_results_at_point(self, point, distance, plane=None, steps=None):
        """Get the displacement of the model around a location (point).

        Parameters
        ----------
        point : [float]
            The coordinates of the point.
        steps : _type_, optional
            _description_, by default None

        Returns
        -------
        dict
            Dictionary with {step: result}

        """
        nodes = self.model.find_nodes_around_point(point, distance, plane)
        if not nodes:
            print(f"WARNING: No nodes found at {point} within {distance}")
        else:
            results = []
            steps = steps or self.problem.steps
            results = self.get_results(nodes, steps)
            return results


class DisplacementFieldResults(FieldResults):
    """Displacement field.

    Parameters
    ----------
    FieldResults : _type_
        _description_
    """

    def __init__(self, problem, name=None, *args, **kwargs):
        super(DisplacementFieldResults, self).__init__(problem=problem, field_name="U", name=name, *args, **kwargs)
        self._components_names = ["U1", "U2", "U3"]
        self._invariants_names = ["magnitude"]
        self._results_class = DisplacementResult
        self._results_func = "find_node_by_key"

    def results(self, step):
        nodes = self.model.nodes
        return self.get_results(nodes, steps=step)[step]


class ReactionFieldResults(FieldResults):
    """Reaction field.

    Parameters
    ----------
    FieldResults : _type_
        _description_
    """

    def __init__(self, problem, name=None, *args, **kwargs):
        super(ReactionFieldResults, self).__init__(problem=problem, field_name="RF", name=name, *args, **kwargs)
        self._components_names = ["RF1", "RF2", "RF3"]
        self._invariants_names = ["magnitude"]
        self._results_class = ReactionResult
        self._results_func = "find_node_by_key"

    def results(self, step):
        nodes = self.model.nodes
        return self.get_results(nodes, steps=step)[step]


class StressFieldResults(FEAData):
    """_summary_

    Parameters
    ----------
    FieldResults : _type_
        _description_
    """

    def __init__(self, problem, name=None, *args, **kwargs):
        super(StressFieldResults, self).__init__(name, *args, **kwargs)
        self._registration = problem
        self._components_names_2d = ["S11", "S22", "S12", "M11", "M22", "M12"]
        self._components_names_3d = ["S11", "S22", "S23", "S12", "S13", "S33"]
        self._field_name_2d = "S2D"
        self._field_name_3d = "S3D"
        self._results_class_2d = ShellStressResult
        self._results_class_3d = SolidStressResult
        self._results_func = "find_element_by_key"

    @property
    def field_name(self):
        return self._field_name

    @property
    def problem(self):
        return self._registration

    @property
    def model(self):
        return self.problem.model

    @property
    def rdb(self):
        return self.problem.results_db

    @property
    def components_names(self):
        return self._components_names

    @property
    def invariants_names(self):
        return self._invariants_names

    def _get_db_results(self, members, steps):
        """Get the results for the given members and steps in the database
        format.

        Parameters
        ----------
        members : _type_
            _description_
        steps : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if not isinstance(members, Iterable):
            members = [members]
        if not isinstance(steps, Iterable):
            steps = [steps]

        members_keys = set([member.key for member in members])
        parts_names = set([member.part.name for member in members])
        steps_names = set([step.name for step in steps])

        if isinstance(members[0], _Element3D):
            columns = ["step", "part", "key"] + self._components_names_3d
            field_name = self._field_name_3d
        elif isinstance(members[0], _Element2D):
            columns = ["step", "part", "key"] + self._components_names_2d
            field_name = self._field_name_2d
        else:
            raise ValueError("Not an element")

        results_set = self.rdb.get_rows(field_name, columns, {"key": members_keys, "part": parts_names, "step": steps_names})
        return results_set

    def _to_result(self, results_set):
        """Convert a set of results in database format to the appropriate
        result object.

        Parameters
        ----------
        results_set : _type_
            _description_

        Returns
        -------
        dic
            Dictiorany grouping the results per Step.
        """
        results = {}
        for r in results_set:
            step = self.problem.find_step_by_name(r[0])
            results.setdefault(step, [])
            part = self.model.find_part_by_name(r[1]) or self.model.find_part_by_name(r[1], casefold=True)
            if not part:
                raise ValueError(f"Part {r[1]} not in model")
            m = getattr(part, self._results_func)(r[2])
            if isinstance(m, _Element3D):
                cls = self._results_class_3d
                columns = self._components_names_3d
            else:
                cls = self._results_class_2d
                columns = self._components_names_2d
            values = {k.lower(): v for k, v in zip(columns, r[3:])}
            results[step].append(cls(m, **values))
        return results

    def get_results(self, members, steps):
        """Get the results for the given members and steps.

        Parameters
        ----------
        members : _type_
            _description_
        steps : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        results_set = self._get_db_results(members, steps)
        return self._to_result(results_set)

    def get_max_component(self, component, step):
        """Get the result where a component is maximum for a given step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        :class:`compas_fea2.results.Result`
            The appriate Result object.
        """
        results_set = self.rdb.get_func_row(self.field_name, self.field_name + str(component), "MAX", {"step": [step.name]}, self.results_columns)
        return self._to_result(results_set)[step][0]

    def get_min_component(self, component, step):
        results_set = self.rdb.get_func_row(self.field_name, self.field_name + str(component), "MIN", {"step": [step.name]}, self.results_columns)
        return self._to_result(results_set)[step][0]

    def get_limits_component(self, component, step):
        """Get the result objects with the min and max value of a given
        component in a step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return [self.get_min_component(component, step), self.get_max_component(component, step)]

    def get_limits_absolute(self, step):
        limits = []
        for func in ["MIN", "MAX"]:
            limits.append(self.rdb.get_func_row(self.field_name, "magnitude", func, {"step": [step.name]}, self.results_columns))
        return [self._to_result(limit)[step][0] for limit in limits]

    def get_results_at_point(self, point, distance, plane=None, steps=None):
        """Get the displacement of the model around a location (point).

        Parameters
        ----------
        point : [float]
            The coordinates of the point.
        steps : _type_, optional
            _description_, by default None

        Returns
        -------
        dict
            Dictionary with {'part':..; 'node':..; 'vector':...}

        """
        nodes = self.model.find_nodes_around_point(point, distance, plane)
        results = []
        for step in steps:
            results.append(self.get_results(nodes, steps)[step])

    # @property
    # def results_columns(self):
    #     return ["step", "part", "key"]+self.components_names

    def results(self, step):
        elements = self.model.elements
        return self.get_results(elements, steps=step)[step]
