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
from compas_fea2.results.results import StepResults

from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import step_method

from compas_fea2.results.sql_wrapper import (create_connection,
                                             get_database_table,
                                             get_query_results,
                                             get_field_results,
                                             get_field_labels)

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
        """check if the analysis path is correct

        Parameters
        ----------
        path : :class:`pathlib.Path`
            Path where the input file will be saved.

        Return
        :class:`pathlib.Path`
            Path where the input file will be saved.
        """
        if path:
            if not isinstance(path, Path):
                path = Path(path)
            self.path = path.joinpath(self.name)
        if not self.path:
            raise AttributeError('You must provide a path')
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

        Raises
        ------
        ValueError
            _description_
        TypeError
            _description_
        ValueError
            _description_
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
    #                         Results methods
    # =========================================================================
    def connect_db(self, path_db=None):
        # typing: (str) -> str
        """Create a connection to the SWLite database.

        Parameters
        ----------
        path_db : path, optional
            path to the SQLite database, by default None

        Returns
        -------
        :class:`sqlite3.Engine` | :class:`sqlite3.Connection` | :class:`sqlite3.Metadata`
            engine, connection, metadata
        """
        from compas_fea2.results.sql_wrapper import create_connection

        self._db_connection = create_connection(path_db or self.path_db)
        return self._db_connection

    def convert_results_to_sqlite(self, *args, **kwargs):
        """Convert the backend native results database into a sqlite database.

        Raises
        ------
        NotImplementedError
            This method is implemented only at the backend level.
        """
        raise NotImplementedError("this function is not available for the selected backend")

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

    def _get_field_results(self, field, step, db_path=None):
        """_summary_

        Parameters
        ----------
        field : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        engine, connection, metadata = self.db_connection or self.connect_db(db_path)
        TABLE = get_database_table(engine, metadata, field)
        test = [TABLE.columns.step == step.name, TABLE.columns.magnitude != 0.]
        return get_field_results(engine, connection, metadata, TABLE, test)

    def _get_vector_results(self, ResultSet):
        """_summary_

        Parameters
        ----------
        ResultSet : _type_
            _description_

        Returns
        -------
        dict, class:`compas.geoemtry.Vector`
            Dictionary with {'part':..; 'node':..; 'vector':...} and resultant vector
        """
        col_names = ResultSet[0]
        values = ResultSet[1]
        results=[]
        for row in values:
            result={}
            part = self.model.find_part_by_name(row[0])
            if not part:
                # try case insensitive match
                part = self.model.find_part_by_name(row[0], casefold=True)
            if not part:
                print('Part {} not found in model'.format(row[0]))
                continue
            result['part']= part
            result['node'] = part.find_node_by_key(row[2])
            result['vector'] = Vector(*[row[i] for i in range(3,6)])
            results.append(result)
        return results, Vector(*sum_vectors([r['vector'] for r in results]))

    def get_reaction_forces_sql(self, step=None):
        """Retrieve the reaction forces for a given step.

        Parameters
        ----------
        step : _type_
            _description_

        Returns
        -------
        _type_
            _description_
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
        _type_
            _description_
        """
        if not step:
            step = self._steps_order[-1]
        _, col_val = self._get_field_results('RM', step)
        return self._get_vector_results(col_val)


    def _get_func_field_sql(self, func, field, steps=None, group_by=None, component='magnitude'):
        """
        """
        if not steps:
            steps = [self._steps_order[-1]]
        engine, connection, metadata = self.db_connection or self.connect_db()
        components = get_field_labels(engine, connection, metadata, field, 'components')
        invariants = get_field_labels(engine, connection, metadata, field, 'invariants')
        labels = ['part', 'position', 'key']+components+invariants
        labels[labels.index(component)] = '{}({})'.format(func, component)
        sql = """SELECT {}
FROM {}
WHERE step IN ({})
GROUP BY {};""".format(', '.join(labels), field,
                       ', '.join(["'{}'".format(step.name) for step in steps]),
                       group_by)
        ResultProxy = connection.execute(sql)
        ResultSet = ResultProxy.fetchall()
        disp, _ = self._get_vector_results((labels, ResultSet))
        return disp

    def get_displacements_sql(self, step=None):
        """Retrieve all nodal dispacements from the SQLite database.
        Parameters
        ----------
        step : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if not step:
            step = self._steps_order[-1]
        _, col_val = self._get_field_results('U', step)
        return self._get_vector_results(col_val)

    def get_max_displacement_sql(self, component='U3', steps=None, group_by='step'):
        """_summary_

        Parameters
        ----------
        component : str, optional
            _description_, by default 'U3'
        steps : _type_, optional
            _description_, by default None
        group_by : str, optional
            _description_, by default 'step'

        Returns
        -------
        _type_
            _description_
        """
        return self._get_func_field_sql(func='MAX', field='U', steps=steps, group_by=group_by, component=component)[0]

    def get_min_displacement_sql(self, component='U3', steps=None, group_by='step'):
        """_summary_

        Parameters
        ----------
        component : str, optional
            _description_, by default 'U3'
        steps : _type_, optional
            _description_, by default None
        group_by : str, optional
            _description_, by default 'step'

        Returns
        -------
        _type_
            _description_
        """
        return self._get_func_field_sql(func='MIN', field='U', steps=steps, group_by=group_by, component=component)[0]

    def get_displacement_at_nodes_sql(self, nodes, steps=None, group_by=['step', 'part']):
        """_summary_

        Parameters
        ----------
        node : _type_
            _description_
        steps : _type_, optional
            _description_, by default None
        """
        if not isinstance(nodes, Iterable):
            nodes = [nodes]
        if not steps:
            steps = [self._steps_order[-1]]
        field = 'U'
        group_by = 'step'
        engine, connection, metadata = self.db_connection or self.connect_db()
        components = get_field_labels(engine, connection, metadata, field, 'components')
        invariants = get_field_labels(engine, connection, metadata, field, 'invariants')
        labels = ['part', 'position', 'key']+components+invariants

        sql = """SELECT {}
FROM {}
WHERE step IN ({}) AND key  in ({})
GROUP BY {};""".format(', '.join(labels),
                       field,
                       ', '.join(["'{}'".format(step.name) for step in steps]),
                       ', '.join(["'{}'".format(node.key) for node in nodes]),
                       group_by)
        ResultProxy = connection.execute(sql)
        ResultSet = ResultProxy.fetchall()
        disp, _ = self._get_vector_results((labels,ResultSet))
        return disp

    def get_displacement_at_point(self, point, distance, plane=None, steps=None, group_by=['step', 'part']):
        if not steps:
            steps = [self._steps_order[-1]]
        node = self.model.find_node_by_location(point, distance, plane=None)
        return self.get_displacement_at_nodes(nodes=[node], steps=steps,group_by=group_by)

    def show_displacements(self, component=3, step=None, style='contour', deformed=False, width=1600, height=900, scale_factor=1., **kwargs):
        """_summary_

        Parameters
        ----------
        component : int, optional
            _description_, by default 3
        step : _type_, optional
            _description_, by default None
        style : str, optional
            _description_, by default 'contour'
        deformed : bool, optional
            _description_, by default False
        width : int, optional
            _description_, by default 1600
        height : int, optional
            _description_, by default 900
        scale_factor : _type_, optional
            _description_, by default 1.

        Raises
        ------
        ValueError
            _description_
        """
        from compas_fea2.UI.viewer import FEA2Viewer
        from compas.geometry import Point, Vector

        from compas.colors import ColorMap, Color
        cmap = ColorMap.from_palette('hawaii') #ColorMap.from_color(Color.red(), rangetype='light') #ColorMap.from_mpl('viridis')
        v = FEA2Viewer(width, height)

        if component not in [1,2,3, 'magnitude']:
            raise ValueError('The component can be either 1, 2, 3 or magnitude')
        c_symb = 'U'+str(component)
        c_index = component-1

        displacements, _ = self.get_displacements_sql(step)
        max_disp = self.get_max_displacement_sql(component=c_symb)
        min_disp = self.get_min_displacement_sql(component=c_symb)

        parts_gkey_vertex={}
        parts_mesh={}
        if style == 'contour':
            for part in self.model.parts:
                if (mesh:= part.discretized_boundary_mesh):
                    colored_mesh = mesh.copy()
                    parts_gkey_vertex[part.name] = colored_mesh.gkey_key(compas_fea2.PRECISION)
                    parts_mesh[part.name] = colored_mesh

        pts = []
        vectors = []
        colors = []

        for displacement in displacements:
            part = displacement['part']
            node = displacement['node']
            vector = displacement['vector']
            if kwargs.get('bound', None):
                if vector[c_index]>= max_disp['vector'][c_index]*kwargs['bound'] or vector[c_index] <= min_disp['vector'][c_index]*kwargs['bound']:
                    color = Color.red()
                else:
                    color = cmap(vector[c_index], minval=min_disp['vector'][c_index], maxval=max_disp['vector'][c_index])
            else:
                color = cmap(vector[c_index], minval=min_disp['vector'][c_index], maxval=max_disp['vector'][c_index])

            pts.append(node.point)
            vectors.append(vector)
            colors.append(color)

            if part.discretized_boundary_mesh:
                if style=='contour':
                    if node.gkey in parts_gkey_vertex[part.name]:
                        parts_mesh[part.name].vertex_attribute(parts_gkey_vertex[part.name][node.gkey], 'color', color)

        for part in self.model.parts:
            if part.discretized_boundary_mesh:
                if style=='contour':
                    v.draw_mesh(parts_mesh[part.name])
                else:
                    v.draw_mesh(part.discretized_boundary_mesh)

        if style=='vector':
            v.draw_nodes_vector(pts, vectors, colors)

        if kwargs.get('draw_bcs', None):
            v.draw_bcs(self.model, parts, draw_bcs)

        if kwargs.get('draw_loads', None):
            v.draw_loads(step, kwargs['draw_loads'])

        v.show()


    def show_deformed(self, step=None, width=1600, height=900, scale_factor=1.):
        from compas_fea2.UI.viewer import FEA2Viewer
        from compas.geometry import Point, Vector

        from compas.colors import ColorMap, Color
        cmap = ColorMap.from_mpl('viridis')
        v = FEA2Viewer(width, height)


        # TODO create a copy of the model first
        displacements, _ = self.get_displacements_sql(step)
        for displacement in displacements:
            vector = displacement['vector']
            vector.scale(scale_factor)
            displacement['node'].xyz = sum_vectors([Vector(*displacement['node'].xyz), vector])
        v.draw_parts(self.model.parts, solid=True)
        v.show()
