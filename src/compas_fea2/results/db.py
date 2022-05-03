import sqlite3
from sqlite3 import Error

import sqlite3
from sqlite3 import Error


def create_connection(db_file=None):
    """ Create a database connection to the SQLite database specified by db_file.

    Parameters
    ----------
    db_file : str, optional
        Path to the .db file, by default 'None'. If not provided, the database
        is run in memory.

    Return
    ------
    :class:`sqlite3.Connection` | None
        Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file or ':memory:')
    except Error as e:
        print(e)

    return conn


def _create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement.

    Parameters
    ----------
    conn : :class:`sqlite3.Connection`
        Connection to the database.
    create_table_sql : str
        A CREATE TABLE statement

    """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_nodal_results_table(conn):
    # FOREIGN KEY (step) REFERENCES analysis_results (step_name),
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS nodal_results (
                                        key integer PRIMARY KEY,
                                        rf float,
                                        rm float,
                                        u float,
                                        ur float,
                                        cf float,
                                        cm float,
                                        tf float
                                    );"""
        _create_table(conn, sql)


def insert_nodal_results(conn, nodal_results):
    """ Insert the results of the analysis at a node.

    Parameters
    ----------
    conn : obj
        Connection to the databse
    nodal_results : dict
        Dictionary with the results at the node.
    """

    node_fields = ['key', 'rf', 'rm', 'u', 'ur', 'cf', 'cm', 'tf']
    if not any(key in node_fields for key in nodal_results.keys()):
        raise ValueError
    if not all(key in node_fields for key in nodal_results.keys()):
        raise ValueError

    # element_fields = ['sf', 'sm', 'sk', 'se', 's', 'e', 'pe', 'ctf', 'rbfor', 'nforcso']

    sql = """ INSERT INTO nodal_results VALUES({}) """.format(
        ','.join([':{}'.format(key) for key in nodal_results.keys()]))
    cur = conn.cursor()
    cur.execute(sql, nodal_results)
    conn.commit()
    return cur.lastrowid


def show_node_results(conn, field, value):
    sql = """ SELECT * FROM nodal_results WHERE {0}=:{0} """.format(field)
    cur = conn.cursor()
    cur.execute(sql, {field: value})
    return cur.fetchall()


if __name__ == '__main__':
    # create a database connection
    # database=r"C:\temp\results.db"
    conn = create_connection()
    with conn:
        create_nodal_results_table(conn)
        nodal_results = {'key': 0, 'rf': 0, 'rm': 1, 'u': 2, 'ur': 3, 'cf': 4, 'cm': 5, 'tf': 6}
        insert_nodal_results(conn, nodal_results)

    print(show_node_results(conn, 'rf', 0))
