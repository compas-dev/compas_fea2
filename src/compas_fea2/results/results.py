from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Iterable

from compas.geometry import Vector
from compas_fea2.base import FEAData

from .sql_wrapper import get_field_results, get_field_labels, get_database_table, create_connection


class Results(FEAData):
    """Results object. This ensures that the results from all
    the backends are consistent.

    Parameters
    ----------
    location : var
        location of the result
    value : var

    Notes
    -----
    Results are registered to a :class:`compas_fea2.problem.Problem`.

    """

    def __init__(self, location, components, invariants, name=None, **kwargs):
        super(Results, self).__init__(name=name, **kwargs)
        self._location = location
        self._components = components
        self._invariants = invariants

    @property
    def components(self):
        return self._components

    @property
    def invariants(self):
        return self._invariants

    @property
    def location(self):
        return self._location

    @property
    def vector(self):
        if len(self.components) == 3:
            return Vector(*list(self.components.values()))

    @property
    def value(self):
        return self.vector.length

    def to_file(self, *args, **kwargs):
        raise NotImplementedError("this function is not available for the selected backend")


class FieldResults(FEAData):
    def __init__(self, field_name, step, name=None, *args, **kwargs):
        super(FieldResults, self).__init__(name, *args, **kwargs)
        self._registration = step
        self._db_connection = create_connection(self.problem.path_db)
        self._field_name = field_name
        self._components = get_field_labels(*self.db_connection, self.field_name, "components")
        self._invariants = get_field_labels(*self.db_connection, self.field_name, "invariants")

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step.problem

    @property
    def model(self):
        return self.problem.model

    @property
    def db_connection(self):
        return self._db_connection

    @db_connection.setter
    def db_connection(self, path_db):
        self._db_connection = create_connection(path_db)

    def _get_field_results(self, field):
        """_summary_

        Parameters
        ----------
        field : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        engine, connection, metadata = self.db_connection
        TABLE = get_database_table(engine, metadata, field)
        test = [TABLE.columns.step == self.step.name]
        # if hasattr(TABLE.columns, 'magnitude'):
        #     test.append(TABLE.columns.magnitude != 0.)
        return get_field_results(engine, connection, metadata, TABLE, test)

    def _get_func_field_sql(self, func, field, group_by, component):
        """Filter the results with a specific function (e.g. MAX, MIN, etc.)"""
        steps = [self.step]  # FIXME remove the list
        engine, connection, metadata = self.db_connection
        labels = ["part", "position", "key"] + self._components + self._invariants
        labels[labels.index(component)] = "{}({})".format(func, component)
        sql = """SELECT {}
FROM {}
WHERE step IN ({})
GROUP BY {};""".format(
            ", ".join(labels), field, ", ".join(["'{}'".format(step.name) for step in steps]), group_by
        )
        ResultProxy = connection.execute(sql)
        ResultSet = ResultProxy.fetchall()
        return ResultProxy, (labels, ResultSet)


class NodeFieldResults(FieldResults):
    def __init__(self, field_name, step, name=None, *args, **kwargs):
        super(NodeFieldResults, self).__init__(field_name, step, name, *args, **kwargs)
        self._results = self._link_field_results_to_model(self._get_field_results(field=self.field_name)[1])
        if len(self.results) != len(self.model.nodes):
            raise ValueError('The requested field is not defined at the nodes. Try "show_elements_field" instead".')
        self._max_components = {c: self._get_limit("MAX", component=c)[0] for c in self._components}
        self._min_components = {c: self._get_limit("MIN", component=c)[0] for c in self._components}
        self._max_invariants = {c: self._get_limit("MAX", component=c)[0] for c in self._invariants}
        self._min_invariants = {c: self._get_limit("MIN", component=c)[0] for c in self._invariants}

    @property
    def field_name(self):
        return self._field_name

    @property
    def components(self):
        return self._components

    @property
    def invariants(self):
        return self._invariants

    @property
    def results(self):
        return self._results

    @property
    def max(self):
        return self._max_invariants["magnitude"][0]

    @property
    def min(self):
        return self._min_invariants["magnitude"][0]

    def _link_field_results_to_model(self, field_results):
        """Converts the values of the results string to actual nodes of the
        model.

        Parameters
        ----------
        model : :class:`compas_fea2.model.Model`
            The model.
        ResultSet : _type_
            _description_

        Returns
        -------
        dict, class:`compas.geoemtry.Vector`
            Dictionary with {'part':..; 'node':..; 'vector':...} and resultant vector
        """
        # _, field_results = self._get_field_results(self.field_name)
        col_names = field_results[0]
        values = field_results[1]
        if not values:
            raise ValueError("No results found")
        results = []
        for row in values:
            result = {}
            part = self.model.find_part_by_name(row[0])
            if not part:
                # try case insensitive match
                part = self.model.find_part_by_name(row[0], casefold=True)
            if not part:
                print("Part {} not found in model".format(row[0]))
                continue
            result = Results(
                location=part.find_node_by_key(row[2]),
                components={col_names[i]: row[i] for i in range(3, len(self.components) + 3)},
                invariants={col_names[i]: row[i] for i in range(len(self.components) + 3, len(row))},
            )
            results.append(result)
        return results

    def _get_limit(self, limit="MAX", component="magnitude"):
        if component not in self.components + self.invariants:
            raise ValueError(
                "The specified component is not valid. Choose from {}".format(self._components + self.invariants)
            )
        _, field_results = self._get_func_field_sql(
            func=limit, field=self.field_name, group_by="step", component=component
        )
        return self._link_field_results_to_model(field_results=field_results)

    def get_value_at_nodes(self, nodes):
        """Get the displacement of a list of :class:`compas_fea2.model.Node`.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node` | [:class:`compas_fea2.model.Node`]
            The node or the nodes where to retrieve the displacmeent
        steps : _type_, optional
            _description_, by default None

        Returns
        -------
        dict
            Dictionary with {'part':..; 'node':..; 'vector':...}

        """
        if not isinstance(nodes, Iterable):
            nodes = [nodes]
        steps = [self.step]
        field = self.field_name
        group_by = "step"
        engine, connection, metadata = self.db_connection
        components = get_field_labels(engine, connection, metadata, field, "components")
        invariants = get_field_labels(engine, connection, metadata, field, "invariants")
        labels = ["part", "position", "key"] + components + invariants

        sql = """SELECT {}
FROM {}
WHERE step IN ({}) AND key  in ({})
GROUP BY {};""".format(
            ", ".join(labels),
            field,
            ", ".join(["'{}'".format(step.name) for step in steps]),
            ", ".join(["'{}'".format(node.key) for node in nodes]),
            group_by,
        )
        ResultProxy = connection.execute(sql)
        ResultSet = ResultProxy.fetchall()
        value, _ = self._link_field_results_to_model((labels, ResultSet))
        return value

    def get_value_at_point(self, point, distance, plane=None, steps=None, group_by=["step", "part"]):
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
        steps = [self.step]
        node = self.model.find_node_by_location(point, distance, plane=None)
        return self.get_value_at_nodes(nodes=[node], steps=steps, group_by=group_by)


# class DisplacementFieldResults(NodeFieldResults):
#     def __init__(self, step, name=None, *args, **kwargs):
#         self._field_name = "U"
#         self._components = ["U1", "U2", "U3"]
#         self._invariants = ["magnitude"]
#         super(DisplacementFieldResults, self).__init__(step, name, *args, **kwargs)

#     @property
#     def max(self):
#         return self._max_invariants['magnitude'][0]
#     @property
#     def min(self):
#         return self._min_invariants['magnitude'][0]
