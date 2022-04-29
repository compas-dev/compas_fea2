import sqlite3
from sqlite3 import Error


import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_analysis_results(conn, analysis_results):
    """
    Create a new project into the analysis_results table
    :param conn:
    :param analysis_results:
    :return: analysis_results id
    """
    sql = ''' INSERT INTO analysis_results(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, analysis_results)
    conn.commit()
    return cur.lastrowid


def create_step_results(conn, step_results):
    """
    Create a new task
    :param conn:
    :param step_results:
    :return:
    """

    sql = ''' INSERT INTO step_results(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, step_results)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"C:\temp\results.db"

    sql_create_analysis_table = """ CREATE TABLE IF NOT EXISTS analysis_results (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_step_table = """CREATE TABLE IF NOT EXISTS step_results (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES analysis_results (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create analysis_results table
        create_table(conn, sql_create_analysis_table)

        # create tasks table
        create_table(conn, sql_create_step_table)
    else:
        print("Error! cannot create the database connection.")

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        analysis_0 = ('Cool results', 'test', '111')
        results_id = create_analysis_results(conn, analysis_0)

        # steps
        step_1 = ('Step_1', 1, 1, results_id, 'bla', 'bla2')
        step_2 = ('Step_2', 1, 1, results_id, '11', '22')

        # create tasks
        create_step_results(conn, step_1)
        create_step_results(conn, step_2)


if __name__ == '__main__':
    main()
