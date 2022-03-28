from compas_fea2.base import FEAData
from compas_fea2.model.parts import Part
from compas_fea2.model.nodes import Node
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import ElementsGroup

from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput

from compas_fea2.problem.loads import Load
from compas_fea2.problem.loads import GravityLoad
from compas_fea2.problem.loads import PointLoad

from compas_fea2.problem.displacements import GeneralDisplacement


# ==============================================================================
#                                Base Steps
# ==============================================================================

class Step(FEAData):
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
        super(Step, self).__init__(name=name, **kwargs)
        self._field_outputs = None
        self._history_outputs = None

    @property
    def field_outputs(self):
        return self._field_outputs

    @property
    def history_outputs(self):
        return self._history_outputs

    # def add_output(self, output):
    #     if not isinstance()

# NOTE: this is not really a step, but rather a type of anlysis


class ModalStep(Step):
    """Initialises ModalStep object for use in a modal analysis.

    Note
    ----
    Modal steps can be only used as Linear Perturbation steps. Check
    :class:`LinearFrequencyStep`

    Parameters
    ----------
    name : str
        Name of the ModalStep.
    modes : int
        Number of modes to analyse.
    """

    def __init__(self, name=None, modes=1, **kwargs):
        super(ModalStep, self).__init__(name=name, **kwargs)
        self._modes = modes

    @property
    def modes(self):
        return self._modes


# ==============================================================================
#                                General Steps
# ==============================================================================
class GeneralStep(Step):
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
        super(GeneralStep, self).__init__(name=name, **kwargs)

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
        # type: (Load, Node) -> Load
        """Add a load to Step object.

        Warning
        -------
        The *load* and the *keys* must be consistent (you should not assing a
        line load to a node). Consider using specific methods to assign load,
        such as ``add_point_load``, ``add_line_load``, etc.

        Parameters
        ----------
        load : obj
            any ``compas_fea2`` :class:`compas_fea2.problem.Load` subclass object
        node : :class:`compas_fea2.model.Node`
            Node where the load is applied

        Returns
        -------
        None
        """

        if not isinstance(load, Load):
            raise TypeError('{!r} is not a Load.'.format(load))

        if not isinstance(node, Node):
            raise TypeError('{!r} is not a Node.'.format(node))
        # self.model.contains_node(node) #TODO implement method
        node._loads.add(load)
        self._loads.setdefault(node.part, {}).setdefault(load, set()).add(node)
        return load

    def add_loads(self, load, nodes):
        return [self.add_load(load, node) for node in nodes]


class StaticStep(GeneralStep):
    """GeneralStaticStep object for use in a static analysis.

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
    gravity : :class:`compas_fea2.problem.GravityLoad`
        Gravity load to assing to the whole model.
    displacements : dict
        Dictionary of the displacements assigned to each part in the model in the step.
    """

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(StaticStep, self).__init__(max_increments=max_increments,
                                         initial_inc_size=initial_inc_size, min_inc_size=min_inc_size,
                                         time=time, nlgeom=nlgeom, modify=modify, name=name, **kwargs)
        self._displacements = {}
        self._gravity = None

    @property
    def gravity(self):
        return self._gravity

    @property
    def displacements(self):
        return self._displacements

    def add_point_load(self, node, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        """Add a :class:`compas_fea2.problem.PointLoad` subclass object to the ``Step``.

        Warning
        -------
        local axes are not supported yet

        Parameters
        ----------
        name : str
            name of the point load
        part : str
            name of the :class:`compas_fea2.problem.Part` where the load is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a NodesGroup of the nodes where the load is
            applied.
        x : float, optional
            x component (in global coordinates) of the point load, by default None
        y : float, optional
            y component (in global coordinates) of the point load, by default None
        z : float, optional
            z component (in global coordinates) of the point load, by default None
        xx : float, optional
            moment about the global x axis of the point load, by default None
        yy : float, optional
            moment about the global y axis of the point load, by default None
        zz : float, optional
            moment about the global z axis of the point load, by default None
        axes : str, optional
            'local' or 'global' axes, by default 'global'
        """
        if axes != 'global':
            raise NotImplementedError('local axes are not supported yet')
        return self.add_load(PointLoad(x, y, z, xx, yy, zz, axes), node)

    def add_gravity_load(self, g=9.81, x=0., y=0., z=-1.):
        """Add a :class:`compas_fea2.problem.GravityLoad` load to the ``Step``

        Warning
        -------
        Be careful to assign a value of *g* consistent with the units in your
        model!

        Parameters
        ----------
        g : float, optional
            acceleration of gravity, by default 9.81
        x : float, optional
            x component of the gravity direction vector (in global coordinates), by default 0.
        y : [type], optional
            y component of the gravity direction vector (in global coordinates), by default 0.
        z : [type], optional
            z component of the gravity direction vector (in global coordinates), by default -1.
        """
        self._gravity = GravityLoad(g, x, y, z)

    def add_prestress_load(self):
        raise NotImplementedError

    def add_line_load(self):
        raise NotImplementedError

    def add_area_load(self):
        raise NotImplementedError

    def add_tributary_load(self):
        raise NotImplementedError

    # =========================================================================
    #                       Displacement methods
    # =========================================================================

    def add_displacement(self, displacement, node):
        """Add a displacement to Step object.

        Parameters
        ----------
        displacement : obj
            ``compas_fea2`` :class:`compas_fea2.problem.GeneralDisplacement` object.
        where : int
            node or element key where the load is applied
        part : str
            name of the part where the load is applied
        Returns
        -------
        None
        """
        if not isinstance(displacement, GeneralDisplacement):
            raise TypeError('{!r} is not a General Displacement.'.format(displacement))

        if not isinstance(node, Node):
            raise TypeError('{!r} is not a Node.'.format(node))
        # self.model.contains_node(node) #TODO implement method
        node._displacements.add(displacement)
        self._displacements.setdefault(node.part, {}).setdefault(displacement, set()).add(node)
        return displacement

    def add_displacements(self, displacement, nodes):
        return [self.add_displacement(displacement, node) for node in nodes]


class DynamicStep(GeneralStep):
    def add_harmonic_point_load(self):
        raise NotImplementedError

    def add_harmonic_preassure_load(self):
        raise NotImplementedError


class AcousticStep(GeneralStep):
    def add_acoustic_diffuse_field_load(self):
        raise NotImplementedError
