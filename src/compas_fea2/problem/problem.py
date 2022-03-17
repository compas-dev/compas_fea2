from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
import importlib

from compas_fea2.base import FEAData
from compas_fea2.problem.displacements import GeneralDisplacement
from compas_fea2.problem.steps import Step


class Problem(FEAData):
    """Initialises the Problem object.

    Parameters
    ----------
    name : str
        Name of the Problem.
    model : obj
        model object.
    """

    def __init__(self, name, model, author=None, description=None):
        super(Problem, self).__init__(name=name)
        self._author = author
        self._description = description or f'Problem for {model}'
        self._model = model
        self._steps = {}
        self._steps_order = []
        self._path = None

    @property
    def author(self):
        """str : The author of the Model. This will be added to the input file and
        can be useful for future reference."""
        return self._author

    @property
    def description(self):
        """str : Some description of the Problem. This will be added to the input file and
        can be useful for future reference."""
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def model(self):
        """obj : compas_fea2 Model object."""
        return self._model

    @property
    def path(self):
        """str, Path obj : str or `pathlib.Path` object to the analysis folder."""
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def steps(self):
        """dict : dict containing the Steps objects."""
        return self._steps

    @property
    def steps_order(self):
        """list : List containing the Steps names in the sequence they are applied."""
        return self._steps_order

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def _check_step_in_problem(self, step):
        """Check if a step is defined in the Problem. If `step` is of type `str`,
        check if the step is already defined. If `step` is of type `Step`,
        add the step to the Problem if not already defined.

        Parameters
        ----------
        step : str, obj
            Name of the step (must be already defined) or Step object.

        Returns
        -------
        obj
            Step object

        Raises
        ------
        ValueError
            if `step` is a string and the step is not defined in the problem
        TypeError
            `step` must be either an instance of a `compas_fea2` Step class or the
            name of a Step already defined in the Problem.
        """
        if isinstance(step, str):
            if step not in self._steps:
                raise ValueError(f'{step} not found in the Problem')
            step_name = step
        elif isinstance(step, Step):
            if step.name not in self.steps:
                self.add_step(step)
                print(f'{step!r} added to the Problem')
            step_name = step.name
        else:
            raise TypeError(
                f'{step!r} is either not an instance of a `compas_fea2` Step class or not found in the Problem')

        return self.steps[step_name]

    def add_step(self, step, append=True):
        """Adds a Step to the Problem object.

        Parameters
        ----------
        Step : obj
            :class:`Step` subclass object.
        append : bool
            if ``True`` add it to the step_order sequence.

        Returns
        -------
        None
        """
        if isinstance(step, Step):
            if step._name in self._steps:
                print(f'WARNING: {step!r} already defined in the Problem. skipped!')
            else:
                self._steps[step._name] = step
                if append:
                    self._steps_order.append(step._name)
        else:
            raise TypeError('You must provide a Step/Step object')

    def add_steps(self, steps):
        """Adds multiple steps to the Problem object.

        Parameters
        ----------
        steps : list
            List of :class:`Step` subclass objects in the order they will be
            applied.

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

    def add_linear_perturbation_step(self, lp_step, base_step):
        """Add a linear perturbation step to a previously defined step.

        Note
        ----
        Linear perturbartion steps do not change the history of the problem (hence
        following steps will not consider their effects).

        Parameters
        ----------
        lp_step : obj
            :class:`LinearPerturbationBase` subclass instance
        base_step : str
            name of a previously defined step which will be used as starting conditions
            for the application of the linear perturbation step.
        """
        raise NotImplementedError()
    # =========================================================================
    #                           Displacements methods
    # =========================================================================

    def add_displacement(self, displacement, step=None):
        """Add a displacement to the Problem object and optionally to a Step.

        Parameters
        ----------
        displacement : obj, str
            :class:`GeneralDisplacementBase` subclass object or name of the object.
        step : obj or str, optional
            :class:`Step` subclass object or name of the object, by default
            ``None``.

        Returns
        -------
        None
        """

        if step:
            if isinstance(step, Step):
                if step._name not in self._steps:
                    self.add_step(step)
                    print(f'{step!r} added to the Problem')
                step_name = step._name
            else:
                if step not in self._steps:
                    raise ValueError(
                        'The step provided is either not an instance of a compas_fea2 Step subclass or not found in the Problem')
                step_name = step

            if isinstance(displacement, GeneralDisplacement):
                if displacement._name not in self._displacements:
                    self._displacements[displacement._name] = displacement
                    print(f'{displacement!r} added to {self!r}')
                displacement_name = displacement._name
            else:
                if displacement not in self._displacements:
                    raise ValueError("ERROR : dispalcement not found!")
                displacement_name = displacement

            self._steps[step_name].add_displacement(self._displacements[displacement_name])
            print(f'{self._displacements[displacement_name]!r} added to {self._steps[step_name]!r}')

        else:
            if not isinstance(displacement, GeneralDisplacement):
                raise ValueError('You must provide a Displacement object.')
            if displacement._name not in self._displacements:
                self._displacements[displacement._name] = displacement
                print(f'{displacement!r} added to {self!r}')

    def add_displacements(self, displacements, step):
        """Adds multiple displacements to the a Step in Problem object.

        Parameters
        ----------
        displacements : list
            List of :class:`GeneralDisplacementBase` subclass objects.

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
            Name of the Displacement to remove.
        stap_name : str
            Name of the Step where the Displacement will be removed from.

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
        stap_name : str
            Name of the Step where the Displacement will be removed from.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_displacements(self, step_name):
        """Removes all the Displacements from a Step.

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
    def add_point_load(self, name, step, part, where, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        """Apply a :class:`PointLoadBase` subclass object to a Part in a Step.

        Parameters
        ----------
        name : str
            name of the PointLoad
        step : str
            name of the Step
        part : str
            name of the Part
        where : int or list(int), obj
            It can be either a key or a list of keys, or a NodesGroup of the nodes where the load is
            applied.
        x : float, optional
            x component of force, by default ``None``.
        y : float, optional
            y component of force, by default ``None``.
        z : float, optional
            z component of force, by default ``None``.
        xx : float, optional
            xx component of moment, by default ``None``.
        yy : float, optional
            yy component of moment, by default ``None``.
        zz : float, optional
            zz component of moment, by default ``None``.
        axes : str, optional
            Load applied via 'local' or 'global' axes, by default ``global``.
        """
        # FIXME in this way it is not possible to check if the part is in the model
        step = self._check_step_in_problem(step)
        step.add_point_load(name, part, where, x, y, z, xx, yy, zz, axes)

    def add_gravity_load(self, name, step, g=9.81, x=0., y=0., z=-1.):
        step = self._check_step_in_problem(step)
        step.add_gravity_load(name, g, x, y, z)

    def add_prestress_load(self):
        raise NotImplementedError()

    def add_line_load(self):
        raise NotImplementedError()

    def add_area_load(self):
        raise NotImplementedError()

    def add_tributary_load(self):
        raise NotImplementedError()

    def add_harmonic_point_load(self):
        raise NotImplementedError()

    def add_harmonic_preassure_load(self):
        raise NotImplementedError()

    def add_acoustic_diffuse_field_load(self):
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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

    def add_output(self, output, step):
        """Add a FieldOutput or HistoryOutput to a Step.

        Parameters
        ----------
        output : obj
            `compas_fea2` FieldOutput or HistoryOutput object.
        step : obj or str
            `compas_fea2` Step object or name of the object.

        Returns
        -------
        None
        """

        step = self._check_step_in_problem(step)
        step.add_output(output)

    def add_outputs(self, outputs, step):
        """Adds multiple outputs to the Problem object.

        Parameters
        ----------
        outputs : list
            List of `compas_fea2` output objects. Can be either a FieldOutput or a HistoryOutput
        step : obj or str
            `compas_fea2` Step object or name of the object.

        Returns
        -------
        None
        """
        for output in outputs:
            self.add_output(output, step)

    def remove_output(self, output_name, step):
        """Removes a output from the Problem object.

        Parameters
        ----------
        output_name : list
            Name of the output to remove. Can be either a FieldOutput or a HistoryOutput
        step : obj or str
            `compas_fea2` Step object or name of the object.

        Returns
        -------
        None
        """
        raise NotImplementedError()

    def remove_all_output(self, step):
        """Removes all the outputs from the Problem object. Both FieldOutputs and HistoryOutputs
        are erased.

        Parameters
        ----------
        step : obj or str
            `compas_fea2` Step object or name of the object.

        Returns
        -------
        None
        """
        raise NotImplementedError()

    # =========================================================================
    #                           Field outputs
    # =========================================================================

    def add_field_output(self, name, node_outputs, element_outputs, step):
        """Adds a FieldOutput object to the Problem object.

        Parameters
        ----------
        name : str
            name of the FieldOutput to be added
        nodes_outputs : list
            list of node fields to output
        elements_outputs : list
            list of elements fields to output
        step : obj or str
            `compas_fea2` Step object or name of the object.

        Returns
        -------
        None
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        output = m.FieldOutput(name, node_outputs, element_outputs)
        self.add_output(output, step)

    # =========================================================================
    #                           History outputs
    # =========================================================================

    def add_history_output(self, name, step):
        """Adds a HistoryOutput object to the Problem object.

        Parameters
        ----------
        name : str
            name of the HistoryOutput object to be added.

        Returns
        -------
        None
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        output = m.HistoryOutput(name)
        self.add_output(output, step)

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
        steps_data = '\n'.join([f'{self.steps[step].name}: {self.steps[step].__name__}' for step in self.steps_order])

        summary = f"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Problem: {self._name}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

description: {self.description}
author: {self.author}

Steps (in order of application)
-------------------------------
{steps_data}

"""
        print(summary)
        return summary

    # ==============================================================================
    # Viewer
    # ==============================================================================

    def show(self, width=800, height=500, scale_factor=.001, node_lables=None):
        from compas_fea2.interfaces.viewer import ProblemViewer

        v = ProblemViewer(self, width, height, scale_factor, node_lables)
        v.show()

    # ==============================================================================
    # Save and Load
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

        filename = f'{path}/{self.name}.cfp'

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        if output:
            print(f'***** Problem saved to: {filename} *****\n')

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
            print(f'***** Problem loaded from: {filename} *****\n')

        return probelm

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    def write_input_file(self):
        raise NotImplementedError("this function is not available for the selceted backend")

    def analyse(self):
        raise NotImplementedError("this function is not available for the selceted backend")

    # =========================================================================
    #                         Results methods
    # =========================================================================

    def extract(self):
        raise NotImplementedError("this function is not available for the selceted backend")
