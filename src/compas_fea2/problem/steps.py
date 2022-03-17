import importlib

from compas_fea2.base import FEAData
from compas_fea2.problem.loads import Load
from compas_fea2.problem.displacements import GeneralDisplacement
from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.model.parts import Part
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import ElementsGroup


class Step(FEAData):
    """Initialises base Step object.

    Note
    ----
    A ``compas_fea2`` analysis is based on the concept of ``steps``,
    which represent the sequence of modification of the state of the model. Steps
    can be introduced simply to change the output requests or to change the loads,
    boundary conditions, analysis procedure, etc. There is no limit on the number
    of steps in an analysis.

    Parameters
    ----------
    name : str
        Name of the Step object.
    """

    def __init__(self, name):
        super(Step, self).__init__(name)
        self.__name__ = 'Step'
        self._name = name
        self._field_outputs = {}
        self._history_outputs = {}

    @property
    def name(self):
        """str : Name of the Step object."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def field_outputs(self):
        """dict : dictionary containing the `compas_fea2` FieldOutput objects"""
        return self._field_outputs

    @property
    def history_outputs(self):
        """dict : dictionary containing the `compas_fea2` HistoryOutput objects"""
        return self._history_outputs

    # =========================================================================
    #                           Outputs methods
    # =========================================================================

    def add_output(self, output):
        """Add an output to the Step object.

        Parameters
        ----------
        output : obj
            `compas_fea2` Output objects. Can be either a :class:`FieldOutputBase`
            or a :class:`HistoryOutputBase` subclass instance.

        Returns
        -------
        None
        """
        attrb = '_field_outputs' if isinstance(output, FieldOutput) else '_history_outputs'

        if output.name not in getattr(self, attrb):
            getattr(self, attrb)[output.name] = output
        else:
            print(f'WARNING: {output.__repr__()} already present in the Problem. skipped!')

    def add_outputs(self, outputs):
        """Add multiple outputs to the Step object.

        Parameters
        ----------
        outputs : list
            list of `compas_fea2` Output objects. The list can contain both :class:`FieldOutputBase`
            or a :class:`HistoryOutputBase` subclass instances.

        Returns
        -------
        None
        """
        for output in outputs:
            self.add_output(output)


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

    def __init__(self, name, modes=1):
        super(ModalStep, self).__init__(name)

        self.__name__ = 'ModalStep'
        self._modes = modes

    @property
    def modes(self):
        """int : Number of modes to analyse."""
        return self._modes


class StaticStep(Step):
    """Initialises base StaticStep object.

    Parameters
    ----------
    name : str
        Name of the Step object.
    """

    def __init__(self, name, **kwargs):
        super(StaticStep, self).__init__(name, **kwargs)
        self.__name__ = 'StaticStep'
        self._gravity = None
        self._loads = {}
        self._displacements = {}

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    @property
    def gravity(self):
        """obj : :class:`GravityLoadBase` subclass object."""
        return self._gravity

    @property
    def loads(self):
        """dict: dictionary of the loads assigned to the ``Step``."""
        return self._loads

    @property
    def displacements(self):
        """dict: dictionary of the displacements assigned to the ``Step``."""
        return self._displacements

    # =========================================================================
    #                           Loads methods
    # =========================================================================

    def add_load(self, load, where, part):
        """Add a load to Step object.

        Warning
        -------
        The *load* and the *keys* must be consistent (you should not assing a
        line load to a node). Consider using specific methods to assign load,
        such as ``add_point_load``, ``add_line_load``, etc.

        Parameters
        ----------
        load : obj
            any ``compas_fea2`` :class:`LoadBase` subclass object
        keys : int
            node or element key where the load is applied
        part : str
            name of the part where the load is applied

        Returns
        -------
        None
        """

        # check if load is valid
        if not isinstance(load, Load):
            raise TypeError(f'{load} is not a `compas_fea2` Load object')

        if isinstance(where, int):
            nodes = [where]
        elif isinstance(where, (list, tuple)):
            nodes = where
        elif isinstance(where, (NodesGroup, ElementsGroup)):
            nodes = where.keys
        else:
            raise TypeError('You must provide either a key or a list of keys, or a Group instance')
        # self._check_nodes_in_model(nodes) #TODO implement method

        if not isinstance(load, Load):
            raise TypeError(f'{load} is not a compas_fea2 LoadBase subclass instance')
        if isinstance(part, Part):
            part = part.name
        self._loads.setdefault(part, {})[load] = nodes

    def add_loads(self, loads):
        for load in loads:
            self.add_load(load)

    def add_point_load(self, name, part, where, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        """Add a :class:`PointLoadBase` subclass object to the ``Step``.

        Warning
        -------
        local axes are not supported yet

        Parameters
        ----------
        name : str
            name of the point load
        part : str
            name of the :class:`PartBase` where the load is applied
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
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        load = m.PointLoad(name, x, y, z, xx, yy, zz, axes)
        self.add_load(load, where, part)

    def add_gravity_load(self, name='gravity', g=9.81, x=0., y=0., z=-1.):
        """Add a :class:`GravityLoadBase` load to the ``Step``

        Warning
        -------
        Be careful to assign a value of *g* consistent with the units in your
        model!

        Parameters
        ----------
        name : str, optional
            name to assign to the load, by default 'gravity'
        g : float, optional
            acceleration of gravity, by default 9.81
        x : float, optional
            x component of the gravity direction vector (in global coordinates), by default 0.
        y : [type], optional
            y component of the gravity direction vector (in global coordinates), by default 0.
        z : [type], optional
            z component of the gravity direction vector (in global coordinates), by default -1.
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        self._gravity = m.GravityLoad(name, g, x, y, z)

    def add_prestress_load(self):
        raise NotImplementedError

    def add_line_load(self):
        raise NotImplementedError

    def add_area_load(self):
        raise NotImplementedError

    def add_tributary_load(self):
        raise NotImplementedError

    def add_harmonic_point_load(self):
        raise NotImplementedError

    def add_harmonic_preassure_load(self):
        raise NotImplementedError

    def add_acoustic_diffuse_field_load(self):
        raise NotImplementedError

    # =========================================================================
    #                       Displacement methods
    # =========================================================================

    def add_displacement(self, displacement, where, part):
        """Add a displacement to Step object.

        Parameters
        ----------
        displacement : obj
            ``compas_fea2`` :class:`GeneralDisplacementBase` object.
        where : int
            node or element key where the load is applied
        part : str
            name of the part where the load is applied
        Returns
        -------
        None
        """
        # check if where is valid
        if isinstance(where, int):
            nodes = [where]
        elif isinstance(where, (list, tuple)):
            nodes = where
        elif isinstance(where, (NodesGroup, ElementsGroup)):
            nodes = where.keys
        else:
            raise TypeError('You must provide either a key or a list of keys, or a Group instance')

        # check if displacement is valid
        if not isinstance(displacement, GeneralDisplacement):
            raise ValueError(f'{displacement} is not a `compas_fea2` GeneralDisplacement object')

        # check if part is valid
        if isinstance(part, Part):
            part = part.name
        self._loads.setdefault(part, {})[displacement] = nodes


# ==============================================================================
#                                General Steps
# ==============================================================================
class GeneralStep(Step):
    """Initialises GeneralStep object for use in a general static, dynamic or
    multiphysics analysis.

        name to assign to the ``Step``
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
    """

    def __init__(self, name, max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify):
        super(GeneralStep, self).__init__(name)

        self._max_increments = max_increments
        self._initial_inc_size = initial_inc_size
        self._min_inc_size = min_inc_size
        self._time = time
        self._nlgeom = 'YES' if nlgeom else 'NO'  # FIXME change to bool
        self._modify = modify

    @property
    def max_increments(self):
        """int : Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear
        problems. This might increase the analysis time.)."""
        return self._max_increments

    @property
    def initial_inc_size(self):
        """float : Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease
        the size automatically.)"""
        return self._initial_inc_size

    @property
    def min_inc_size(self):
        """float : Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear
        problems. This might increase the analysis time.)"""
        return self._min_inc_size

    @property
    def time(self):
        """float : Total time of the case step. Note that this not actual 'time',
        but rather a proportionality factor. (By default is 1, meaning that the
        analysis is complete when all the increments sum up to 1)"""
        return self._time

    @property
    def nlgeometry(self):
        """The nlgeometry property."""
        return self.nlgeom

    @property
    def modify(self):
        """The modify property."""
        return self._modify


class GeneralStaticStep(StaticStep, GeneralStep):
    """Initialises GeneralStaticStep object for use in a static analysis.
    """

    def __init__(self, name, max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify):
        super(GeneralStaticStep, self).__init__(name=name, max_increments=max_increments,
                                                initial_inc_size=initial_inc_size, min_inc_size=min_inc_size,
                                                time=time, nlgeom=nlgeom, modify=modify)
        self.__name__ = 'GeneralStaticStep'


# ==============================================================================
#                                Linear Steps
# ==============================================================================

class LinearStep():
    """Initialises LinearStep object for use in a linear perturbation analysis.

    Note
    ----
    a linear step allows the investigation of the perturbation
    response of the system with respect to a base state at any stage during the
    response history. The solution from the perturbation response is not carried
    over to subsequent steps and, therefore, does not contribute to the response
    history. A linear step can be used only to analyze linear problems, but can
    be static, dynamic or multiphysics.

    Parameters
    ----------
    name : str
        Name of the LinearPerturbationStep.
    """

    def __init__(self,  name):
        super(LinearStep, self).__init__(name)
        self.__name__ = 'LinearPerturbationStep'


class LinearStaticStep(LinearStep, StaticStep):
    """Initialises LinearStaticStep object for use in a linear static analysis.


    Parameters
    ----------
    name : str
        Name of the LinearPerturbationStep.
    """

    def __init__(self,  name):
        super(LinearStaticStep, self).__init__(name)
        self.__name__ = 'LinearPerturbationStaticStep'


# TODO implement dynamic steps
class LinearFrequencyStep(LinearStep, ):
    """Initialises LinearStaticStep object for use in a linear static analysis.


    Parameters
    ----------
    name : str
        Name of the LinearPerturbationStep.
    """

    def __init__(self,  name):
        super(LinearFrequencyStep, self).__init__(name)
        self.__name__ = 'LinearFrequencyStep'

# class HarmonicStep(Step):
#     """Initialises HarmoniStep object for use in a harmonic analysis.

#     Parameters
#     ----------
#     name : str
#         Name of the HarmoniStep.
#     freq_list : list
#         Sorted list of frequencies to analyse.
#     displacements : list
#         Displacement object names.
#     loads : list
#         Load object names.
#     factor : float
#         Proportionality factor on the loads and displacements.
#     damping : float
#         Constant harmonic damping ratio.
#     stype : str
#         'harmonic'.

#     Attributes
#     ----------
#     name : str
#         Name of the HarmoniStep.
#     freq_list : list
#         Sorted list of frequencies to analyse.
#     displacements : list
#         Displacement object names.
#     loads : list
#         Load object names.
#     factor : float
#         Proportionality factor on the loads and displacements.
#     damping : float
#         Constant harmonic damping ratio.
#     stype : str
#         'harmonic'.
#     """

#     def __init__(self, name, freq_list, displacements=None, loads=None, factor=1.0, damping=None):
#         Step.__init__(self, name=name)

#         if not displacements:
#             displacements = []

#         if not loads:
#             loads = []

#         self.__name__ = 'HarmonicStep'
#         self.name = name
#         self.freq_list = freq_list
#         self.displacements = displacements
#         self.loads = loads
#         self.factor = factor
#         self.damping = damping
#         self.attr_list.extend(['freq_list', 'displacements', 'loads', 'factor', 'damping', 'stype'])


# class BucklingStep(Step):
#     """Initialises BucklingStep object for use in a buckling analysis.

#     Parameters
#     ----------
#     name : str
#         Name of the BucklingStep.
#     modes : int
#         Number of modes to analyse.
#     increments : int
#         Number of increments.
#     factor : float, dict
#         Proportionality factor on the loads and displacements.
#     displacements : list
#         Displacement object names.
#     loads : list
#         Load object names.
#     stype : str
#         'buckle'.
#     case : str
#         Step to copy loads and displacements from.

#     Attributes
#     ----------
#     name : str
#         Name of the BucklingStep.
#     modes : int
#         Number of modes to analyse.
#     increments : int
#         Number of increments.
#     factor : float, dict
#         Proportionality factor on the loads and displacements.
#     displacements : list
#         Displacement object names.
#     loads : list
#         Load object names.
#     stype : str
#         'buckle'.
#     case : str
#         Step to copy loads and displacements from.
#     """

#     def __init__(self, name, modes=5, increments=100, factor=1., displacements=None, loads=None, case=None):
#         Step.__init__(self, name=name)

#         if not displacements:
#             displacements = []

#         if not loads:
#             loads = []

#         self.__name__ = 'BucklingStep'
#         self.name = name
#         self.modes = modes
#         self.increments = increments
#         self.factor = factor
#         self.displacements = displacements
#         self.loads = loads
#         self.case = case
#         self.attr_list.extend(['modes', 'increments', 'factor', 'displacements', 'loads', 'case'])


# class AcousticStep(Step):
#     """Initialises AcoustiStep object for use in a acoustic analysis.

#     Parameters
#     ----------
#     name : str
#         Name of the AcoustiStep.
#     freq_range : list
#         Range of frequencies to analyse.
#     freq_step : int
#         Step size for frequency range.
#     displacements : list
#         Displacement object names.
#     loads : list
#         Load object names.
#     sources : list
#         List of source elements or element sets radiating sound.
#     samples : int
#         Number of samples for acoustic analysis.
#     factor : float
#         Proportionality factor on the loads and displacements.
#     damping : float
#         Constant harmonic damping ratio.
#     type : str
#         'acoustic'.

#     Attributes
#     ----------
#     name : str
#         Name of the AcoustiStep.
#     freq_range : list
#         Range of frequencies to analyse.
#     freq_step : int
#         Step size for frequency range.
#     displacements : list
#         Displacement object names.
#     loads : list
#         Load object names.
#     sources : list
#         List of source elements or element sets radiating sound.
#     samples : int
#         Number of samples for acoustic analysis.
#     factor : float
#         Proportionality factor on the loads and displacements.
#     damping : float
#         Constant harmonic damping ratio.
#     type : str
#         'acoustic'.
#     """

#     def __init__(self, name, freq_range, freq_step, displacements=None, loads=None, sources=None, samples=5,
#                  factor=1.0, damping=None):
#         Step.__init__(self, name=name)

#         if not displacements:
#             displacements = []

#         if not loads:
#             loads = []

#         if not sources:
#             sources = []

#         self.__name__ = 'AcousticStep'
#         self.name = name
#         self.freq_range = freq_range
#         self.freq_step = freq_step
#         self.displacements = displacements
#         self.sources = sources
#         self.samples = samples
#         self.loads = loads
#         self.factor = factor
#         self.damping = damping
#         self.attr_list.extend(['freq_range', 'freq_step', 'displacements', 'sources', 'samples', 'loads', 'factor',
#                                'damping'])

# class HeatStep(Step):
#     """Initialises HeatStep object for use in a thermal analysis.

#     Parameters
#     ----------
#     name : str
#         Name of the HeatStep.
#     interaction : str
#         Name of the HeatTransfer interaction.
#     increments : int
#         Number of case step increments.
#     temp0 : float
#         Initial temperature of all nodes.
#     dTmax : float
#         Maximum temperature increase per increment.
#     stype : str
#         'heat transfer'.
#     duration : float
#         Duration of case step.

#     Attributes
#     ----------
#     name : str
#         Name of the HeatStep.
#     interaction : str
#         Name of the HeatTransfer interaction.
#     increments : int
#         Number of case step increments.
#     temp0 : float
#         Initial temperature of all nodes.
#     dTmax : float
#         Maximum temperature increase per increment.
#     stype : str
#         'heat transfer'.
#     duration : float
#         Duration of case step.
#     """

#     def __init__(self, name, interaction, field_outputs, history_outputs, increments=100, temp0=20, dTmax=1, duration=1):
#         super(HeatStep, self).__init__(name, field_outputs, history_outputs)

#         self.__name__ = 'HeatStep'
#         self.interaction = interaction
#         self.increments = increments
#         self.temp0 = temp0
#         self.dTmax = dTmax
#         self.duration = duration
