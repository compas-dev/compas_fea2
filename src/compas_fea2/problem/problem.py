from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
import compas_fea2
from pathlib import Path
import os
from typing import Iterable
from unittest import result

from compas_fea2.base import FEAData
from compas_fea2.problem.steps.step import _Step
from compas_fea2.job.input_file import InputFile

from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import step_method

from compas_fea2.results import NodeFieldResults


from compas.geometry import Point, Plane
from compas.geometry import Vector
from compas.geometry import sum_vectors


class Problem(FEAData):
    """A Problem is a collection of analysis steps (:class:`compas_fea2.problem._Step)
    applied in a specific sequence.

    Note
    ----
    Problems are registered to a :class:`compas_fea2.model.Model`.

    Problems can also be used as canonical `load combinations`, where each `load`
    is actually a `factored step`. For example, a typical load combination such
    as 1.35*DL+1.50LL can be applied to the model by creating the Steps DL and LL,
    factoring them (see :class:`compas_fea2.problem._Step documentation) and adding
    them to Problme

    Note
    ----
    While for linear models the sequence of the steps is irrelevant, it is not the
    case for non-linear models.

    Warning
    -------
    Factore Steps are new objects! check the :class:`compas_fea2.problem._Step
    documentation.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
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

    def __init__(self, name=None, description=None, **kwargs):
        super(Problem, self).__init__(name=name, **kwargs)
        self.description = description
        self._path = None
        self._path_db = None
        self._db_connection = None
        self._steps = set()
        self._steps_order = []  # TODO make steps a list

    @property
    def model(self):
        return self._registration

    @property
    def steps(self):
        return self._steps

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value if isinstance(value, Path) else Path(value)
        self._path_db = os.path.join(self._path, '{}-results.db'.format(self.name))

    @property
    def db_connection(self):
        return self._db_connection

    @property
    def path_db(self):
        return self._path_db

    @property
    def steps_order(self):
        return self._steps_order
    @steps_order.setter
    def steps_order(self, value):
        for step in value:
            if not self.is_step_in_problem(step, add=False):
                raise ValueError('{!r} must be previously added to {!r}'.format(step, self))
        self._steps_order = value


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

    def add_step(self, step):
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
        if not isinstance(step, _Step):
            raise TypeError('You must provide a valid compas_fea2 Step object')

        if self.find_step_by_name(step):
            raise ValueError('There is already a step with the same name in the model.')

        step._key = len(self._steps)
        self._steps.add(step)
        step._registration = self
        self._steps_order.append(step)
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

    # def define_steps_order(self, order):
    #     """Defines the order in which the steps are applied during the analysis.

    #     Parameters
    #     ----------
    #     order : list
    #         List contaning the names of the analysis steps in the order in which
    #         they are meant to be applied during the analysis.

    #     Returns
    #     -------
    #     None

    #     Warning
    #     -------
    #     Not implemented yet!
    #     """
    #     for step in order:
    #         if not isinstance(step, _Step):
    #             raise TypeError('{} is not a step'.format(step))
    #     self._steps_order = order

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
        # type: () -> str
        """Prints a summary of the Problem object.

        Parameters
        ----------
        None

        Returns
        -------
        str
            Problem summary
        """
        steps_data = '\n'.join([f'{step.name}' for step in self.steps])

        summary = """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Problem: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

description: {}

Steps (in order of application)
-------------------------------
{}

Analysis folder path : {}

""".format(self._name,
           self.description or 'N/A',
           steps_data,
           self.path  or 'N/A')
        print(summary)
        return summary

    # =========================================================================
    #                         Analysis methods
    # =========================================================================
    @timer(message='Finished writing input file in')
    def write_input_file(self, path=None):
        # type: (Path |str) -> None
        """Writes the input file.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path to the folder where the input file is saved. In case the folder
            does not exist, one is created.

        Returns
        -------
        :class:`compas_fea2.job.InputFile`
            The InputFile objects that generates the input file.
        """
        path = path or self.path
        if not path.exists():
            path.mkdir(parents=True)
        input_file = InputFile.from_problem(self)
        input_file.write_to_file(path)
        return input_file

    def _check_analysis_path(self, path):
        """Check the analysis path and adds the correct folder structure.

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path where the input file will be saved.

        Return
        :class:`pathlib.Path`
            Path where the input file will be saved.
        """
        if path:
            self.model.path = path
            self.path = self.model.path.joinpath(self.name)
        if not self.path and not self.model.path:
            raise AttributeError('You must provide a path for storing the model and the analysis results.')
        return self.path

    def analyse(self, path=None, *args, **kwargs):
        """Analyse the problem in the selected backend.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.
        """
        raise NotImplementedError("this function is not available for the selected backend")

    def analyze(self, *args, **kwargs):
        """American spelling of the analyse method \n"""
        __doc__ += self.analyse.__doc__
        self.analyse(*args, **kwargs)

    def analyse_and_extract(self, path=None, *args, **kwargs):
        """Analyse the problem in the selected backend and extract the results
        from the native database system to SQLite.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.
        """
        raise NotImplementedError("this function is not available for the selected backend")

    #FIXME check the funciton and 'memory only parameter
    def analyse_and_store(self, memory_only=False, *args, **kwargs):
        """Analyse the problem in the selected backend and stores the results in
        the model.

        Note
        ----
        The extraction of the results to SQLite ca be done `in memory` to speed up
        the process but no database file is generated.

        Parameters
        ----------
        problems : [:class:`compas_fea2.problem.Problem`], optional
            List of problems to store, by default None and all the problems of
            the model are stored.
        memory_only : bool, optional
            store the SQLITE database only in memory (no .db file will be saved),
            by default False
        """
        self.analyse(*args, **kwargs)
        self.convert_results_to_sqlite(*args, **kwargs)
        self.store_results_in_model(*args, **kwargs)

    def restart_analysis(self, *args, **kwargs):
        """Continue a previous analysis from a given increement with additional
        steps.

        Note
        ----
        For abaqus, you have to specify to save specific files during the original
        analysis by passing the `restart=True` option.

        Parameters
        ----------
        problem : :class:`compas_fea2.problme.Problem`
            The problem (already analysed) to continue.
        start : float
            Time-step increment.
        steps : [:class:`compas_fea2.problem.Step`]
            List of steps to add to the orignal problem.

        Raises
        ------
        ValueError
            _description_
        """
        raise NotImplementedError("this function is not available for the selected backend")

    # =========================================================================
    #                         Results methods - general
    # =========================================================================


    @timer(message='Problem results copied in the model in ')
    def store_results_in_model(self, database_path=None, database_name=None, steps=None, fields=None, *args, **kwargs):
        """Copy the results form the sqlite database back into the model at the
        nodal and element level.

        Parameters
        ----------
        database_path : str
            path to the folder
        database_name : str
            name of the database
        file_format : str, optional
            serialization type ('pkl' or 'json'), by default 'pkl'
        steps : :class:`compas_fea2.problem._Step`, optional
            The steps fro which copy the results, by default `None` (all the steps are saved)
        fields : _type_, optional
            Fields results to save, by default `None` (all available fields are saved)

        Returns
        -------
        None

        """
        databse_full_path = os.path.join(database_path, database_name) if database_path and database_name else self.path_results
        if not os.path.exists(databse_full_path):
            self.convert_results_to_sqlite(*args, **kwargs)
        for step in steps or self.steps:
            step._store_results_in_model(databse_full_path, fields)

    # =========================================================================
    #                         Results methods - reactions
    # =========================================================================

    def get_reaction_forces_sql(self, step=None):
        """Retrieve the reaction forces for a given step.

        Parameters
        ----------
        step : _type_
            _description_

        Returns
        -------
        dict, class:`compas.geoemtry.Vector`
            Dictionary with {'part':..; 'node':..; 'vector':...} and resultant vector
        """
        if not step:
            step = self._steps_order[-1]
        _, col_val = self._get_field_results('RF', step)
        return self._get_vector_results(col_val)

    def get_reaction_moments_sql(self, step=None):
        """_summary_

        Parameters
        ----------
        step : _type_
            _description_

        Returns
        -------
        dict, class:`compas.geoemtry.Vector`
            Dictionary with {'part':..; 'node':..; 'vector':...} and resultant vector
        """
        if not step:
            step = self._steps_order[-1]
        _, col_val = self._get_field_results('RM', step)
        return self._get_vector_results(col_val)

    # =========================================================================
    #                         Results methods - displacements
    # =========================================================================

   # TODO add moments
    def get_total_reaction(self):
        reactions_forces = []
        for part in self.step.problem.model.parts:
            for node in part.nodes:
                rf = node.results[[self.problem]][self.step].get("RF", None)
                if rf:
                    x, y, z = rf
                    vector = Vector(x=x, y=y, z=z)
                    if vector.length == 0:
                        continue
                    reactions_forces.append(vector)
        return sum_vectors(reactions_forces)

    def get_total_moment(self):
        raise NotImplementedError()

    def get_deformed_model(self, step=None, **kwargs):
        from copy import deepcopy
        if not step:
            step=self.steps_order[-1]

        deformed_model = deepcopy(self.model)
        # # # TODO create a copy of the model first
        # displacements = NodeFieldResults('U', step)
        # for displacement in displacements.results:
        #     vector = displacement.vector.scaled(scale_factor)
        #     node = deformed_model.find_node_by_key
        #     displacement.location.xyz = sum_vectors([Vector(*displacement.location.xyz), vector])
        raise NotImplementedError()
        return deformed_model


    # =========================================================================
    #                         Viewer methods
    # =========================================================================
    # def show(self, scale_factor=1., step=None, width=1600, height=900, parts=None,
    #          solid=True, draw_nodes=False, node_labels=False,
    #          draw_bcs=1., draw_constraints=True, draw_loads=True, **kwargs):

    #     from compas_fea2.UI.viewer import FEA2Viewer
    #     from compas.colors import ColorMap, Color
    #     cmap = kwargs.get('cmap', ColorMap.from_palette('hawaii'))
    #     #ColorMap.from_color(Color.red(), rangetype='light') #ColorMap.from_mpl('viridis')

    #     # Get values
    #     if not step:
    #         step = self._steps_order[-1]

    #     # # Color the mesh
    #     # pts, vectors, colors = [], [], []
    #     # for r in field.results:
    #     #     if r.vector.length == 0:
    #     #         continue
    #     #     vectors.append(r.vector.scaled(scale_factor))
    #     #     pts.append(r.location.xyz)
    #     #     colors.append(cmap(r.invariants['magnitude'], minval=min_value, maxval=max_value))

    #     # Display results
    #     v = FEA2Viewer(width, height, scale_factor=scale_factor)
    #     # v.draw_nodes_vector(pts=pts, vectors=vectors, colors=colors)
    #     parts = parts or self.model.parts
    #     if draw_bcs:
    #         v.draw_bcs(self.model, parts, draw_bcs)

    #     v.draw_parts(parts,
    #                  draw_nodes,
    #                  node_labels,
    #                  solid)

    #     if kwargs.get('draw_loads', None):
    #         v.draw_loads(step, scale_factor=kwargs['draw_loads'])
    #     v.show()

    def show_nodes_field_vector(self, field_name, vector_sf=1., model_sf=1., step=None, width=1600, height=900, **kwargs):
        from compas_fea2.UI.viewer import FEA2Viewer
        from compas.colors import ColorMap, Color
        cmap = kwargs.get('cmap', ColorMap.from_palette('hawaii'))
        #ColorMap.from_color(Color.red(), rangetype='light') #ColorMap.from_mpl('viridis')

        # Get values
        if not step:
            step = self._steps_order[-1]
        field = NodeFieldResults(field_name, step)
        min_value = field._min_invariants['magnitude'].invariants["MIN(magnitude)"]
        max_value = field._max_invariants['magnitude'].invariants["MAX(magnitude)"]

        # Color the mesh
        pts, vectors, colors = [], [], []
        for r in field.results:
            if r.vector.length == 0:
                continue
            vectors.append(r.vector.scaled(vector_sf))
            pts.append(r.location.xyz)
            colors.append(cmap(r.invariants['magnitude'], minval=min_value, maxval=max_value))

        # Display results
        v = FEA2Viewer(width, height, scale_factor=model_sf)
        v.draw_nodes_vector(pts=pts, vectors=vectors, colors=colors)
        v.draw_parts(self.model.parts)
        if kwargs.get('draw_bcs', None):
            v.draw_bcs(self.model, scale_factor=kwargs['draw_bcs'])
        if kwargs.get('draw_loads', None):
            v.draw_loads(step, scale_factor=kwargs['draw_loads'])
        v.show()

    def show_nodes_field(self, field_name, component, step=None, width=1600, height=900, model_sf=1., **kwargs):
        """Display a contour plot of a given field and component. The field must
        de defined at the nodes of the model (e.g displacement field).

        Parameters
        ----------
        field : str
            The field to display, e.g. 'U' for displacements.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        component : str
            The compoenet of the field to display, e.g. 'U3' for displacements
            along the 3 axis.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        step : :class:`compas_fea2.problem.Step`, optional
            The step to show the results of, by default None.
            if not provided, the last step of the analysis is used.
        deformed : bool, optional
            Choose if to display on the deformed configuration or not, by default False
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Options
        -------
        draw_loads : float
            Displays the loads at the step scaled by the given value
        draw_bcs : float
            Displays the bcs of the model scaled by the given value
        bound : float
            limit the results to the given value

        Raises
        ------
        ValueError
            _description_
        """
        from compas_fea2.UI.viewer import FEA2Viewer
        from compas.colors import ColorMap, Color
        cmap = kwargs.get('cmap', ColorMap.from_palette('hawaii'))
        #ColorMap.from_color(Color.red(), rangetype='light') #ColorMap.from_mpl('viridis')

        # Get mesh
        parts_gkey_vertex={}
        parts_mesh={}
        for part in self.model.parts:
            if (mesh:= part.discretized_boundary_mesh):
                colored_mesh = mesh.copy()
                parts_gkey_vertex[part.name] = colored_mesh.gkey_key(compas_fea2.PRECISION)
                parts_mesh[part.name] = colored_mesh
            else:
                raise AttributeError('Discretized boundary mesh not found')

        # Set the bounding limits
        if kwargs.get('bound', None):
            if not isinstance(kwargs['bound'], Iterable) or len(kwargs['bound'])!=2:
                raise ValueError('You need to provide an upper and lower bound -> (lb, up)')
            if kwargs['bound'][0]>kwargs['bound'][1]:
                kwargs['bound'][0], kwargs['bound'][1] = kwargs['bound'][1], kwargs['bound'][0]

        # Get values
        if not step:
            step = self._steps_order[-1]
        field = NodeFieldResults(field_name, step)
        min_value = field._min_components[component].components[f'MIN({component})']
        max_value = field._max_components[component].components[f'MAX({component})']

        # Color the mesh
        for r in field.results:
            if min_value - max_value == 0.:
                color = Color.red()
            elif kwargs.get('bound', None):
                if r.components[component]>=kwargs['bound'] or r.components[component]<=kwargs['bound']:
                    color = Color.red()
                else:
                    color = cmap(r.components[component], minval=min_value, maxval=max_value)
            else:
                color = cmap(r.components[component], minval=min_value, maxval=max_value)
            if r.location.gkey in parts_gkey_vertex[part.name]:
                parts_mesh[part.name].vertex_attribute(parts_gkey_vertex[part.name][r.location.gkey], 'color', color)

        # Display results
        v = FEA2Viewer(width, height, scale_factor=model_sf)
        for part in self.model.parts:
            v.draw_mesh(parts_mesh[part.name])

        if kwargs.get('draw_bcs', None):
            v.draw_bcs(self.model, scale_factor=kwargs['draw_bcs'])

        if kwargs.get('draw_loads', None):
            v.draw_loads(step, scale_factor=kwargs['draw_loads'])

        v.show()

    def show_displacements(self, component=3, step=None, style='contour', deformed=False, width=1600, height=900, model_sf=1., **kwargs):
        """Display the displacement of the nodes.

        Parameters
        ----------
        component : int, optional
            The component to display, by default 3.
            Choose among [1, 2, 3, 'magnitude']
        step : :class:`compas_fea2.problem.Step`, optional
            The step to show the results of, by default None.
            if not provided, the last step of the analysis is used.
        style : str, optional
            The style of the results, by default 'contour'.
            You can choose between ['contour', 'vector'].
        deformed : bool, optional
            Choose if to display on the deformed configuration or not, by default False
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Options
        -------
        draw_loads : float
            Displays the loads at the step scaled by the given value
        draw_bcs : float
            Displays the bcs of the model scaled by the given value
        bound : float
            limit the results to the given value

        Raises
        ------
        ValueError
            "The style can be either 'vector' or 'contour'"
        """
        if style == 'contour':
            self.show_nodes_field(field_name='U', component='U'+str(component), step=step, width=width, height=height, model_sf=model_sf, **kwargs)
        elif style == 'vector':
            raise NotImplementedError('WIP')
        else:
            raise ValueError("The style can be either 'vector' or 'contour'")

    def show_deformed(self, step=None, width=1600, height=900, scale_factor=1., **kwargs):
        """Display the structure in its deformed configuration.

        Parameters
        ----------
        step : :class:`compas_fea2.problem._Step`, optional
            The Step of the analysis, by default None. If not provided, the last
            step is used.
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Return
        ------
        None
        """
        from compas_fea2.UI.viewer import FEA2Viewer
        from compas.geometry import Point, Vector

        from compas.colors import ColorMap, Color
        v = FEA2Viewer(width, height)
        if not step:
            step=self.steps_order[-1]
        # TODO create a copy of the model first
        displacements = NodeFieldResults('U', step)
        for displacement in displacements.results:
            vector = displacement.vector.scaled(scale_factor)
            displacement.location.xyz = sum_vectors([Vector(*displacement.location.xyz), vector])
        v.draw_parts(self.model.parts, solid=True)

        if kwargs.get('draw_bcs', None):
            v.draw_bcs(self.model, scale_factor=kwargs['draw_bcs'])

        if kwargs.get('draw_loads', None):
            v.draw_loads(step, scale_factor=kwargs['draw_loads'])
        v.show()
