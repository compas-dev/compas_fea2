from typing import Iterable
import numpy as np
import matplotlib.pyplot as plt

from compas.geometry import Vector, Frame
from compas.geometry import Transformation, Rotation

import compas_fea2
from compas_fea2.base import FEAData

from compas_fea2.model import _Element
from compas_fea2.model import ElasticIsotropic
from .results import (DisplacementResult,
                      ShellStressResult,
                      SolidStressResult,
                      ReactionResult)

from .sql_wrapper import get_field_results, get_field_labels, get_database_table, create_connection


class FieldResults(FEAData):
    """FieldResults object. This is a collection of Result objects that define a field.
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
    FieldResults are registered to a :class:`compas_fea2.problem._Step`.

    """
    def __init__(self, field_name, step, name=None, *args, **kwargs):
        super(FieldResults, self).__init__(name, *args, **kwargs)
        self._results = None
        self._registration = step
        self._db_connection = create_connection(self.problem.path_db)
        self._field_name = field_name
        self._components_lables = get_field_labels(*self.db_connection, self.field_name, "components")
        self._invariants_labels = get_field_labels(*self.db_connection, self.field_name, "invariants")

    @property
    def results(self):
        return self._results

    @property
    def field_name(self):
        return self._field_name

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

    @property
    def components_labels(self):
        return self._components_lables

    @property
    def invariants_labels(self):
        return self._invariants_labels

    @property
    def max(self):
        return self.max_invariants["magnitude"]

    @property
    def min(self):
        return self.min_invariants["magnitude"]

    @property
    def max_components(self):
        return {c: self._get_limit("MAX", component=c)[0] for c in self._components_lables}

    @property
    def min_components(self):
        return {c: self._get_limit("MIN", component=c)[0] for c in self._components_lables}

    @property
    def max_invariants(self):
        return {c: self._get_limit("MAX", component=c)[0] for c in self._invariants_labels}

    @property
    def min_invariants(self):
        return {c: self._get_limit("MIN", component=c)[0] for c in self._invariants_labels}

    def _get_field_results(self, field_name):
        """Create the connection to the SQLite database and retrieve
        the Results at each location of the field.

        Parameters
        ----------
        field : str
            The name of the field.

        Returns
        -------
        _type_
            _description_
        """
        engine, connection, metadata = self.db_connection
        TABLE = get_database_table(engine, metadata, field_name)
        test = [TABLE.columns.step == self.step.name]
        return get_field_results(engine, connection, metadata, TABLE, test)

    def _get_func_field_sql(self, func, field, group_by, component):
        """Filter the results with a specific function (e.g. MAX, MIN, etc.)"""
        steps = [self.step]  # FIXME remove the list
        engine, connection, metadata = self.db_connection
        labels = ["part", "position", "key"] + self._components_lables + self._invariants_labels
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

    def _link_field_results_to_model(self, field_results):
        """Converts the values of the results string to actual nodes of the
        model.

        Parameters
        ----------
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

            func = part.find_node_by_key if isinstance(self, NodeFieldResults) else part.find_element_by_key

            if self.field_name.upper() == 'U':
                cls = DisplacementResult
            elif self.field_name.upper() == 'RF':
                cls = ReactionResult
            elif self.field_name.upper() == 'S2D':
                cls = ShellStressResult
            elif self.field_name.upper() == 'S3D':
                cls = SolidStressResult
            else:
                raise NotImplementedError(f"{self.field_name} not implemented")

            result = cls.from_components(
                location=func(row[2]),
                components={col_names[i]: row[i] for i in range(3, len(self.components_labels) + 3)},
                # invariants={col_names[i]: row[i] for i in range(len(self.components_labels) + 3, len(row))},
            )
            results.append(result)
        return results

    def _get_limit(self, limit="MAX", component="magnitude"):
        if component not in self.components_labels + self.invariants_labels:
            raise ValueError(
                "The specified component is not valid. Choose from {}".format(self._components_lables + self.invariants_labels)
            )
        _, field_results = self._get_func_field_sql(
            func=limit, field=self.field_name, group_by="step", component=component
        )
        return self._link_field_results_to_model(field_results=field_results)

    def get_value_at_location(self, location):
        """Get the displacement of a list of :class:`compas_fea2.model.Node`.

        Parameters
        ----------
        location : [:class:`compas_fea2.model.Node`] | []:class:`compas_fea2.model._Element`]
            The node or the nodes where to retrieve the displacmeent

        Returns
        -------
        dict
            Dictionary with {'part':..; 'node':..; 'vector':...}

        """
        if not isinstance(location, Iterable):
            location = [location]
        steps = [self.step]
        group_by = "step"
        engine, connection, metadata = self.db_connection
        components = get_field_labels(engine, connection, metadata, self.field_name, "components")
        invariants = get_field_labels(engine, connection, metadata, self.field_name, "invariants")
        labels = ["part", "position", "key"] + components + invariants

        sql = """SELECT {}
FROM {}
WHERE step IN ({}) AND key  in ({})
GROUP BY {};""".format(
            ", ".join(labels),
            self.field_name,
            ", ".join(["'{}'".format(step.name) for step in steps]),
            ", ".join(["'{}'".format(node.key) for node in location]),
            group_by,
        )
        ResultProxy = connection.execute(sql)
        ResultSet = ResultProxy.fetchall()
        value, _ = self._link_field_results_to_model(field_results=(labels, ResultSet))
        return value


class NodeFieldResults(FieldResults):
    def __init__(self, field_name, step, name=None, *args, **kwargs):
        super(NodeFieldResults, self).__init__(field_name, step, name, *args, **kwargs)
        self._results = self._link_field_results_to_model(self._get_field_results(field_name=self.field_name)[1])
        if len(self.results) != len(self.model.nodes_set):
            raise ValueError('The requested field is not defined at the nodes. Try "show_elements_field" instead".')


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
        return self.get_value_at_location(location=[node], steps=steps, group_by=group_by)




class ElementFieldResults(FieldResults):
    def __init__(self, field_name, step, name=None, *args, **kwargs):
        super(ElementFieldResults, self).__init__(field_name, step, name, *args, **kwargs)
        self._results = self._link_field_results_to_model(self._get_field_results(field_name=self.field_name)[1])

    def compute_principal_stresses():
        pass
