from compas_fea2.results.sql_wrapper import create_connection
from math import sqrt
import os
import sqlite3
from sqlite3 import Error

# TODO convert to sqlalchemy

def create_connection(db_file=None):
    """Create a database connection to the SQLite database specified by db_file.

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


def _create_table(conn, sql):
    """Create a table from the create_table_sql statement.

    Parameters
    ----------
    conn : :class:`sqlite3.Connection`
        Connection to the database.
    create_table_sql : str
        A CREATE TABLE statement

    Return
    ------
    None
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def _insert_entry(conn, sql):
    """General code to insert an entry in a table

    Parameters
    ----------
    conn : _type_
        _description_
    sql : _type_
        _description_

    Return
    ------
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

def create_field_description_table(conn):
    """ Create the table containing general results information and field
    descriptions.

    Parameters
    ----------
    conn :

    Return
    ------
    None
    """
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS fields (field text, description text, components text, invariants text, UNIQUE(field) );"""
        _create_table(conn, sql)

def insert_field_description(conn, field, description, components_names, invariants_names):
    """ Create the table containing general results information and field
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

    Return
    ------
    None
    """
    sql = """ INSERT OR IGNORE INTO fields VALUES ('{}', '{}', '{}', '{}')""".format(field,
                                                                               description,
                                                                               components_names,
                                                                               invariants_names,
                                                                               )

    return _insert_entry(conn, sql)

def create_field_table(conn, field, components_names):
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

    Return
    ------
    None
    """
    # FOREIGN KEY (step) REFERENCES analysis_results (step_name),
    with conn:
        sql = """CREATE TABLE IF NOT EXISTS {} (step text, part text, type text, position text, key integer, {});""".format(
            field, ', '.join(['{} float'.format(c) for c in components_names]))
        _create_table(conn, sql)


def insert_field_results(conn, field, node_results_data):
    """Insert the results of the analysis at a node.

    Parameters
    ----------
    conn : obj
        Connection to the databse.
    field : str
        Name of the output field.
    node_results_data : Iterable
        Output field components values.

    Return
    ------
    int
        Index of the inserted item.
    """

    sql = """ INSERT INTO {} VALUES ({})""".format(field,
                                                ', '.join(
                                                    ["'"+str(c)+"'" for c in node_results_data])
                                                )
    return _insert_entry(conn, sql)



def read_results_file(database_path, database_name, field_output):
    """Read the .out results file and convert it to an SQLite db.

    Parameters
    ----------
    database_path : _type_
        _description_
    database_name : _type_
        _description_
    field_output : _type_
        _description_
    """
    results = {}

    field_info = {
        "u": {"num_of_comp": 3,
              "description_table": [['Spatial displacement', 'U1 U2 U3'], ['magnitude']],
              "field_table": ['U1', 'U2', 'U3', 'magnitude']},
        "rf": {"num_of_comp": 3,
              "description_table": [['Reaction forces', 'RF1 RF2 RF3'], ['magnitude']],
              "field_table": ['RF1', 'RF2', 'RF3', 'magnitude']},
        "rm": {"num_of_comp": 3,
              "description_table": [['Reaction moments', 'M1 M2 M3'], ['magnitude']],
              "field_table": ['RM1', 'RM2', 'RM3', 'magnitude']},
        "s": {"num_of_comp": 6,
              "description_table": [['Stresses', 'S11 S22 S12 M11 M22 M12'], ['magnitude']],
              "field_table": ['S11', 'S22', 'S12', 'M11', 'M22', 'M12']},
    }

    if field_output.node_outputs:
        for field in field_output.node_outputs:
            field = field.lower()
            number_of_components = field_info[field]["num_of_comp"]
            results.setdefault(field, {})

            nodes = field_output.nodes_set or range(0, list(field_output.model.parts)[0].nodes_count+1)
            filepath = os.path.join(database_path, '{}.out'.format(field.lower()))

            if not os.path.exists(filepath):
                print(f"file {filepath} not found. Results not extracted.")
                continue

            with open(filepath, 'r') as f:
                lines = f.readlines()
                # take the last analysis step and ignore the time stamp
                data = [float(i) for i in lines[-1].split(' ')[1:]]

            results[field]=[]
            for c, node in enumerate(nodes):
                part = list(field_output.model.parts)[0]
                step = field_output.step
                fea2_node = part.find_node_by_key(node)
                node_properties = [step.name, part.name, 'node', 'nodal', node]
                components_results = data[c*number_of_components:c*number_of_components+number_of_components]
                #TODO change to vectors
                u, v, w = components_results
                magnitude = [sqrt(u**2 + v**2 + w**2)]
                results[field].append(node_properties+components_results+magnitude)

            print('***** {0}.out data loaded *****'.format(filepath))

    if field_output.element_outputs:
        for field in field_output.element_outputs:
            field = field.lower()
            number_of_components = field_info[field]["num_of_comp"]
            results.setdefault(field, {})

            elements = field_output.elements_set or range(0, list(field_output.model.parts)[0].elements_count+1)
            filepath = os.path.join(database_path, '{}.out'.format(field.lower()))

            if not os.path.exists(filepath):
                print(f"file {filepath} not found. Results not extracted.")
                continue

            with open(filepath, 'r') as f:
                lines = f.readlines()
                # take the last analysis step and ignore the time stamp
                data = [float(i) for i in lines[-1].split(' ')[1:]]

            results[field]=[]
            for c, element_key in enumerate(elements):
                part = list(field_output.model.parts)[0]
                step = field_output.step
                fea2_element = part.find_element_by_key(node)
                element_properties = [step.name, part.name, 'element', 'nodal', element_key]
                components_results = data[c*number_of_components:c*number_of_components+number_of_components]
                results[field].append(element_properties+components_results)

            print('***** {0}.out data loaded *****'.format(filepath))


    database = os.path.join(database_path, f'{database_name}-results.db')

    if os.path.exists(database):
        os.remove(database)

    with create_connection(database) as conn:
        create_field_description_table(conn)
        for field_name, field_data in results.items():
            insert_field_description(conn, field_name.upper(),
                                     *field_info[field_name]['description_table'][0],
                                     *field_info[field_name]['description_table'][1])
            create_field_table(conn, field_name.upper(), field_info[field_name]['field_table'])
            for result_data in field_data:
                insert_field_results(conn, field_name.upper(), result_data)
        conn.commit()

