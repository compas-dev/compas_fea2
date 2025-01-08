import sqlite3


class ResultsDatabase:
    """sqlite3 wrapper class to access the SQLite database."""

    def __init__(self, db_uri):
        """
        Initialize DataRetriever with the database URI.

        Parameters
        ----------
        db_uri : str
            The database URI.
        """
        self.db_uri = db_uri
        self.connection = self.db_connection()
        self.cursor = self.connection.cursor()

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
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in self.cursor.fetchall()]

    @property
    def fields(self):
        return [c for c in self.table_names if c != "fields"]

    def column_names(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        return [row[1] for row in self.cursor.fetchall()]

    def get_table(self, table_name):
        """Get a table from the database.

        Parameters
        ----------
        table_name : str
            The name of the table.

        Return
        ------
        str
            The table name.
        """
        return table_name

    def get_column_values(self, table_name, column_name):
        """Get all the rows in a given table that match the filtering criteria
        and return the values for each column.

        Parameters
        ----------
        table_name : str
            The name of the table.
        column_name : str
            The name of the column.

        Returns
        -------
        list
            The column values.
        """
        query = f"SELECT {column_name} FROM {table_name}"
        return self.execute_query(query)

    def get_column_unique_values(self, table_name, column_name):
        """Get all the values in a column and remove duplicates.

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

        Return
        ------
        list of lists
            list with each row as a list
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
