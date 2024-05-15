import sqlite3
from sqlite3 import Error

import sqlalchemy as db

# TODO convert to sqlalchemy


def create_connection_sqlite3(db_file=None):
    """Create a database connection to the SQLite database specified by db_file.

    Parameters
    ----------
    db_file : str, optional
        Path to the .db file, by default 'None'. If not provided, the database
        is run in memory.

    Returns
    -------
    :class:`sqlite3.Connection` | None
        Connection object or None

    """
    conn = None
    try:
        conn = sqlite3.connect(db_file or ":memory:")
    except Error as e:
        print(e)
    return conn


def _create_table_sqlite3(conn, sql):
    """Create a table from the create_table_sql statement.

    Parameters
    ----------
    conn : :class:`sqlite3.Connection`
        Connection to the database.
    create_table_sql : str
        A CREATE TABLE statement

    Returns
    -------
    None

    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def _insert_entry__sqlite3(conn, sql):
    """General code to insert an entry in a table

    Parameters
    ----------
    conn : _type_
        _description_
    sql : _type_
        _description_

    Returns
    -------
    lastrowid

    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)
        print(sql)
        exit()
    return c.lastrowid


def create_field_description_table_sqlite3(conn):
    """Create the table containing general results information and field
    descriptions.

    Parameters
    ----------
    conn :

    Returns
    -------
    None

    """
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS fields (field text, description text, components text, invariants text, UNIQUE(field) );"""
        _create_table_sqlite3(conn, sql)


def insert_field_description_sqlite3(conn, field, description, components_names, invariants_names):
    """Create the table containing general results information and field
    descriptions.

    Parameters
    ----------
    conn : obj
        Connection to the databse.
    field : str
        Name of the output field.
    components_names : Iterable
        Output field components names.
    invariants_names : Iterable
        Output field invariants names.

    Returns
    -------
    None

    """
    sql = """ INSERT OR IGNORE INTO fields VALUES ('{}', '{}', '{}', '{}')""".format(
        field,
        description,
        components_names,
        invariants_names,
    )

    return _insert_entry__sqlite3(conn, sql)


def create_field_table_sqlite3(conn, field, components_names):
    """Create the results table for the given field.

    Parameters
    ----------
    conn : obj
        Connection to the databse.
    field : str
        Name of the output field.
    components_names : Iterable
        Output field components names.
    invariants_names : Iterable
        Output field invariants names.

    Returns
    -------
    None

    """
    # FOREIGN KEY (step) REFERENCES analysis_results (step_name),
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS {} (step text, part text, type text, position text, key integer, {});""".format(
            field, ", ".join(["{} float".format(c) for c in components_names])
        )
        _create_table_sqlite3(conn, sql)


def insert_field_results_sqlite3(conn, field, node_results_data):
    """Insert the results of the analysis at a node.

    Parameters
    ----------
    conn : obj
        Connection to the databse.
    field : str
        Name of the output field.
    node_results_data : Iterable
        Output field components values.

    Returns
    -------
    int
        Index of the inserted item.

    """

    sql = """ INSERT INTO {} VALUES ({})""".format(field, ", ".join(["'" + str(c) + "'" for c in node_results_data]))
    return _insert_entry__sqlite3(conn, sql)


def create_connection(db_file=None):
    """Create a database connection to the SQLite database specified by db_file.

    Parameters
    ----------
    db_file : str, optional
        Path to the .db file, by default 'None'. If not provided, the database
        is run in memory.

    Returns
    -------
    :class:`sqlite3.Connection` | None
        Connection object or None

    """
    engine = db.create_engine("sqlite:///{}".format(db_file))
    connection = engine.connect()
    metadata = db.MetaData()
    return engine, connection, metadata


def get_database_table(engine, metadata, table_name):
    """Retrieve a table from the database.

    Parameters
    ----------
    engine : _type_
        _description_
    metadata : _type_
        _description_
    table_name : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return db.Table(table_name, metadata, autoload=True, autoload_with=engine)


def get_query_results(connection, table, columns, test):
    """Get the filtering query to execute.

    Parameters
    ----------
    connection : _type_
        _description_
    table : _type_
        _description_
    columns : _type_
        _description_
    test : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    query = db.select([table.columns[column] for column in columns]).where(db.and_(*test))
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return ResultProxy, ResultSet


def get_field_labels(engine, connection, metadata, field, label):
    """Get the names of the components or invariants of the field

    Parameters
    ----------
    engine : _type_
        _description_
    connection : _type_
        _description_
    metadata : _type_
        _description_
    field : _type_
        _description_
    label : _type_
        'components' or 'invariants'

    Returns
    -------
    _type_
        _description_
    """
    FIELDS = get_database_table(engine, metadata, "fields")
    query = db.select([FIELDS.columns[label]]).where(FIELDS.columns.field == field)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return ResultSet[0][0].split(" ")


def get_all_field_results(engine, connection, metadata, table):
    components = get_field_labels(engine, connection, metadata, str(table), "components")
    invariants = get_field_labels(engine, connection, metadata, str(table), "invariants")
    columns = ["part", "position", "key"] + components + invariants
    query = db.select([table.columns[column] for column in columns])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return ResultProxy, ResultSet


def get_field_results(engine, connection, metadata, table, test):
    components = get_field_labels(engine, connection, metadata, str(table), "components")
    invariants = get_field_labels(engine, connection, metadata, str(table), "invariants")
    labels = ["part", "position", "key"] + components + invariants
    ResultProxy, ResultSet = get_query_results(connection, table, labels, test)

    return ResultProxy, (labels, ResultSet)


if __name__ == "__main__":
    from pprint import pprint

    engine, connection, metadata = create_connection_sqlite3(r"C:\Code\myRepos\swissdemo\data\q_5\output\1_0\ULS\ULS-results.db")
    # U = db.Table('U', metadata, autoload=True, autoload_with=engine)
    U = get_database_table(engine, metadata, "U")
    # print(RF.columns.keys())
    # query = db.select([U]).where(U.columns.key == 0)
    # query = db.select([U]).where(U.columns.part.in_ == ['BLOCK_0', 'TIE_21'])
    # query = db.func.sum(RF.columns.RF3)
    # ResultProxy, ResultSet = get_query_results(connection, RF, ['RF1', 'RF2', 'RF3'], {'step': ('==', '"udl"'),
    #                                               'magnitude': ('!=', 0.)})

    sql = """
SELECT step, part, key, MIN(U3)
FROM U
WHERE step IN ('udl') AND part || '#$' || key  in ('BLOCK_8#$1', 'BLOCK_9#$3')
GROUP BY step, part;
"""
    ResultProxy = connection.execute(sql)
    ResultSet = ResultProxy.fetchall()
    pprint(ResultSet)
    # table_name = 'RF'
    # component = 'RF3'
    # # result = connection.execute(f'SELECT rowid, MIN({component}) , MAX({component}) FROM {table_name} GROUP BY rowid')
    # result = connection.execute(f'SELECT MIN({component}) , MAX({component}) FROM {table_name}')

    # min_value = None
    # max_value = None

    # for elem in result:
    #     min_value = elem[0]
    #     max_value = elem[1]

    # print('Min value : ',min_value)
    # print('Max value : ',max_value)
