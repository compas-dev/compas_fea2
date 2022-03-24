from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import pickle
from sys import path
from pathlib import Path

from compas_fea2.base import FEAData


class Results(FEAData):
    """`compas_fea2` Results object. This ensures that the results from all
    the backends are consistent.

    Parameters
    ----------
    database_name : str
        name of the backend database containing the results
    database_path : str
        path to the backend database containing the results
    fields : list
        Data fields requested.
    steps : list
        Steps requested.
    sets : list
        Groups requested.
    components : list
        Specific components to extract from the fields data.
    output : bool
        Print terminal output.
    """

    def __init__(self, database_name, database_path, fields, steps, sets, components, output):
        super(Results, self).__init__()
        self.database_name = database_name
        self.database_path = database_path
        self.temp_dump = Path(self.database_path).joinpath(self.database_name + '.cfr')
        self._fields = fields
        self._steps = steps
        self._sets = sets
        self._components = components
        self.output = output

    @property
    def fields(self):
        return self._fields

    # @fields.setter
    # def fields(self, fields):
    #     if not isinstance(fields, list):
    #         fields = [fields]
    #     for x in fields:
    #         if x not in self.problem.field_outputs:
    #             print("WARNING: field {0} not in {1} and it will be ignored!\nRun the anlysis requesting {0}".format(
    #                 x, self.database_name))
    #         else:
    #             self._fields.append(x)

    @property
    def steps(self):
        return self._steps

    # @steps.setter
    # def steps(self, steps):
    #     if not isinstance(steps, list):
    #         steps = [steps]
    #     for x in steps:
    #         if x not in self.problem.steps:
    #             print("WARNING: step {0} not in {1} and it will be ignored!\nRun the anlysis requesting {0}".format(
    #                 x, self.problem_name))
    #         else:
    #             self._steps.append(x)

    @property
    def sets(self):
        return self._sets

    @property
    def components(self):
        return self._components

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_problem(cls, problem, fields='all', steps=None, sets=None, components=None, output=True,
                     exe=None, license='research'):
        results = cls(problem.name, problem.path, fields, steps, sets, output, components, exe, license)
        results.extract_data()
        return results

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

        else:
            keys = elements

        for key in keys:
            data[key] = rdict[field][key]

        return data

    # ==========================================================================
    # Serialization
    # ==========================================================================

    def save_cfr(self):
        with open(self.temp_dump, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print("***** .cfr file successfully saved! *****")

    @ classmethod
    def load_cfr(cls, path):
        with open(path, 'rb') as f:
            cls = pickle.load(f)
        return cls

    # ==========================================================================
    # Save results
    # ==========================================================================
    def save_to_json(self, path):
        with open(path, 'w') as f:
            json.dump(self, f)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class StepResults(FEAData):
    """`compas_fea2` ResultsStep object. This ensures that the results from
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
        super(StepResults, self).__init__(name=name)
        self.path = path
        self.temp_dump = Path(self.path).joinpath(self.name+'-results')
        self.info = {}
        self.nodal = {}
        self.element = {}
        self.modal = {}

    def serialize(self):
        with open(self.temp_dump, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def save_to_json(self, path=None):
        with open(path, 'w') as f:
            json.dump(self, f)
