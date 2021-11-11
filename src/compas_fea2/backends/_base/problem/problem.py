from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import pickle
from pathlib import Path

from compas_fea2.backends._base.base import FEABase
from compas_fea2.backends._base.problem.outputs import FieldOutputBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'ProblemBase',
]


class ProblemBase(FEABase):
    """Initialises the Problem object.

    Parameters
    ----------
    name : str
        Name of the Problem.
    model : obj
        model object.
    """

    def __init__(self, name, model):
        self.__name__ = 'Problem'
        self._name = name
        self._model = model
        self._path = None
        self._bcs = {}
        self._loads = {}
        self._steps = {}
        self._steps_order = []
        self._field_outputs = {}
        self._history_outputs = {}

    @property
    def name(self):
        """str : Name of the Problem"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def model(self):
        """obj : compas_fea2 Model object."""
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def path(self):
        """str, path obj : str or `pathlib.Path` object to the analysis folder."""
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def bcs(self):
        """dict : Dictionary containing the boundary conditions objects."""
        return self._bcs

    @bcs.setter
    def bcs(self, value):
        self._bcs = value

    @property
    def loads(self):
        """dict : Dictionary containing the loads objects."""
        return self._loads

    @loads.setter
    def loads(self, value):
        self._loads = value

    @property
    def steps(self):
        """dict : dict containing the Steps objects."""
        return self._steps

    @steps.setter
    def steps(self, value):
        self._steps = value

    @property
    def steps_order(self):
        """list : List containing the Steps names in the sequence they are applied."""
        return self._steps_order

    @steps_order.setter
    def steps_order(self, value):
        self._steps_order = value

    @property
    def field_outputs(self):
        """dict : Dictionary contanining the field output requests."""
        return self._field_outputs

    @field_outputs.setter
    def field_outputs(self, value):
        self._field_outputs = value

    @property
    def history_outputs(self):
        """dict : Dictionary contanining the history output requests."""
        return self._history_outputs

    @history_outputs.setter
    def history_outputs(self, value):
        self._history_outputs = value

    # =========================================================================
    #                           BCs methods
    # =========================================================================

    def add_bc(self, bc):
        """Adds a boundary condition to the Problem object.

        Parameters
        ----------
        bc : obj
            `compas_fea2` BoundaryCondtion object.

        Returns
        -------
        None
        """
        if bc.name not in self.bcs:
            self.bcs[bc.name] = bc
        else:
            print('WARNING: {} already present in the Problem. skipped!'.format(bc.__repr__()))

    def add_bcs(self, bcs):
        """Adds multiple boundary conditions to the Problem object.

        Parameters
        ----------
        bcs : list
            List of `compas_fea2` BoundaryCondtion objects.

        Returns
        -------
        None
        """
        for bc in bcs:
            self.add_bc(bc)

    def remove_bc(self, bc_name):
        """Removes a boundary condition from the Problem object.

        Parameters
        ----------
        bc_name : str
            Name of the boundary condition to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_bcs(self, bc_names):
        """Removes multiple boundary conditions from the Problem object.

        Parameters
        ----------
        bc_names : list
            List of names of the boundary conditions to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_bcs(self):
        """Removes all the boundary conditions from the Problem object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.bcs = {}

    # =========================================================================
    #                           Loads methods
    # =========================================================================

    def add_load(self, load):
        """Adds a load to the Problem object.

        Parameters
        ----------
        load : list
            List of `compas_fea2` Load objects.

        Returns
        -------
        None
        """
        if load.name not in self.loads:
            self.loads[load.name] = load
        else:
            print('WARNING: {} already present in the Problem. skipped!'.format(load.__repr__()))

    def add_loads(self, loads):
        """Adds multiple loads to the Problem object.

        Parameters
        ----------
        loads : list
            List of `compas_fea2` Load objects.

        Returns
        -------
        None
        """
        for load in loads:
            self.add_load(load)

    def remove_load(self, load_name):
        """Removes a load from the Problem object.

        Parameters
        ----------
        load_name : list
            Name of the load to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_loads(self, load_names):
        """Removes multiple loads from the Problem object.

        Parameters
        ----------
        load_names : list
            List of the names of the loads to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_loads(self):
        """Removes all the loads from the Problem object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.loads = {}

    # =========================================================================
    #                           Outputs methods
    # =========================================================================

    def add_output(self, output):
        """Adds an output to the Problem object.

        Parameters
        ----------
        output : obj
            `compas_fea2` Output objects.

        Returns
        -------
        None
        """
        attrb_name = 'field_outputs' if isinstance(output, FieldOutputBase) else 'history_output'
        if output.name not in getattr(self, attrb_name):
            getattr(self, attrb_name)[output.name] = output
        else:
            print('WARNING: {} already present in the Problem. skipped!'.format(output.__repr__()))

    def add_outputs(self, outputs):
        """Adds multiple outputs to the Problem object.

        Parameters
        ----------
        outputs : list
            List of `compas_fea2` output objects.

        Returns
        -------
        None
        """
        for output in outputs:
            self.add_output(output)

    def remove_output(self, load_name):
        """Removes a load from the Problem object.

        Parameters
        ----------
        load_name : list
            Name of the load to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_outputs(self, load_names):
        """Removes multiple loads from the Problem object.

        Parameters
        ----------
        load_names : list
            List of the names of the loads to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_output(self):
        """Removes all the loads from the Problem object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._field_outputs = {}
        self._history_outputs = {}

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def add_step(self, step):
        """Adds a Step to the Problem object.

        Parameters
        ----------
        Step : obj
            `compas_fea2` Step object.

        Returns
        -------
        None
        """

        if step.name in self.steps:
            print('WARNING: {} already present in the Problem. skipped!'.format(step.__repr__()))
        else:
            for disp in step.displacements:
                if disp not in self.displacements:
                    self.add_bc(disp)

            for load in step.loads:
                if load not in self.loads:
                    self.add_load(load)

            if step.field_outputs not in self.field_outputs:
                self.add_field_output(step.field_outputs)

            if step.history_outputs not in self.history_outputs:
                self.add_history_output(step.history_outputs)
            self._steps[step.name] = step
            self._steps_order.append(step.name)

    def add_steps(self, steps):
        """Adds multiple steps to the Problem object.

        Parameters
        ----------
        steps : list
            List of `compas_fea2` Step objects in the order they will be applied.

        Returns
        -------
        None
        """
        for step in steps:
            self.add_step(step)

    def define_steps_order(self, order):
        """Defines the order in which the steps are applied during the analysis.

        Parameters
        ----------
        order : list
            List contaning the names of the analysis steps in the order in which
            they are meant to be applied during the analysis.

        Returns
        -------
        None

        Note
        ----
        Not implemented yet!
        """
        raise NotImplementedError

    # =========================================================================
    #                           Field outputs
    # =========================================================================

    def add_field_output(self, fout):
        """Adds a FieldOutput object to the Problem object.

        Parameters
        ----------
        fout : obj
            `compas_fea2` FieldOutput object.

        Returns
        -------
        None
        """
        if fout.name not in self.field_outputs:
            self.field_outputs[fout.name] = fout

    def add_field_outputs(self, fouts):
        """Adds multiple FieldOutput objects to the Problem object.

        Parameters
        ----------
        fouts : list
            List containing `compas_fea2` FieldOutput objects to be added.

        Returns
        -------
        None
        """
        for fout in fouts:
            self.add_field_output(fout)

    # =========================================================================
    #                           History outputs
    # =========================================================================

    def add_history_output(self, hout):
        """Adds a HistoryOutput object to the Problem object.

        Parameters
        ----------
        hout : obj
            `compas_fea2` HistoryOutput object to be added.

        Returns
        -------
        None
        """
        if hout.name not in self.history_outputs:
            self.history_outputs[hout.name] = hout

    def add_history_outputs(self, houts):
        """Adds multiple HistoryOutput objects to the Problem object.

        Parameters
        ----------
        houts : list
            List containing `compas_fea2` HistoryOutput objects to be added.

        Returns
        -------
        None
        """
        for hout in houts:
            self.add_history_output(hout)

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
        data = [self.bcs,
                self.loads,
                # self.steps,
                # self.steps_order,
                self.field_outputs,
                self.history_outputs]
        d = []
        for entry in data:
            if entry:
                d.append('\n'.join(['  {0} : {1}'.format(
                    i, j.__name__) for i, j in entry.items()]))
            else:
                d.append('n/a')

        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Problem: {}
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
        problem : obj
            Imported `compas_fea2` Problem object.
        """
        with open(filename, 'rb') as f:
            probelm = pickle.load(f)

        if output:
            print('***** Problem loaded from: {0} *****'.format(filename))

        return probelm

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    def write_input_file(self):
        raise NotImplementedError("this function is not available for the selceted backend")

    def analyse(self):
        raise NotImplementedError("this function is not available for the selceted backend")

    def optimise(self):
        raise NotImplementedError("this function is not available for the selceted backend")

    # =========================================================================
    #                         Results methods
    # =========================================================================

    def extract(self):
        raise NotImplementedError("this function is not available for the selceted backend")
