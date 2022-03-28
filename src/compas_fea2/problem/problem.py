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
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    model : :class:`compas_fea2.model.Model`
        Model object to analyse.
    author : str, optional
        The author of the Model, by default ``None``.
        This will be added to the input file and can be useful for future reference.
    describption : str, optional
        Brief description of the Problem, , by default ``None``.
        This will be added to the input file and can be useful for future reference.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    model : :class:`compas_fea2.model.Model`
        Model object to analyse.
    author : str
        The author of the Model. This will be added to the input file and
        can be useful for future reference.
    describption : str
        Brief description of the Problem. This will be added to the input file and
        can be useful for future reference.
    steps : list of :class:`compas_fea2.problem.Step`
        list of analysis steps in the order they are applied.
    path : str, :class:`pathlib.Path`
        Path to the analysis folder where all the files will be saved.

    """

    def __init__(self, model, name=None, author=None, description=None, **kwargs):
        super(Problem, self).__init__(name=name, **kwargs)
        self.author = author
        self.description = description or f'Problem for {model}'
        self.path = None
        self._model = model
        self._steps = []

    @property
    def model(self):
        return self._model

    @property
    def steps(self):
        return self._steps

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def is_step_in_problem(self, step):
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

    def add_step(self, step) -> Step:
        # # type: (Step) -> Step
        """Adds a Step to the Problem object.

        Parameters
        ----------
        Step : obj
            :class:`Step` subclass object.

        Returns
        -------
        None
        """
        if isinstance(step, Step):
            self._steps.append(step)
        else:
            raise TypeError('You must provide a valid compas_fea2 Step object')
        return step

    def add_steps(self, steps):
        """Adds multiple steps to the Problem object.

        Parameters
        ----------
        steps : list[:class:`compas_fea2.problem.Step`]
            List of steps objects in the order they will be applied.

        Returns
        -------
        list[:class:`compas_fea2.problem.Step`]
        """
        return [self.add_step(step) for step in steps]

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
            :class:`compas_fea2.problem.LinearPerturbation` subclass instance
        base_step : str
            name of a previously defined step which will be used as starting conditions
            for the application of the linear perturbation step.
        """
        raise NotImplementedError()

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
        steps_data = '\n'.join([f'{step.name}' for step in self.steps])

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
        from compas_fea2.UI.viewer import ProblemViewer
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
