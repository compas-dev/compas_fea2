# from sqlite3 import Error
# import sqlite3

try:
    # from ..job import *
    from odbAccess import *
except:
    pass

import pickle
import json
import os
import sys


# convert = {
#     'CF1':   'cfx',  'CF2':  'cfy',  'CF3':  'cfz', 'CFM': 'cfm',
#     'CM1':   'cmx',  'CM2':  'cmy',  'CM3':  'cmz', 'CMM': 'cmm',
#     'U1':    'ux',   'U2':   'uy',   'U3':   'uz',  'UM':  'um',
#     'UR1':   'urx',  'UR2':  'ury',  'UR3':  'urz', 'URM': 'urm',
#     'RF1':   'rfx',  'RF2':  'rfy',  'RF3':  'rfz', 'RFM': 'rfm',
#     'RM1':   'rmx',  'RM2':  'rmy',  'RM3':  'rmz', 'RMM': 'rmm',
#     'S11':   'sxx',  'S22':  'syy',  'S33':  'szz',  'S12':  'sxy',  'S13':  'sxz',  'S23':  'sxz',
#     'E11':   'exx',  'E22':  'eyy',  'E33':  'ezz',  'E12':  'exy',  'E13':  'exz',  'E23':  'exz',
#     'LE11':  'exx',  'LE22': 'eyy',  'LE33': 'ezz',  'LE12': 'exy',  'LE13': 'exz',  'LE23': 'exz',
#     'PE11':  'pexx', 'PE22': 'peyy', 'PE33': 'pezz', 'PE12': 'pexy', 'PE13': 'pexz', 'PE23': 'pexz',
#     'SF1':   'sf1',  'SF2':  'sf2',  'SF3':  'sf3',  'SF4':  'sf4',  'SF5':  'sf5',  'SF6':  'sf6',
#     'SM1':   'sm1',  'SM2':  'sm2',  'SM3':  'sm3',
#     'SK1':   'skx',  'SK2':  'sky',  'SK3':  'skz',
#     'SE1':   'se1',  'SE2':  'se2',  'SE3':  'se3',
#     'CTF1':  'spfx', 'CTF2': 'spfy', 'CTF3': 'spfz',
#     'TF1':   'tfx',  'TF2':  'tfy',  'TF3':  'tfz',
#     'NFORCSO1': 'nfx', 'NFORCSO2': 'nfy', 'NFORCSO3': 'nfz', 'NFORCSO4': 'nmx',  'NFORCSO5':  'nmy',  'NFORCSO6':  'nmz',


#     'VALUE':  'rbfor',
#     'AXES':   'axes',
#     'SMISES': 'smises', 'SMAXP': 'smaxp', 'SMINP': 'sminp',
# }

# TODO Extend with:https://abaqus-docs.mit.edu/2017/English/SIMACAEOUTRefMap/simaout-c-std-nodalvariables.htm


# def create_connection(db_file=None):
#     """ Create a database connection to the SQLite database specified by db_file.

#     Parameters
#     ----------
#     db_file : str, optional
#         Path to the .db file, by default 'None'. If not provided, the database
#         is run in memory.

#     Return
#     ------
#     :class:`sqlite3.Connection` | None
#         Connection object or None
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file or ':memory:')
#     except Error as e:
#         print(e)

#     return conn


# def _create_table(conn, create_table_sql):
#     """ Create a table from the create_table_sql statement.

#     Parameters
#     ----------
#     conn : :class:`sqlite3.Connection`
#         Connection to the database.
#     create_table_sql : str
#         A CREATE TABLE statement

#     """

#     try:
#         c = conn.cursor()
#         c.execute(create_table_sql)
#     except Error as e:
#         print(e)


# def create_steps_table(conn, step):
#     # FOREIGN KEY (step) REFERENCES analysis_results (step_name),
#     with conn:
#         sql = """CREATE TABLE IF NOT EXISTS steps(name text);"""
#         _create_table(conn, sql)
#         sql = """ INSERT INTO steps VALUES(:name) """
#         cur = conn.cursor()
#         cur.execute(sql, (step,))
#         conn.commit()
#         return cur.lastrowid


# def create_nodal_results_table(conn, fields):
#     # FOREIGN KEY (step) REFERENCES analysis_results (step_name),
#     with conn:
#         sql = """CREATE TABLE IF NOT EXISTS nodal (
#                                         key integer PRIMARY KEY,
#                                         {}
#                                     );""".format(', '.join(['FOREIGN KEY({0}) REFERENCES fields({0})'.format(field) for field in fields]))
#         _create_table(conn, sql)


# def create_nodal_results_table(conn):
#     # FOREIGN KEY (step) REFERENCES analysis_results (step_name),
#     with conn:
#         sql = """CREATE TABLE IF NOT EXISTS nodal (
#                                         key integer PRIMARY KEY,
#                                         rf float,
#                                         rm float,
#                                         u float,
#                                         um float,
#                                         ur float,
#                                         cf float,
#                                         cm float,
#                                         tf float
#                                     );"""
#         _create_table(conn, sql)


# def insert_nodal_results(conn, nodal_results):
#     """ Insert the results of the analysis at a node.

#     Parameters
#     ----------
#     conn : obj
#         Connection to the databse
#     nodal_results : dict
#         Dictionary with the results at the node.
#     """

#     # node_fields = ['key', 'rf', 'rm', 'u', 'ur', 'cf', 'cm', 'tf']
#     # if not any(key in node_fields for key in nodal_results.keys()):
#     #     raise ValueError
#     # if not all(key in node_fields for key in nodal_results.keys()):
#     #     raise ValueError

#     sql = """ INSERT INTO nodal VALUES({}) """.format(
#         ','.join([':{}'.format(key) for key in nodal_results.keys()]))
#     cur = conn.cursor()
#     cur.execute(sql, nodal_results)
#     conn.commit()
#     return cur.lastrowid


def extract_odb_data(database_path, database_name, to_json=True, to_pickle=False):
    """Extracts data from the .odb file for the requested steps and fields.

    Parameters
    ----------
    database_path : str
        Folder path containing the analysis .odb file.
    database_name : str
        Name of the database.
    fields : list
        Data field requests.
    components : list
        Specific components to extract from the fields data.
    steps : list, str
        Step names to extract data for, by default all steps.

    Returns
    -------
    None

    """
    odb = openOdb(os.path.join(database_path, '{}.odb'.format(database_name)))

    results = {'steps': {}}
    # tables
    steps_table = {'id': [], 'name': []}
    parts_table = {'id': [], 'name': []}
    nodes_table = {'id': [], 'part_id': []}
    results_table = {'field': [], 'step_id': [], 'part_id': [], 'node_id': [], 'field_value': []}
    elements_table = {'id': [], 'part_id': [], 'step_id': [], 'field_id': [], 'field_value': []}
    steps = odb.steps
    for step_name, step in steps.items():

        frame = step.frames[-1]  # TODO maybe loop through the frames
        step_id = 1
        steps_table['id'] = step_id
        steps_table['name'] = step_name

        for field, output in frame.fieldOutputs.items():
            node_id = 1
            for value in output.values:
                nodelabel = getattr(value, 'nodeLabel')
                elementlabel = getattr(value, 'elementLabel')
                part_id = 1
                if value.instance.name[:-2] not in parts_table['name']:
                    parts_table['id'] = part_id
                    parts_table['name'] = value.instance.name[:-2]
                    part_id += 1
                if nodelabel:
                    results['steps'].setdefault(step_id, {}).setdefault(step_name, {}).setdefault(value.instance.name[:-2], {}).setdefault('nodes', {}).setdefault(nodelabel-1, {})[
                        field] = [float(n) for n in value.data]
                    if node_id not in nodes_table['id']:
                        nodes_table['id'].append(node_id)
                        nodes_table['part_id'].append(part_id)

                    results_table.setdefault('field', []).append(field)
                    results_table.setdefault('step_id', []).append(step_id)
                    results_table.setdefault('part_id', []).append(part_id)
                    results_table.setdefault('node_id', []).append(node_id)
                    results_table.setdefault('field_value', []).append([float(n) for n in value.data])
                    node_id += 1
                if elementlabel:
                    results['steps'].setdefault(step_id, {}).setdefault(step_name, {}).setdefault(value.instance.name[:-2], {}).setdefault('elements', {}).setdefault(elementlabel-1, {})[
                        field] = [float(n) for n in value.data]
        step_id += 1

    if to_pickle:
        with open(os.path.join(database_path, '{}-results.pkl'.format(database_name)), 'wb') as f:
            pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    if to_json:
        with open(os.path.join(database_path, '{}-results.json'.format(database_name)), 'wb') as f:
            json.dump(results, f)
        with open(os.path.join(database_path, '{}-node_results.json'.format(database_name)), 'wb') as f:
            json.dump(results_table, f)

    # with conn:
    #     for step, results_types in results.items():
    #         create_steps_table(conn, step)
    #         for result_type, values in results_types.items():
    #             if result_type == 'nodal':
    #                 create_nodal_results_table(conn)
    #                 insert_nodal_results(conn, values)


# ============================================================================
# Main
# ============================================================================
# NOTE: this is used while calling the module through abaqus -> !!!DO NOT DELETE!!!
if __name__ == "__main__":

    database_path = sys.argv[-1]
    database_name = sys.argv[-2]

    extract_odb_data(database_path=database_path, database_name=database_name)
