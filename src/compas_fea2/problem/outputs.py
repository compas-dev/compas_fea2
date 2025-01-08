from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import chain

from compas_fea2.base import FEAData
import os
import sqlite3


class _Output(FEAData):
    """Base class for output requests.

    Parameters
    ----------
    FEAData : _type_
        _description_

    Notes
    -----
    Outputs are registered to a :class:`compas_fea2.problem.Step`.

    """

    def __init__(self, title, description, components, invariants, **kwargs):
        super(_Output, self).__init__(**kwargs)
        self._title = title
        self._description = description
        self._components = components
        self._invariants = invariants

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step._registration

    @property
    def model(self):
        return self.problem._registration

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def components(self):
        return self._components

    @property
    def invariants(self):
        return self._invariants

    @classmethod
    def get_sqltable_schema(cls):
        """
        Returns a dictionary describing the SQL table structure
        for this output type. Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must define their table schema.")

    @classmethod
    def get_jsontable_schema(cls):
        """
        Returns a JSON-like dict describing the SQL table structure
        for this output type. Subclasses should override.
        """
        raise NotImplementedError("Subclasses must define their table schema.")

    def create_table_for_output_class(self, connection, results):
        """
        Reads the table schema from `output_cls.get_table_schema()`
        and creates the table in the given database.

        Parameters
        ----------
        database_path : str
            Path to the folder where the database is located
        database_name : str
            Name of the database file, e.g. 'results.db'
        output_cls : _Output subclass
            A class like NodeOutput that implements `get_table_schema()`
        """

        cursor = connection.cursor()

        schema = self.get_sqltable_schema()
        table_name = schema["table_name"]
        columns_info = schema["columns"]

        # Build CREATE TABLE statement:
        columns_sql = []
        for col_name, col_def in columns_info:
            columns_sql.append(f"{col_name} {col_def}")
        columns_sql_str = ", ".join(columns_sql)
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql_str})"
        cursor.execute(create_sql)
        connection.commit()

        # Skip PRIMARY KEY columns
        insert_columns = [col_name for (col_name, col_def) in columns_info if "PRIMARY KEY" not in col_def.upper()]
        col_names_str = ", ".join(insert_columns)
        placeholders_str = ", ".join(["?"] * len(insert_columns))
        sql = f"INSERT INTO {table_name} ({col_names_str}) VALUES ({placeholders_str})"

        # Build a list of tuples from rows_data
        cursor.executemany(sql, results)
        connection.commit()

class _NodeFieldOutput(_Output):
    """NodeFieldOutput object for requesting the fields at the nodes from the analysis."""


class _ElementFieldOutput(_Output):
    """ElementFieldOutput object for requesting the fields at the elements from the analysis."""


class DisplacementFieldOutput(_NodeFieldOutput):
    """DisplacmentFieldOutput object for requesting the displacements at the nodes
    from the analysis."""

    def __init__(self, **kwargs):
        super(DisplacementFieldOutput, self).__init__("u", "Displacement field output", ["ux", "uy", "uz", "uxx", "uyy", "uzz"], ["magnitude"], **kwargs)

    @classmethod
    def get_sqltable_schema(cls):
        """
        Return a dict describing the table name and each column
        (column_name, column_type, constraints).
        """
        return {
            "table_name": "u",
            "columns": [
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("input_key", "INTEGER"),
                ("step", "TEXT"),
                ("part", "TEXT"),
                ("ux", "REAL"),
                ("uy", "REAL"),
                ("uz", "REAL"),
                ("uxx", "REAL"),
                ("uyy", "REAL"),
                ("uzz", "REAL"),
            ],
        }

    @classmethod
    def get_jsontable_schema(cls):
        """
        Return a dict describing the table name and columns in JSON-like format.
        """
        return {
            "table_name": "node_output",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True, "autoincrement": True},
                {"name": "node_key", "type": "INTEGER"},
                {"name": "ux", "type": "REAL"},
                {"name": "uy", "type": "REAL"},
                {"name": "uz", "type": "REAL"},
                {"name": "uxx", "type": "REAL"},
                {"name": "uyy", "type": "REAL"},
                {"name": "uzz", "type": "REAL"},
            ],
        }



class ReactionFieldOutput(_NodeFieldOutput):
    """ ReactionFieldOutput object for requesting the reaction forces at the nodes
    from the analysis."""
    
    def __init__(self, **kwargs):
        super(ReactionFieldOutput, self).__init__("rf", "Reaction field output", ["rfx", "rfy", "rfz", "rfxx", "rfyy", "rfzz"], ["magnitude"], **kwargs)

    @classmethod
    def get_sqltable_schema(cls):
        """
        Return a dict describing the table name and each column
        (column_name, column_type, constraints).
        """
        return {
            "table_name": "rf",
            "columns": [
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("input_key", "INTEGER"),
                ("step", "TEXT"),
                ("part", "TEXT"),
                ("rfx", "REAL"),
                ("rfy", "REAL"),
                ("rfz", "REAL"),
                ("rfxx", "REAL"),
                ("rfyy", "REAL"),
                ("rfzz", "REAL"),
            ],
        }

    @classmethod
    def get_jsontable_schema(cls):
        """
        Return a dict describing the table name and columns in JSON-like format.
        """
        return {
            "table_name": "node_output",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True, "autoincrement": True},
                {"name": "node_key", "type": "INTEGER"},
                {"name": "rx", "type": "REAL"},
                {"name": "ry", "type": "REAL"},
                {"name": "rz", "type": "REAL"},
                {"name": "rxx", "type": "REAL"},
                {"name": "ryy", "type": "REAL"},
                {"name": "rzz", "type": "REAL"},
            ],
        }
        
class StressFieldOutput(_ElementFieldOutput):
    """StressFieldOutput object for requesting the stresses at the elements from the analysis."""

    def __init__(self, **kwargs):
        super(StressFieldOutput, self).__init__("s", "Stress field output", ["sxx", "syy", "szz", "sxy", "sxz", "syz"], ["von_mises"], **kwargs)

    @classmethod
    def get_sqltable_schema(cls):
        """
        Return a dict describing the table name and each column
        (column_name, column_type, constraints).
        """
        return {
            "table_name": "s",
            "columns": [
                ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
                ("input_key", "INTEGER"),
                ("step", "TEXT"),
                ("part", "TEXT"),
                ("sxx", "REAL"),
                ("syy", "REAL"),
                ("szz", "REAL"),
                ("sxy", "REAL"),
                ("sxz", "REAL"),
                ("syz", "REAL"),
                ("von_mises", "REAL"),
            ],
        }

    @classmethod
    def get_jsontable_schema(cls):
        """
        Return a dict describing the table name and columns in JSON-like format.
        """
        return {
            "table_name": "element_output",
            "columns": [
                {"name": "id", "type": "INTEGER", "primary_key": True, "autoincrement": True},
                {"name": "element_key", "type": "INTEGER"},
                {"name": "sxx", "type": "REAL"},
                {"name": "syy", "type": "REAL"},
                {"name": "szz", "type": "REAL"},
                {"name": "sxy", "type": "REAL"},
                {"name": "sxz", "type": "REAL"},
                {"name": "syz", "type": "REAL"},
                {"name": "von_mises", "type": "REAL"},
            ],
        }



class FieldOutput(_Output):
    """FieldOutput object for specification of the fields (stresses, displacements,
    etc..) to output from the analysis.

    Parameters
    ----------
    nodes_outputs : list
        list of node fields to output
    elements_outputs : list
        list of elements fields to output

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    nodes_outputs : list
        list of node fields to output
    elements_outputs : list
        list of elements fields to output

    """

    def __init__(self, node_outputs=None, element_outputs=None, contact_outputs=None, name=None, **kwargs):
        super(FieldOutput, self).__init__(name=name, **kwargs)
        self._node_outputs = node_outputs
        self._element_outputs = element_outputs
        self._contact_outputs = contact_outputs

    @property
    def node_outputs(self):
        return self._node_outputs

    @property
    def element_outputs(self):
        return self._element_outputs

    @property
    def contact_outputs(self):
        return self._contact_outputs

    @property
    def outputs(self):
        return chain(self.node_outputs, self.element_outputs, self.contact_outputs)


class HistoryOutput(_Output):
    """HistoryOutput object for recording the fields (stresses, displacements,
    etc..) from the analysis.

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

    """

    def __init__(self, name=None, **kwargs):
        super(HistoryOutput, self).__init__(name=name, **kwargs)
