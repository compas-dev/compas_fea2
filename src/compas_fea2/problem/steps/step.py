from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

from compas_fea2.model.nodes import Node

from compas_fea2.problem.loads import _Load
from compas_fea2.problem.loads import GravityLoad
from compas_fea2.problem.loads import PointLoad

from compas_fea2.problem.displacements import GeneralDisplacement

from compas_fea2.problem.outputs import _Output
from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput

# ==============================================================================
#                                Base Steps
# ==============================================================================


class _Step(FEAData):
    """Initialises base Step object.

    Note
    ----
    A ``compas_fea2`` analysis is based on the concept of ``steps``,
    which represent the sequence of modification of the state of the model. Steps
    can be introduced for example to change the output requests or to change loads,
    boundary conditions, analysis procedure, etc. There is no limit on the number
    of steps in an analysis.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    field_outputs: :class:`compas_fea2.problem.FieldOutput'
        field outuputs requested for the step.
    history_outputs: :class:`compas_fea2.problem.HistoryOutput'
        history outuputs requested for the step.

    """

    def __init__(self, name=None, **kwargs):
        super(_Step, self).__init__(name=name, **kwargs)
        self._field_outputs = set()
        self._history_outputs = set()

    @property
    def field_outputs(self):
        return self._field_outputs

    @property
    def history_outputs(self):
        return self._history_outputs

    def add_output(self, output):
        if isinstance(output, FieldOutput):
            self._field_outputs.add(output)
        elif isinstance(output, HistoryOutput):
            self._history_outputs.add(output)
        else:
            raise TypeError('{!r} is not a Load.'.format(output))
        return output

# ==============================================================================
#                                General Steps
# ==============================================================================


class _GeneralStep(_Step):
    """General Step object for use in a general static, dynamic or
    multiphysics analysis.

    Parameters
    ----------
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        if ``True`` nonlinear geometry effects are considered.
    modify : bool
        if ``True`` the loads applied in a previous step are substituted by the
        ones defined in the present step, otherwise the loads are added.
    loads : dict
        Dictionary of the loads assigned to each part in the model in the step.
    """

    def __init__(self, max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name=None, **kwargs):
        super(_GeneralStep, self).__init__(name=name, **kwargs)

        self._max_increments = max_increments
        self._initial_inc_size = initial_inc_size
        self._min_inc_size = min_inc_size
        self._time = time
        self._nlgeom = 'YES' if nlgeom else 'NO'  # FIXME change to bool
        self._modify = modify

        self._loads = {}

    @property
    def loads(self):
        return self._loads

    @property
    def max_increments(self):
        return self._max_increments

    @property
    def initial_inc_size(self):
        return self._initial_inc_size

    @property
    def min_inc_size(self):
        return self._min_inc_size

    @property
    def time(self):
        return self._time

    @property
    def nlgeometry(self):
        return self.nlgeom

    @property
    def modify(self):
        return self._modify

    # =========================================================================
    #                           Loads methods
    # =========================================================================

    def add_load(self, load, node):
        # type: (_Load, Node) -> _Load
        """Add a load to Step object.

        Warning
        -------
        The *load* and the *keys* must be consistent (you should not assing a
        line load to a node). Consider using specific methods to assign load,
        such as ``add_point_load``, ``add_line_load``, etc.

        Parameters
        ----------
        load : obj
            any ``compas_fea2`` :class:`compas_fea2.problem._Load` subclass object
        node : :class:`compas_fea2.model.Node`
            Node where the load is applied

        Returns
        -------
        None
        """

        if not isinstance(load, _Load):
            raise TypeError('{!r} is not a Load.'.format(load))

        if not isinstance(node, Node):
            raise TypeError('{!r} is not a Node.'.format(node))
        # self.model.contains_node(node) #TODO implement method
        node._loads.add(load)
        self._loads.setdefault(node.part, {}).setdefault(load, set()).add(node)
        return load

    def add_loads(self, load, nodes):
        return [self.add_load(load, node) for node in nodes]


class AcousticStep(_GeneralStep):
    def __init__(self, max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name=None, **kwargs):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name, **kwargs)
        raise NotImplementedError()

    def add_acoustic_diffuse_field_load(self):
        raise NotImplementedError
