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


def extract_odb_data(database_path, database_name, fields, to_json=True, to_pickle=False):
    """Extracts data from the .odb file for the requested steps and fields.

    Parameters
    ----------
    database_path : str
        Folder path containing the analysis .odb file.
    database_name : str
        Name of the database.
    fields : list
        Data field requests.

    Returns
    -------
    None

    """
    odb = openOdb(os.path.join(database_path, '{}.odb'.format(database_name)))

    results = {}
    steps = odb.steps
    for step_name, step in steps.items():

        frame = step.frames[-1]  # TODO maybe loop through the frames

        for field, output in frame.fieldOutputs.items():
            if fields:
                if field not in fields:
                    continue
            for value in output.values:
                nodelabel = getattr(value, 'nodeLabel')
                elementlabel = getattr(value, 'elementLabel')
                try:
                    iter(value.data)
                    value_data = value.data
                except:
                    value_data = [value.data]
                value_data = [float(x) for x in value_data]
                if nodelabel:
                    results.setdefault(step_name, {}).setdefault(value.instance.name[:-2], {}).setdefault('nodes', {}).setdefault(nodelabel-1, {})[
                        field] = value_data
                if elementlabel:
                    results.setdefault(step_name, {}).setdefault(value.instance.name[:-2], {}).setdefault('elements', {}).setdefault(elementlabel-1, {})[
                        field] = value_data
    if to_pickle:
        with open(os.path.join(database_path, '{}-results.pkl'.format(database_name)), 'wb') as f:
            pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    if to_json:
        with open(os.path.join(database_path, '{}-results.json'.format(database_name)), 'wb') as f:
            json.dump(results, f)


# ============================================================================
# Main
# ============================================================================
# NOTE: this is used while calling the module through abaqus -> !!!DO NOT DELETE!!!
if __name__ == "__main__":

    # NOTE: the arguments are in the order they are passed
    database_path = sys.argv[-2]
    database_name = sys.argv[-1]
    fields = None if sys.argv[-3] == 'None' else sys.argv[-3].split(',')

    extract_odb_data(database_path=database_path, database_name=database_name, fields=fields)
