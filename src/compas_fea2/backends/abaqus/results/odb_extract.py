from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # from ..job import *
    from odbAccess import *
except:
    pass

try:
    # from ..job import *
    from .job import *
except:
    pass

import pickle
import json
import os
import sys


# Author(s): Andrew Liew (github.com/andrewliew)


convert = {
    'CF1':   'cfx',  'CF2':  'cfy',  'CF3':  'cfz', 'CFM': 'cfm',
    'CM1':   'cmx',  'CM2':  'cmy',  'CM3':  'cmz', 'CMM': 'cmm',
    'U1':    'ux',   'U2':   'uy',   'U3':   'uz',  'UM':  'um',
    'UR1':   'urx',  'UR2':  'ury',  'UR3':  'urz', 'URM': 'urm',
    'RF1':   'rfx',  'RF2':  'rfy',  'RF3':  'rfz', 'RFM': 'rfm',
    'RM1':   'rmx',  'RM2':  'rmy',  'RM3':  'rmz', 'RMM': 'rmm',
    'S11':   'sxx',  'S22':  'syy',  'S33':  'szz',  'S12':  'sxy',  'S13':  'sxz',  'S23':  'sxz',
    'E11':   'exx',  'E22':  'eyy',  'E33':  'ezz',  'E12':  'exy',  'E13':  'exz',  'E23':  'exz',
    'LE11':  'exx',  'LE22': 'eyy',  'LE33': 'ezz',  'LE12': 'exy',  'LE13': 'exz',  'LE23': 'exz',
    'PE11':  'pexx', 'PE22': 'peyy', 'PE33': 'pezz', 'PE12': 'pexy', 'PE13': 'pexz', 'PE23': 'pexz',
    'SF1':   'sf1',  'SF2':  'sf2',  'SF3':  'sf3',  'SF4':  'sf4',  'SF5':  'sf5',  'SF6':  'sf6',
    'SM1':   'sm1',  'SM2':  'sm2',  'SM3':  'sm3',
    'SK1':   'skx',  'SK2':  'sky',  'SK3':  'skz',
    'SE1':   'se1',  'SE2':  'se2',  'SE3':  'se3',
    'CTF1':  'spfx', 'CTF2': 'spfy', 'CTF3': 'spfz',
    'TF1':   'tfx',  'TF2':  'tfy',  'TF3':  'tfz',
    'NFORCSO1': 'nfx', 'NFORCSO2': 'nfy', 'NFORCSO3': 'nfz', 'NFORCSO4': 'nmx',  'NFORCSO5':  'nmy',  'NFORCSO6':  'nmz',


    'VALUE':  'rbfor',
    'AXES':   'axes',
    'SMISES': 'smises', 'SMAXP': 'smaxp', 'SMINP': 'sminp',
}

# TODO Extend with:https://abaqus-docs.mit.edu/2017/English/SIMACAEOUTRefMap/simaout-c-std-nodalvariables.htm
node_fields = ['rf', 'rm', 'u', 'ur', 'cf', 'cm', 'tf']
element_fields = ['sf', 'sm', 'sk', 'se', 's', 'e', 'pe', 'ctf', 'rbfor', 'nforcso']


def extract_odb_data(database_path, database_name, fields=None, components=None, steps=None):
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

    if not components:
        components = set()
        for value in convert.values():
            components.add(value)
    else:
        components = set(components)

    results = {}
    info = {}

    if not steps:
        steps = odb.steps.keys()

    for step in steps:

        results[step] = {'nodal': {}, 'element': {}}
        info[step] = {}

        # last frame description
        description = odb.steps[step].frames[-1].description

        refn = results[step]['nodal']
        refe = results[step]['element']

        if 'Mode' in description:

            info[step]['description'] = {}

            for counter, frame in enumerate(odb.steps[step].frames):
                fieldoutputs = frame.fieldOutputs
                info[step]['description'][counter] = frame.description
                clabels = list(fieldoutputs['U'].componentLabels)
                for c in clabels:
                    if convert[c] in components:
                        refn[convert[c] + str(counter)] = {}
                if 'um' in components:
                    refn['um' + str(counter)] = {}
                for value in fieldoutputs['U'].values:
                    data = value.jobdata
                    node = value.nodeLabel - 1
                    for i, c in enumerate(clabels):
                        if convert[c] in components:
                            refn[convert[c] + str(counter)][node] = float(data[i])
                    if 'um' in components:
                        refn['um' + str(counter)][node] = float(value.magnitude)
            try:
                frequencies = odb.steps[step].historyRegions['Assembly Assembly-1'].historyOutputs['EIGFREQ'].data
                results[step]['frequencies'] = [i[1] for i in frequencies]
            except:
                pass
            try:
                masses = odb.steps[step].historyRegions['Assembly Assembly-1'].historyOutputs['GM'].data
                results[step]['masses'] = [i[1] for i in masses]
            except:
                pass

        else:
            info[step]['description'] = description
            frame = odb.steps[step].frames[-1]
            fieldoutputs = frame.fieldOutputs

            # Node data
            try:
                for field in list(set(fields) & set(node_fields)):
                    clabels = list(fieldoutputs[field.upper()].componentLabels)
                    # create a dictionary entry for each component
                    for c in clabels:
                        if convert[c] in components:
                            refn[convert[c]] = {}
                    # create a dictionary entry for the magnitude component
                    if field + 'm' in components:
                        refn[field + 'm'] = {}

                    for fieldvalue in fieldoutputs[field.upper()].values:
                        data = fieldvalue.data
                        if isinstance(data, float):
                            data = [data]
                        node = fieldvalue.nodeLabel - 1
                        for i, c in enumerate(clabels):
                            if convert[c] in components:  # TODO remove?!
                                refn[convert[c]][node] = float(data[i])
                        if field + 'm' in components:
                            refn[field + 'm'][node] = float(fieldvalue.magnitude)
            except:
                sys.__stderr__.write('Node output failed\n')

            # Element data
            try:
                for field in list(set(fields) & set(element_fields)):

                    if field == 'nforcso':
                        for i in range(6):
                            comp = field.upper()+str(i+1)
                            refe[convert[comp]] = {}

                            for fieldvalue in fieldoutputs[comp].values:
                                data = fieldvalue.data  # if not isinstance(data, float) else [data]
                                element = fieldvalue.elementLabel - 1
                                # group data belonging to the same element
                                if element in refe[convert[comp]].keys():
                                    refe[convert[comp]][element].append(data)
                                else:
                                    refe[convert[comp]][element] = [data]

                    else:
                        field = 'ctf' if field == 'spf' else field
                        field = 'le' if field == 'e' else field
                        clabels = ['VALUE'] if field == 'rbfor' else list(fieldoutputs[field.upper()].componentLabels)

                        for c in clabels:
                            if convert[c] in components:
                                refe[convert[c]] = {}
                        if (field == 's') and ('smises' in components):
                            refe['smises'] = {}
                        if field in ['s', 'pe']:
                            if field + 'maxp' in components:
                                refe[field + 'maxp'] = {}
                            if field + 'minp' in components:
                                refe[field + 'minp'] = {}
                            if 'axes' in components:
                                refe['axes'] = {}
                        elif field == 'le':
                            if 'emaxp' in components:
                                refe['emaxp'] = {}
                            if 'eminp' in components:
                                refe['eminp'] = {}

                        for fieldvalue in fieldoutputs[field.upper()].values:
                            data = fieldvalue.data
                            if isinstance(data, float):
                                data = [data]
                            element = fieldvalue.elementLabel - 1
                            ip = fieldvalue.integrationPoint
                            sp = fieldvalue.sectionPoint.number if fieldvalue.sectionPoint else 0
                            id = 'ip{0}_sp{1}'.format(ip, sp)

                            for i, c in enumerate(clabels):
                                if convert[c] in components:
                                    try:
                                        refe[convert[c]][element][id] = float(data[i])
                                    except:
                                        refe[convert[c]][element] = {}
                                        try:
                                            refe[convert[c]][element][id] = float(data[i])
                                        except:
                                            refe[convert[c]][element][id] = None

                            if field == 's':
                                if 'smises' in components:
                                    try:
                                        refe['smises'][element][id] = float(fieldvalue.mises)
                                    except:
                                        refe['smises'][element] = {}
                                        try:
                                            refe['smises'][element][id] = float(fieldvalue.mises)
                                        except:
                                            refe['smises'][element][id] = None

                            if field in ['s', 'pe']:
                                try:
                                    if field + 'maxp' in components:
                                        refe[field + 'maxp'][element][id] = float(fieldvalue.maxPrincipal)
                                    if field + 'minp' in components:
                                        refe[field + 'minp'][element][id] = float(fieldvalue.minPrincipal)
                                    if 'axes' in components:
                                        refe['axes'][element] = fieldvalue.localCoordSystem
                                except:
                                    refe[field + 'maxp'][element] = {}
                                    refe[field + 'minp'][element] = {}
                                    try:
                                        if field + 'maxp' in components:
                                            refe[field + 'maxp'][element][id] = float(fieldvalue.maxPrincipal)
                                        if field + 'minp' in components:
                                            refe[field + 'minp'][element][id] = float(fieldvalue.minPrincipal)
                                    except:
                                        if field + 'maxp' in components:
                                            refe[field + 'maxp'][element][id] = None
                                        if field + 'minp' in components:
                                            refe[field + 'minp'][element][id] = None

                            if field == 'le':
                                try:
                                    if 'emaxp' in components:
                                        refe['emaxp'][element][id] = float(fieldvalue.maxPrincipal)
                                    if 'eminp' in components:
                                        refe['eminp'][element][id] = float(fieldvalue.minPrincipal)
                                except:
                                    refe['emaxp'][element] = {}
                                    refe['eminp'][element] = {}
                                    try:
                                        if 'emaxp' in components:
                                            refe['emaxp'][element][id] = float(fieldvalue.maxPrincipal)
                                        if 'eminp' in components:
                                            refe['eminp'][element][id] = float(fieldvalue.minPrincipal)
                                    except:
                                        if 'emaxp' in components:
                                            refe['emaxp'][element][id] = None
                                        if 'eminp' in components:
                                            refe['eminp'][element][id] = None
            except:
                sys.__stderr__.write('Element output failed\n')  # TODO change

    with open(os.path.join(database_path, '{}-results.pkl'.format(database_name)), 'wb') as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    with open(os.path.join(database_path, '{}-info.pkl'.format(database_name)), 'wb') as f:
        pickle.dump(info, f, pickle.HIGHEST_PROTOCOL)

    with open(os.path.join(database_path, '{}-results.json'.format(database_name)), 'wb') as f:
        json.dump(results, f)

    with open(os.path.join(database_path, '{}-info.json'.format(database_name)), 'wb') as f:
        json.dump(results, f)


# ============================================================================
# Main
# ============================================================================
# NOTE: this is used while calling the module through abaqus -> !!!DO NOT DELETE!!!
if __name__ == "__main__":

    database_path = sys.argv[-1]
    database_name = sys.argv[-2]
    fields = None if sys.argv[-3] == 'None' else sys.argv[-3].split(',')
    components = None if sys.argv[-4] == 'None' else sys.argv[-4].split(',')
    steps = None if sys.argv[-5] == 'None' else sys.argv[-5].split(',')

    extract_odb_data(database_path=database_path, database_name=database_name,
                     steps=steps, fields=fields, components=components)
