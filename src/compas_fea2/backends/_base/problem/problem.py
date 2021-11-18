from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import pickle
from pathlib import Path

from compas_fea2.backends._base.base import FEABase
from compas_fea2.backends._base.problem.bcs import GeneralDisplacementBase
from compas_fea2.backends._base.problem.loads import LoadBase
from compas_fea2.backends._base.problem.outputs import FieldOutputBase, HistoryOutputBase
from compas_fea2.backends._base.problem.steps import CaseBase

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
        self.__name__ = 'ProblemBase'
        self._name = name
        self._model = model
        self._path = None
        self._bcs = {}
        self._loads = {}
        self._displacements = {}
        self._steps = {}
        self._steps_order = []
        self._field_outputs = {}
        self._history_outputs = {}

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

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
        """dict : Dictionary containing the load objects."""
        return self._loads

    @loads.setter
    def loads(self, value):
        self._loads = value

    @property
    def displacements(self):
        """"dict : Dictionary containing the displacement objects."""
        return self._displacements

    @displacements.setter
    def displacements(self, value):
        self._displacements = value

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

        if bc._name not in self._bcs:
            if not isinstance(bc, GeneralDisplacementBase):
                raise ValueError(f'{bc} not instance of a Displacement class')
            self.bcs[bc._name] = bc
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
            Name of thedisplacement to remove.

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
    #                           Displacements methods
    # =========================================================================

    def add_displacement(self, displacement, step=None):
        """Add a displacement to the Problem object and optionally to a Step.

        Parameters
        ----------
        displacement : obj, str
            `compas_fea2` Displacement object or name of the object.
        step : obj or str, optional
            `compas_fea2` Step object or name of the object, by default None.

        Returns
        -------
        None
        """

        if step:
            if isinstance(step, CaseBase):
                if step._name not in self._steps:
                    self.add_step(step)
                    print(f'{step.__repr__()} added to the Problem')
                step_name = step._name
            else:
                if step not in self._steps:
                    raise ValueError(
                        'The step provided is either not an instance of a `compas_fea2` Step class or not found in the Problem')
                step_name = step

            if isinstance(displacement, GeneralDisplacementBase):
                if displacement._name not in self._displacements:
                    self._displacements[displacement._name] = displacement
                    print(f'{displacement.__repr__()} added to {self.__repr__()}')
                displacement_name = displacement._name
            else:
                if displacement not in self._displacements:
                    raise ValueError("ERROR : dispalcement not found!")
                displacement_name = displacement

            self._steps[step_name].add_displacement(self._displacements[displacement_name])
            print(f'{self._displacements[displacement_name].__repr__()} added to {self._steps[step_name].__repr__()}')

        else:
            if not isinstance(displacement, GeneralDisplacementBase):
                raise ValueError('You must provide a Displacement object.')
            if displacement._name not in self._displacements:
                self._displacements[displacement._name] = displacement
                print(f'{displacement.__repr__()} added to {self.__repr__()}')

    def add_displacements(self, displacements, step):
        """Adds multiple displacements to the a Step in Problem object.

        Parameters
        ----------
        displacements : list
            List of `compas_fea2` Displacement objects.

        Returns
        -------
        None
        """
        for displacement in displacements:
            self.add_displacement(displacement, step)

    def remove_displacement(self, displacement_name, step_name):
        """Removes a boundary condition from the Problem object.

        Parameters
        ----------
        displacement_name : str
            Name of thedisplacement to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_displacements(self, displacement_names, step_name):
        """Removes multiple boundary conditions from the Problem object.

        Parameters
        ----------
        displacement_names : list
            List of names of the displacements to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_displacement(self, step_name):
        """Removes all the Displacements from a Step in the Problem object.

        Parameters
        ----------
        step_name : str
            name of the step to be erased

        Returns
        -------
        None
        """
        self.steps[step_name].remove_all_displacements()

    # =========================================================================
    #                           Loads methods
    # =========================================================================

    def add_load(self, load, step=None):
        """Add a load to the Problem object and optionally to a Step.

        Parameters
        ----------
        load : obj, str
            `compas_fea2` Load object or name of the object.
        step : obj or str, optional
            `compas_fea2` Step object or name of the object, by default None.

        Returns
        -------
        None
        """

        if step:
            if isinstance(step, CaseBase):
                if step._name not in self._steps:
                    self.add_step(step)
                    print(f'{step.__repr__()} added to the Problem')
                step_name = step._name
            elif isinstance(step, str):
                if step not in self._steps:
                    raise ValueError(
                        'The step provided is either not an instance of a `compas_fea2` Step class or not found in the Problem')
                step_name = step
            else:
                raise ValueError()

            if isinstance(load, LoadBase):
                if load._name not in self._loads:
                    self._loads[load._name] = load
                    print(f'{load.__repr__()} added to {self.__repr__()}')
                load_name = load._name
            else:
                if load not in self._loads:
                    raise ValueError("ERROR : dispalcement not found!")
                load_name = load

            self._steps[step_name].add_load(self._loads[load_name])
            print(f'{self._loads[load_name].__repr__()} added to {self._steps[step_name].__repr__()}')

        else:
            if not isinstance(load, LoadBase):
                raise ValueError('You must provide a Displacement object.')
            if load._name not in self._loads:
                self._loads[load._name] = load
                print(f'{load.__repr__()} added to {self.__repr__()}')

    def add_loads(self, loads, step=None):
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
            self.add_load(load, step)

    def remove_load(self, load_name, step_name):
        """Removes a Load from the Problem object.

        Parameters
        ----------
        load_name : str
            Name of the load to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_loads(self, load_names, step_name):
        """Removes multiple Loads from the Problem object.

        Parameters
        ----------
        load_names : list
            List of names of the loads to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_loads(self, step_name):
        """Removes all the loads from a Step in the Problem object.

        Parameters
        ----------
        step_name : str
            name of the step to be erased

        Returns
        -------
        None
        """
        self.steps[step_name].remove_all_loads()

    # =========================================================================
    #                           Outputs methods
    # =========================================================================

    def add_output(self, output, step=None):
        """Add a displacement to the Problem object and optionally to a Step.

        Parameters
        ----------
        displacement : obj, str
            `compas_fea2` Displacement object or name of the object.
        step : obj or str, optional
            `compas_fea2` Step object or name of the object, by default None.

        Returns
        -------
        None
        """

        if step:
            if isinstance(step, CaseBase):
                if step._name not in self._steps:
                    self.add_step(step)
                    print(f'{step.__repr__()} added to the Problem')
                step_name = step._name
            else:
                if step not in self._steps:
                    raise ValueError(
                        'The step provided is either not an instance of a `compas_fea2` Step class or not found in the Problem')
                step_name = step

            attrb_name = '_field_outputs' if isinstance(output, FieldOutputBase) else '_history_outputs'
            if isinstance(output, FieldOutputBase) or isinstance(output, HistoryOutputBase):
                if output._name not in getattr(self, attrb_name):
                    getattr(self, attrb_name)[output._name] = output
                    print(f'{output.__repr__()} added to {self.__repr__()}')
                output_name = output._name
            else:
                if output not in getattr(self, attrb_name):
                    raise ValueError("ERROR : output not found!")
                output_name = output

            self._steps[step_name].add_output(getattr(self, attrb_name)[output_name])
            print(f'{getattr(self, attrb_name)[output_name].__repr__()} added to {self._steps[step_name].__repr__()}')

        else:
            if not isinstance(output, GeneralDisplacementBase):
                raise ValueError('You must provide a Displacement object.')
            attrb_name = '_field_outputs' if isinstance(output, FieldOutputBase) else '_history_output'
            if output._name not in getattr(self, attrb_name):
                getattr(self, attrb_name)[output._name] = output
                print(f'{output.__repr__()} added to {self.__repr__()}')

    def add_outputs(self, outputs, step=None):
        """Adds multiple outputs to the Problem object.

        Parameters
        ----------
        outputs : list
            List of `compas_fea2` output objects. Can be either a FieldOutput or a HistoryOutput

        Returns
        -------
        None
        """
        for output in outputs:
            self.add_output(output, step)

    def remove_output(self, output_name, step_name):
        """Removes a output from the Problem object.

        Parameters
        ----------
        output_name : list
            Name of the output to remove. Can be either a FieldOutput or a HistoryOutput

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_outputs(self, output_names, step_name):
        """Removes multiple outputs from the Problem object.

        Parameters
        ----------
        output_names : list
            List of the names of the outputs to remove. Can be either a FieldOutput or a HistoryOutput

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_output(self, step_name):
        """Removes all the outputs from the Problem object. Both FieldOutputs and HistoryOutputs
        are erased.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._steps[step_name]._field_outputs = {}
        self._steps[step_name]._history_outputs = {}

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def add_step(self, step, append=True):
        """Adds a Step to the Problem object.

        Parameters
        ----------
        Step : obj
            `compas_fea2` Step object.
        append : bool
            if True add it to the step_order sequence.

        Returns
        -------
        None
        """

        if step._name in self._steps:
            print('WARNING: {} already defined in the Problem. skipped!'.format(step.__repr__()))
        else:
            self._steps[step._name] = step
            if step._displacements:
                for displacement in step._displacements:
                    if isinstance(displacement, GeneralDisplacementBase):
                        if displacement._name not in self._displacements:
                            self._displacements[displacement._name] = displacement
                    else:
                        raise ValueError()
            if step._loads:
                for load in step._loads:
                    if isinstance(load, LoadBase):
                        if load._name not in self._loads:
                            self._loads[load._name] = load
                    else:
                        raise ValueError()

            if step._field_outputs:
                for field_output in step._field_outputs:
                    if isinstance(displacement, FieldOutputBase) or isinstance(displacement, FieldOutputBase):
                        if field_output._name not in self._field_outputs:
                            self._field_outputs[field_output._name] = field_output
                    else:
                        raise ValueError()

            if step._history_outputs:
                for history_output in step._history_outputs:
                    if isinstance(displacement, GeneralDisplacementBase):
                        if history_output._name not in self._history_outputs:
                            self._history_outputs[history_output._name] = history_output
                    else:
                        raise ValueError()
            if append:
                self._steps_order.append(step._name)

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
        data = [self._name,
                '\n'.join([f'{name.__repr__()}' for name in self.bcs.values()]),
                '\n'.join([f'{name.__repr__()}' for name in self.steps.values()]),
                '\n'.join([f'{name}' for name in self.steps_order])
                ]

        summary = """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Problem: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Boundary Conditions
-------------------
{}

Steps
-----
{}

Steps Order
-----------
{}

""".format(*data)

        print(summary)

        return summary

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

    @ staticmethod
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
