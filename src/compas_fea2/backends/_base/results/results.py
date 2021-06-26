from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from sys import path

from compas_fea2.backends._base.base import FEABase

import json
import pickle
from pathlib import Path

# Author(s): Francesco Ranaudo (github.com/franaudo)


class ResultsBase(FEABase):
    """`compas_fea2` ResultsBase object. This ensures that the results from all
    the backends are consistent.

    Parameters
    ----------
    fields : list
        Data field requests.
    exe : str
        Abaqus exe path to bypass defaults.
    output : bool
        Print terminal output.
    components : list
        Specific components to extract from the fields data.
    """

    def __init__(self, problem, fields, steps, sets, components, output):
        self.problem_name = problem.name
        self.database_path = problem.path
        self.temp_dump = Path(self.database_path).joinpath(self.problem_name + '-results')
        self._fields = fields
        self._steps = steps
        self._sets = sets
        self._components = components
        self.output = output
        self._info = {}
        self._nodal = {}
        self._element = {}
        self._modal = {}

    @property
    def nodal(self):
        return self._nodal

    @property
    def element(self):
        return self._element

    @property
    def info(self):
        return self._info

    @property
    def modal(self):
        return self._modal

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields):
        if not isinstance(fields, list):
            fields = [fields]
        for x in fields:
            if x not in self.problem.field_outputs:
                print("WARNING: field {0} not in {1} and it will be ignored!\nRun the anlysis requesting {0}".format(
                    x, self.problem_name))
            else:
                self._fields.append(x)

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, steps):
        if not isinstance(steps, list):
            steps = [steps]
        for x in steps:
            if x not in self.problem.steps:
                print("WARNING: step {0} not in {1} and it will be ignored!\nRun the anlysis requesting {0}".format(
                    x, self.problem_name))
            else:
                self._steps.append(x)

    @property
    def sets(self):
        return self._sets

    @property
    def components(self):
        return self._components

    # ==========================================================================
    # Extract results
    # ==========================================================================

    def extract_data(self):
        raise NotImplementedError("this function is not available for the selceted backend")

    # ==============================================================================
    # Read results
    # ==============================================================================

    def get_nodal_results(self, step, field, nodes='all'):
        """Extract nodal results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        nodes : str, list
            Extract 'all' or a node collection/list.

        Returns
        -------
        dict
            The nodal results for the requested field.
        """
        data = {}
        rdict = self.results[step]['nodal']

        if nodes == 'all':
            keys = list(self.nodes.keys())
        else:
            keys = nodes

        for key in keys:
            data[key] = rdict[field][key]

        return data

    def get_element_results(self, step, field, elements='all'):
        """Extract element results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        elements : str, list
            Extract 'all' or an element collection/list.

        Returns
        -------
        dict
            The element results for the requested field.
        """
        data = {}
        rdict = self.results[step]['element']

        if elements == 'all':
            keys = list(self.elements.keys())

        # elif isinstance(elements, str):              TODO: transfor to 'collection'
        #     keys = self.sets[elements].selection

        else:
            keys = elements

        for key in keys:
            data[key] = rdict[field][key]

        return data

    # ==========================================================================
    # Serialization
    # ==========================================================================

    def serialize(self):
        with open(self.temp_dump+'.pkl', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def deserialize(cls, path):
        with open(path, 'rb') as f:
            cls = pickle.load(f)
        return cls

    # ==========================================================================
    # Save results
    # ==========================================================================
    def save_to_json(self, path=None):
        if not path:
            path = self.temp_dump+'.json'
        with open(path, 'w') as f:
            json.dump(self, f)


class CaseResultsBase(FEABase):
    """`compas_fea2` ResultsCaseBase object. This ensures that the results from
    a specific load case are consistently organised across all backends.

    Parameters
    ----------
    name : str
        load case name.
    nodal : dict
        nodal results for the load case.\n`{node_id: value}`
    element : dict
        element results for the loda case\n`{element_id: value}`
    """

    def __init__(self, name):
        self.name = name
        self.path = path
        self.temp_dump = Path(self.path).joinpath(self.name+'-results')
        self.info = {}
        self.nodal = {}
        self.element = {}
        self.modal = {}

    def serialize(self):
        with open(self.temp_dump+'.pkl', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def save_to_json(self, path=None):
        if not path:
            path = self.temp_dump+'.json'
        with open(path, 'w') as f:
            json.dump(self, f)
