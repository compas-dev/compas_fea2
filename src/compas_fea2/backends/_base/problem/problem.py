from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import pickle

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'ProblemBase',
]

class ProblemBase(object):
    """Initialises the Problem object.

    Parameters
    ----------
    name : str
        Name of the Structure.
    model : obj
        model object.


    bcs : dict
        Dictionary containing the boundary conditions objects.
    loads : dict
        Dictionary containing the loads objects.
    steps : list
        List containing the Steps objects.

    """

    def __init__(self, name, model):
        self.name               = name
        self.model              = model
        self.path               = None

        self.bcs                = {}
        self.loads              = {}
        self.steps              = []
        self.steps_order        = []
        self.field_outputs      = {}
        self.history_outputs    = {}

        self.results            = {}

    def __str__(self):
        data = [self.bcs,
                self.loads,
                # self.steps,
                # self.steps_order,
                self.field_outputs,
                self.history_outputs]
        d = []
        for entry in data:
            if entry:
                d.append('\n'.join(['  {0} : {1}'.format(i, j.__name__) for i, j in entry.items()]))
            else:
                d.append('n/a')
        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea Problem: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Boundary Conditions
-------------------
{}

Loads
-----
{}

Steps
-----
{}

Steps Order
-----------
{}

Field Output Requests
---------------------
{}

History Output Requests
-----------------------
{}


""".format(self.name, d[0], d[1], d[2], d[3], d[3], d[3])


    # =========================================================================
    #                           BCs methods
    # =========================================================================

    def add_bc(self, bc):
        if bc.bset not in self.model.sets.keys():
            sys.exit('ERROR: bc set {} not found in the model!'.format(bc.bset))
        if bc.name not in self.bcs.keys():
            self.bcs[bc.name] = bc

    def add_bcs(self, bcs):
        for bc in bcs:
            self.add_bc(bc)

    def remove_bc(self, bc_name):
        pass

    def remove_bcs(self, bcs):
        pass

    def remove_all_bcs(self):
        self.bcs = {}

    # =========================================================================
    #                           Loads methods
    # =========================================================================

    def add_load(self, load):
        if load.lset and load.lset not in self.model.sets:
            sys.exit('ERROR: load set {} not found in the model!'.format(load.lset))
        if load.name not in self.loads.keys():
            self.loads[load.name] = load

    def add_loads(self, loads):
        for load in loads:
            self.add_load(load)

    def remove_bc(self, bc_name):
        pass

    def remove_bcs(self, bcs):
        pass

    def remove_all_loads(self):
        self.loads = {}


    # =========================================================================
    #                           Step methods
    # =========================================================================

    def add_step(self, step):

        for disp in step.displacements:
            if disp not in self.displacements:
                sys.exit('ERROR: displacement {} not found in the model!'.format(disp))

        for load in step.loads:
            if load not in self.loads:
                sys.exit('ERROR: load {} not found in the model!'.format(load))

        for fout in step.field_outputs:
            if fout not in self.field_outputs:
                sys.exit('ERROR: field output {} not found in the model!'.format(fout))

        for hout in step.history_outputs:
            if hout not in self.history_outputs:
                sys.exit('ERROR: history output {} not found in the model!'.format(hout))

        self.steps.append(step)


    def add_steps(self, steps):
        for step in steps:
            self.add_step

    def define_steps_order(self, order):
        pass

    # =========================================================================
    #                           Field outputs
    # =========================================================================

    def add_field_output(self, fout):
        if fout.name not in self.field_outputs:
            self.field_outputs[fout.name] = fout

    def add_field_outputs(self, fouts):
        for fout in fouts:
            self.add_field_output(fout)

    # =========================================================================
    #                           History outputs
    # =========================================================================

    def add_history_output(self, hout):
        if hout.name not in self.history_outputs:
            self.history_outputs[hout.name] = hout

    def add_history_outputs(self, houts):
        for hout in houts:
            self.add_history_output(hout)


    # ==============================================================================
    # Modifiers
    # ==============================================================================

    # def scale_displacements(self, displacements, factor):
    #     """Scales displacements by a given factor.

    #     Parameters
    #     ----------
    #     displacements : dict
    #         Dictionary containing the displacements to scale.
    #     factor : float
    #         Factor to scale the displacements by.

    #     Returns
    #     -------
    #     dict
    #         The scaled displacements dictionary.
    #     """
    #     disp_dic = {}

    #     for key, disp in displacements.items():
    #         for dkey, dcomp in disp.components.items():
    #             if dcomp is not None:
    #                 disp.components[dkey] *= factor
    #         disp_dic[key] = disp

    #     return disp_dic

    # def scale_loads(self, loads, factor):
    #     """Scales loads by a given factor.

    #     Parameters
    #     ----------
    #     loads : dict
    #         Dictionary containing the loads to scale.
    #     factor : float
    #         Factor to scale the loads by.

    #     Returns
    #     -------
    #     dict
    #         The scaled loads dictionary.
    #     """
    #     loads_dic = {}

    #     for key, load in loads.items():
    #         for lkey, lcomp in load.components.items():
    #             if lcomp is not None:
    #                 load.components[lkey] *= factor
    #         loads_dic[key] = load

    #     return loads_dic

    # ==============================================================================
    # Steps
    # ==============================================================================

    # def set_steps_order(self, order):
    #     """Sets the order that the Steps will be analysed.

    #     Parameters
    #     ----------
    #     order : list
    #         An ordered list of the Step names.

    #     Returns
    #     -------
    #     None
    #     """
    #     self.steps_order = order

    # ==============================================================================
    # Results
    # ==============================================================================

    # def get_nodal_results(self, step, field, nodes='all'):
    #     """Extract nodal results from self.results.

    #     Parameters
    #     ----------
    #     step : str
    #         Step to extract from.
    #     field : str
    #         Data field request.
    #     nodes : str, list
    #         Extract 'all' or a node collection/list.

    #     Returns
    #     -------
    #     dict
    #         The nodal results for the requested field.
    #     """
    #     data  = {}
    #     rdict = self.results[step]['nodal']

    #     if nodes == 'all':
    #         keys = list(self.nodes.keys())
    #     else:
    #         keys = nodes

    #     for key in keys:
    #         data[key] = rdict[field][key]

    #     return data

    # def get_element_results(self, step, field, elements='all'):
    #     """Extract element results from self.results.

    #     Parameters
    #     ----------
    #     step : str
    #         Step to extract from.
    #     field : str
    #         Data field request.
    #     elements : str, list
    #         Extract 'all' or an element collection/list.

    #     Returns
    #     -------
    #     dict
    #         The element results for the requested field.
    #     """
    #     data  = {}
    #     rdict = self.results[step]['element']

    #     if elements == 'all':
    #         keys = list(self.elements.keys())

    #     # elif isinstance(elements, str):              TODO: transfor to 'collection'
    #     #     keys = self.sets[elements].selection

    #     else:
    #         keys = elements

    #     for key in keys:
    #         data[key] = rdict[field][key]

    #     return data



    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):
        """Prints a summary of the Structure object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print(self)

    # ==============================================================================
    # Save
    # ==============================================================================

    def save_to_cfp(self, path, output=True):
        """Exports the Problem object to an .cfp file through Pickle.

        Parameters
        ----------
        output : bool
            Print terminal output.

        Returns
        -------
        None
        """

        filename = '{0}/{1}.cfp'.format(path, self.name)

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        if output:
            print('***** Problem saved to: {0} *****\n'.format(filename))

    # ==============================================================================
    # Load
    # ==============================================================================

    @staticmethod
    def load_from_cfp(filename, output=True):
        """Imports a Problem object from an .cfp file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Problem .cfp from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Problem object.
        """
        with open(filename, 'rb') as f:
            probelm = pickle.load(f)

        if output:
            print('***** Problem loaded from: {0} *****'.format(filename))

        return probelm
