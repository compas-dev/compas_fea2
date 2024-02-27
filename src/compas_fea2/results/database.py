from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy import and_
from sqlalchemy import inspect
from sqlalchemy import desc
from sqlalchemy import asc

from sqlalchemy.exc import SQLAlchemyError
from typing import Iterable


class ResultsDatabase:
    """sqlalchemy wrapper class to access the SQLite database."""

    def __init__(self, db_uri):
        """
        Initialize DataRetriever with the database URI.

        Parameters
        ----------
        db_uri : str
            The database URI.
        """
        self.db_uri = "sqlite:////" + db_uri
        self.engine, self.connection, self.metadata = self.db_connection()
        self.inspector = inspect(self.engine)

    def db_connection(self):
        """
        Create and return a connection to the SQLite database along with its metadata.

        Returns
        -------
        engine : Engine
            The SQLAlchemy engine instance.
        connection : Connection
            The database connection.
        metadata : MetaData
            The MetaData instance for the database.
        """
        engine = create_engine(self.db_uri)
        metadata = MetaData(bind=engine)
        return engine, engine.connect(), metadata

    def execute_query(self, query):
        """Execute a previously-defined query.

        Parameters
        ----------
        query : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        self.connection = self.engine.connect()
        with self.connection:
            result_proxy = self.connection.execute(query)
            result_set = result_proxy.fetchall()
            # self.connection.close()
            return result_set

    # =========================================================================
    #                       Query methods
    # =========================================================================
    @property
    def table_names(self):
        return self.inspector.get_table_names()

    @property
    def fields(self):
        return [c for c in self.inspector.get_table_names() if c != "fields"]

    @property
    def column_names(self, table_name):
        return self.inspector.get_columns(table_name)

    def get_table(self, table_name):
        """Get a table from the database.

        Parameters
        ----------
        table_name : str
            The name of the table.

        Return
        ------
        :class:`sqlalchemy.Table`
            The table from the database.
        """
        return Table(table_name, self.metadata, autoload_with=self.engine)

    def get_column_values(self, table_name, column_name):
        """Get all the rows in a given table that match the filtering criteria
        and return the values for each column.

        Parameters
        ----------
        table_name : _type_
            _description_
        column_name : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        query = select([table.c[column_name]])
        # return result_set[0][0].split(" ")
        return self.execute_query(query)

    def get_column_unique_values(self, table_name, column_name):
        """Get all the values in a column and remove duplicates.

        Parameters
        ----------
        table_name : _type_
            _description_
        column_name : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """

        return set(self.get_column_values(table_name, column_name))

    def get_rows(self, table_name, columns_names, filters):
        """Get all the rows in a given table that match the filtering criteria
        and return the values for each column.

        Parameters
        ----------
        table_name : str
            The name of the table.
        columns_name : list
            Name of each column to retrieve. The results are output in the same
            order.
        filters : dict
            Filtering criteria as {"column_name":[admissible values]}

        Return
        ------
        list of lists
            list with each row as a list
        """
        table = self.get_table(table_name)
        query = select([table.columns[c] for c in columns_names]).where(
            and_(*[table.columns[k].in_(v) for k, v in filters.items()])
        )
        return self.execute_query(query)

    def get_func_row(self, table_name, column_name, func, filters, columns_names):
        """Get all the rows in a given table that match the filtering criteria
        and apply a function to it.

        Currently supported functions:

            - MAX:

        Parameters
        ----------
        table_name : _type_
            _description_
        column_name : _type_
            _description_
        func : _type_
            _description_
        filters : _type_
            _description_
        columns_names : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        table = self.get_table(table_name)
        sql_func = {"MIN": asc, "MAX": desc}
        query = (
            select([table.columns[c] for c in columns_names])
            .where(and_(*[table.columns[k].in_(v) for k, v in filters.items()]))
            .order_by(sql_func[func](table.c[column_name]))
            .limit(1)
        )
        return self.connection.execute(query)
