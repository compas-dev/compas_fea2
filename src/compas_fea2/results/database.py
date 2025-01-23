import sqlite3
from compas_fea2.base import FEAData


class ResultsDatabase(FEAData):
    """sqlite3 wrapper class to access the SQLite database."""

    def __init__(self, problem, **kwargs):
        """
        Initialize DataRetriever with the database URI.

        Parameters
        ----------
        db_uri : str
            The database URI.
        """
        super(ResultsDatabase, self).__init__(**kwargs)
        self._registration = problem
        self.db_uri = problem.path_db
        self.connection = self.db_connection()
        self.cursor = self.connection.cursor()

    @property
    def problem(self):
        return self._registration

    @property
    def model(self):
        return self.problem.model

    def db_connection(self):
        """
        Create and return a connection to the SQLite database.

        Returns
        -------
        connection : Connection
            The database connection.
        """
        return sqlite3.connect(self.db_uri)

    def execute_query(self, query, params=None):
        """Execute a previously-defined query.

        Parameters
        ----------
        query : str
            The SQL query to execute.
        params : tuple, optional
            The parameters to bind to the query.

        Returns
        -------
        list
            The result set.
        """
        self.connection = self.db_connection()
        self.cursor = self.connection.cursor()
        self.cursor.execute(query, params or ())
        result_set = self.cursor.fetchall()
        self.connection.close()
        return result_set

    # =========================================================================
    #                       Query methods
    # =========================================================================
    @property
    def table_names(self):
        """
        Get the names of all tables in the database.

        Returns
        -------
        list
            A list of table names.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in self.cursor.fetchall()]

    @property
    def fields(self):
        """
        Get the names of all fields in the database, excluding the 'fields' table.

        Returns
        -------
        list
            A list of field names.
        """
        return [c for c in self.table_names if c != "fields"]

    def column_names(self, table_name):
        """
        Get the names of all columns in a given table.

        Parameters
        ----------
        table_name : str
            The name of the table.

        Returns
        -------
        list
            A list of column names.
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        return [row[1] for row in self.cursor.fetchall()]

    def get_table(self, table_name):
        """Get a table from the database.

        Parameters
        ----------
        table_name : str
            The name of the table.

        Returns
        -------
        list of tuples
            The table data.
        """
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)

    def get_column_values(self, table_name, column_name):
        """Get all the values in a given column from a table.

        Parameters
        ----------
        table_name : str
            The name of the table.
        column_name : str
            The name of the column.

        Returns
        -------
        list
            A list of values from the specified column.
        """
        query = f"SELECT {column_name} FROM {table_name}"
        return self.execute_query(query)

    def get_column_unique_values(self, table_name, column_name):
        """Get all the unique values in a given column from a table.

        Parameters
        ----------
        table_name : str
            The name of the table.
        column_name : str
            The name of the column.

        Returns
        -------
        set
            The unique column values.
        """
        return set(self.get_column_values(table_name, column_name))

    def get_rows(self, table_name, columns_names, filters):
        """Get all the rows in a given table that match the filtering criteria
        and return the values for each column.

        Parameters
        ----------
        table_name : str
            The name of the table.
        columns_names : list
            Name of each column to retrieve. The results are output in the same
            order.
        filters : dict
            Filtering criteria as {"column_name":[admissible values]}

        Returns
        -------
        list of lists
            List with each row as a list.
        """
        filter_conditions = " AND ".join([f"{k} IN ({','.join(['?' for _ in v])})" for k, v in filters.items()])
        query = f"SELECT {', '.join(columns_names)} FROM {table_name} WHERE {filter_conditions}"
        params = [item for sublist in filters.values() for item in sublist]
        return self.execute_query(query, params)

    def get_func_row(self, table_name, column_name, func, filters, columns_names):
        """Get all the rows in a given table that match the filtering criteria
        and apply a function to it.

        Currently supported functions:

            - MAX:

        Parameters
        ----------
        table_name : str
            The name of the table.
        column_name : str
            The name of the column.
        func : str
            The function to apply (e.g., "MAX").
        filters : dict
            Filtering criteria as {"column_name":[admissible values]}
        columns_names : list
            Name of each column to retrieve. The results are output in the same
            order.

        Returns
        -------
        list
            The result row.
        """
        filter_conditions = " AND ".join([f"{k} IN ({','.join(['?' for _ in v])})}}" for k, v in filters.items()])
        query = f"SELECT {', '.join(columns_names)} FROM {table_name} WHERE {filter_conditions} ORDER BY {func}({column_name}) DESC LIMIT 1"
        params = [item for sublist in filters.values() for item in sublist]
        return self.execute_query(query, params)

    # =========================================================================
    #                       FEA2 Methods
    # =========================================================================

    def to_result(self, results_set, results_class, results_func):
        """Convert a set of results in the database to the appropriate
        result object.

        Parameters
        ----------
        results_set : list of tuples
            The set of results retrieved from the database.
        results_class : class
            The class to instantiate for each result.

        Returns
        -------
        dict
            Dictionary grouping the results per Step.
        """
        results = {}
        for r in results_set:
            step = self.problem.find_step_by_name(r[0])
            results.setdefault(step, [])
            part = self.model.find_part_by_name(r[1]) or self.model.find_part_by_name(r[1], casefold=True)
            if not part:
                raise ValueError(f"Part {r[1]} not in model")
            m = getattr(part, results_func)(r[2])
            if not m:
                raise ValueError(f"Member {r[2]} not in part {part.name}")
            results[step].append(results_class(m, *r[3:]))
        return results

    @staticmethod
    def create_table_for_output_class(output_cls, connection, results):
        """
        Reads the table schema from `output_cls.get_table_schema()`
        and creates the table in the given database.

        Parameters
        ----------
        output_cls : _Output subclass
            A class like NodeOutput that implements `get_table_schema()`
        connection : sqlite3.Connection
            SQLite3 connection object
        results : list of tuples
            Data to be inserted into the table
        """
        cursor = connection.cursor()

        schema = output_cls.sqltable_schema
        table_name = schema["table_name"]
        columns_info = schema["columns"]

        # Build CREATE TABLE statement:
        columns_sql_str = ", ".join([f"{col_name} {col_def}" for col_name, col_def in columns_info])
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql_str})"
        cursor.execute(create_sql)
        connection.commit()

        # Insert data into the table:
        insert_columns = [col_name for col_name, col_def in columns_info if "PRIMARY KEY" not in col_def.upper()]
        col_names_str = ", ".join(insert_columns)
        placeholders_str = ", ".join(["?"] * len(insert_columns))
        sql = f"INSERT INTO {table_name} ({col_names_str}) VALUES ({placeholders_str})"
        cursor.executemany(sql, results)
        connection.commit()
