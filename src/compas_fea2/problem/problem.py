from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
from pathlib import Path

from compas_fea2.base import FEAData
from compas_fea2.problem.steps.step import _Step
from compas_fea2.job.input_file import InputFile

from compas_fea2.utilities._utils import timer


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
    steps : list of :class:`compas_fea2.problem._Step`
        list of analysis steps in the order they are applied.
    path : str, :class:`pathlib.Path`
        Path to the analysis folder where all the files will be saved.

    """

    def __init__(self, model, name=None, author=None, description=None, **kwargs):
        super(Problem, self).__init__(name=name, **kwargs)
        self.author = author
        self.description = description or f'Problem for {model}'
        self._path = None
        self._model = model
        self._steps = []

    @property
    def model(self):
        return self._model

    @property
    def steps(self):
        return self._steps

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value if isinstance(value, Path) else Path(value)

    # =========================================================================
    #                           Step methods
    # =========================================================================

    def is_step_in_problem(self, step, add=True):
        """Check if a :class:`compas_fea2.problem._Step` is defined in the Problem.

        Parameters
        ----------
        step : :class:`compas_fea2.problem._Step`
            The Step object to find.

        Returns
        -------
        :class:`compas_fea2.problem._Step`

        Raises
        ------
        ValueError
            if `step` is a string and the step is not defined in the problem
        TypeError
            `step` must be either an instance of a `compas_fea2` Step class or the
            name of a Step already defined in the Problem.
        """

        if not isinstance(step, _Step):
            raise TypeError('{!r} is not a Step'.format(step))
        if step.name not in self.steps:
            print('{!r} not found'.format(step))
            if add:
                step = self.add_step(step)
                print('{!r} added to the Problem'.format(step))
                return step
            return False
        return True

    def add_step(self, step) -> _Step:
        # # type: (Step) -> Step
        """Adds a :class:`compas_fea2.problem._Step` to the problem.

        Parameters
        ----------
        Step : :class:`compas_fea2.problem._Step`
            The analysis step to add to the problem.

        Returns
        -------
        :class:`compas_fea2.problem._Step`
        """
        if isinstance(step, _Step):
            self._steps.append(step)
        else:
            raise TypeError('You must provide a valid compas_fea2 Step object')
        return step

    def add_steps(self, steps):
        """Adds multiple :class:`compas_fea2.problem._Step` objects to the problem.

        Parameters
        ----------
        steps : list[:class:`compas_fea2.problem._Step`]
            List of steps objects in the order they will be applied.

        Returns
        -------
        list[:class:`compas_fea2.problem._Step`]
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

        Warning
        -------
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
        raise NotImplementedError

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
    @timer(message='Finished writing input file in')
    def write_input_file(self, path):
        """Writes the abaqus input file.

        Parameters
        ----------
        path : str, :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.

        Returns
        -------
        None
        """
        self.path = path
        if not self.path.exists():
            self.path.mkdir()
        input_file = InputFile.from_problem(self)
        input_file.write_to_file(self.path)

    def analyse(self, path, save=False):
        """Run the analysis through the registered backend.

        Parameters
        ----------
        path : str, :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.
        save : bool
            Save structure to .cfp before the analysis.

        Returns
        -------
        None

        """
        self.write_input_file(path)
        if save:
            self.save_to_cfp()

    # =========================================================================
    #                         Results methods
    # =========================================================================

    def extract(self):
        raise NotImplementedError("this function is not available for the selceted backend")
