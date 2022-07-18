from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
from pathlib import Path

from compas_fea2.base import FEAData
from compas_fea2.problem.steps.step import _Step
from compas_fea2.job.input_file import InputFile
from compas_fea2.results.results import StepResults

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
    results : :class:`compas_fea2.results.Results`
        Results object with the analyisis results.

    """

    def __init__(self, model, name=None, author=None, description=None, **kwargs):
        super(Problem, self).__init__(name=name, **kwargs)
        self.author = author
        self.description = description or 'Problem for {}'.format(model.name)
        self._path = None
        self._model = model
        self._steps = set()
        self._steps_order = []
        self._results = None

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

    @property
    def results(self):
        return self._results

    # =========================================================================
    #                           Step methods
    # =========================================================================
    def find_step_by_name(self, name):
        # type: (str) -> _Step
        """Find if there is a step with the given name in the problem.

        Parameters
        ----------
        name : str

        Returns
        -------
        :class:`compas_fea2.problem._Step`

        """
        for step in self.steps:
            if step.name == name:
                return step

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
        if step not in self.steps:
            print('{!r} not found'.format(step))
            if add:
                step = self.add_step(step)
                print('{!r} added to the Problem'.format(step))
                return step
            return False
        return True

    def add_step(self, step) -> _Step:
        # # type: (Step) -> Step
        """Adds a :class:`compas_fea2.problem._Step` to the problem. The name of
        the Step must be unique

        Parameters
        ----------
        Step : :class:`compas_fea2.problem._Step`
            The analysis step to add to the problem.

        Returns
        -------
        :class:`compas_fea2.problem._Step`
        """
        if isinstance(step, _Step):
            if self.find_step_by_name(step):
                raise ValueError('There is already a step with the same name in the model.')
            self._steps.add(step)
            self._steps_order.append(step)
            step._problem = self
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
        for step in order:
            if not isinstance(step, _Step):
                raise TypeError('{} is not a step'.format(step))
        self._steps_order = order

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

    def analyse(self, *args, **kwargs):
        raise NotImplementedError("this function is not available for the selected backend")

    @timer(message='Finished analysis and data extraction in')
    def analyse_and_extract(self, fields=None, *args, **kwargs):
        """Run the analysis through the registered backend.

        Parameters
        ----------
        fields : list
            Output fields to extract, by default 'None'. If `None` all available
            fields will be extracted, which might require considerable time.

        Returns
        -------
        None

        """
        import json
        from compas_fea2.results import StepResults
        self.analyse(*args, **kwargs)
        self.get_results()
        results_file = self._results.extract_data(fields)
        # Save results back into the Results object
        with open(results_file, 'rb') as f:
            results = json.load(f)
            for step in results:
                for part in results[step]:
                    step_obj = self.find_step_by_name(step)
                    if not step_obj:
                        raise ValueError('Step {} not found in the problem'. format(step))

                    # TODO create a copy of the model for each step
                    step_results = self._results.add_step_results(StepResults(step_obj, self.model))

                    for result_type in ['nodes', 'elements']:
                        if result_type in results[step][part]:
                            items = getattr(step_results.model.find_part_by_name(part), result_type)
                            for key, fields in results[step][part][result_type].items():
                                item = [item for item in items if item.key == int(key)][0]
                                if not hasattr(item, 'results'):
                                    item.__setattr__('results', {})
                                item.results[step] = fields

    # =========================================================================
    #                         Results methods
    # =========================================================================

    def get_results(self):
        from compas_fea2.results import Results
        self._results = Results(database_path=self.path, database_name=self.name)

    def get_step_results(self, step):
        for step_results in self.results.steps:
            if step == step_results.step:
                return step_results

    # ==============================================================================
    # Viewer
    # ==============================================================================
    def show(self, width=1600, height=900, scale_factor=1., steps=None, parts=None,
             draw_original=True,
             draw_elements=True, draw_nodes=False, node_labels=False,
             draw_bcs=1., draw_loads=None, **kwargs):

        from compas_fea2.UI.viewer import FEA2Viewer
        from compas.geometry import Point, Vector
        import numpy as np

        from compas.colors import ColorMap, Color
        cmap = ColorMap.from_mpl('viridis')

        steps = steps or self.steps
        parts = parts or self.model.parts

        v = FEA2Viewer(width, height, scale_factor)

        if draw_original:
            v.draw_parts(parts,
                         draw_elements,
                         draw_nodes,
                         node_labels)

        if 'displacements' in kwargs:
            for step in steps:
                pts = []
                vectors = []
                lengths = []
                for part in parts:
                    for node in part.nodes:
                        x, y, z = node.results[step.name]['U']
                        vector = Vector(x=x,
                                        y=y,
                                        z=z)
                        if vector.length == 0:
                            continue
                        vector.scale(kwargs['displacements'])
                        vectors.append(vector)
                        lengths.append(vector.length)
                        pts.append(Point(*node.xyz))
                max_length = max([abs(length) for length in lengths])
                colors = [cmap(value/max_length) for value in lengths]

                v.draw_nodes_vector(pts, vectors, colors)

        # TODO create a copy of the model first
        if 'deformed' in kwargs:
            for step in steps:
                step_results = self.get_step_results(step)
                model = step_results.get_deformed_model(scale=kwargs['deformed'])
                deformed_parts = [model.find_part_by_name(part.name) for part in parts]
                v.draw_parts(deformed_parts,
                             draw_elements,
                             draw_nodes,
                             node_labels)

        if draw_bcs:
            v.draw_bcs(self.model, parts, draw_bcs)

        if draw_loads:
            v.draw_loads(steps, draw_loads)

        if 'nforces' in kwargs:
            for step in steps:
                pts = []
                vectors = []
                lengths = []
                for part in parts:
                    for node in part.nodes:
                        vector = Vector(x=node.results[step.name]['NFORC1'][0],
                                        y=node.results[step.name]['NFORC2'][0],
                                        z=node.results[step.name]['NFORC3'][0])
                        if vector.length == 0:
                            continue
                        vector.scale(kwargs['nforces'])
                        vectors.append(vector)
                        lengths.append(vector.length)
                        pts.append(Point(*node.xyz))
                max_length = max([abs(length) for length in lengths])
                colors = [cmap(value/max_length) for value in lengths]
                v.draw_nodes_vector(pts, vectors, colors)

        # TODO add reaction moments RM
        if 'reactions' in kwargs:
            for step in steps:
                pts = []
                vectors = []
                lengths = []
                for part in parts:
                    for node in part.nodes:
                        x, y, z = node.results[step.name]['RF']
                        vector = Vector(x=x,
                                        y=y,
                                        z=z)
                        if vector.length == 0:
                            continue
                        vector.scale(kwargs['reactions'])
                        vectors.append(vector)
                        lengths.append(vector.length)
                        pts.append(Point(*node.xyz))
                max_length = max([abs(length) for length in lengths])
                colors = [cmap(value/max_length) for value in lengths]
                v.draw_nodes_vector(pts, vectors, colors)

        if 'interface_forces' in kwargs:
            for step in steps:
                step_results = self.get_step_results(step)
                pts = []
                vectors = []
                lengths = []
                for interface in step_results.model.interfaces:
                    for int_side in ['master', 'slave']:
                        pt, vector = step_results.get_resultant_force_at_interface(interface, side=int_side)
                        # for node, vector in node_force_dict.items():
                        #     vector.scale(kwargs['interface_forces'])
                        vector.scale(kwargs['interface_forces'])
                        vectors.append(vector)
                        lengths.append(vector.length)
                        pts.append(pt)
                max_length = max([abs(length) for length in lengths])
                colors = [cmap(value/max_length) for value in lengths]
                v.draw_nodes_vector(pts, vectors, colors)

        v.show()
