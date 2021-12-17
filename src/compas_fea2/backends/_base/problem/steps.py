from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib

from compas_fea2.backends._base.base import FEABase
from compas_fea2.backends._base.problem.loads import LoadBase
from compas_fea2.backends._base.problem.displacements import GeneralDisplacementBase
from compas_fea2.backends._base.problem.outputs import FieldOutputBase
from compas_fea2.backends._base.model.parts import PartBase
from compas_fea2.backends._base.model.groups import NodesGroupBase
from compas_fea2.backends._base.model.groups import ElementsGroupBase

# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez),
#            Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'CaseBase',
    'GeneralStaticCaseBase',
    'StaticLinearPerturbationCaseBase',
    'HeatCaseBase',
    'ModalCaseBase',
    'HarmonicCaseBase',
    'BucklingCaseBase',
    'AcousticCaseBase'
]


class CaseBase(FEABase):
    """Initialises base Case object.

    Parameters
    ----------
    name : str
        Name of the Case object.
    field_outputs : obj
        `compas_fea2` FieldOutput object.
    History_outputs : obj
        `compas_fea2` HistiryOutput object.
    """

    def __init__(self, name):
        super(CaseBase, self).__init__(name)
        self.__name__ = 'CaseBase'
        self._name = name
        self._gravity = None
        self._loads = {}
        self._applied_loads = {}
        self._displacements = {}
        self._applied_displacements = {}
        self._field_outputs = {}
        self._history_outputs = {}

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    @property
    def name(self):
        """str : Name of the Case object."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def gravity(self):
        """The gravity property."""
        return self._gravity

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
            `compas_fea2` Output objects. Can be either a FieldOutput or a HistoryOutput

        Returns
        -------
        None
        """
        attrb_name = '_field_outputs' if isinstance(output, FieldOutputBase) else '_history_output'
        if not getattr(self, attrb_name):
            setattr(self, attrb_name, {})
        if output.name not in getattr(self, attrb_name):
            getattr(self, attrb_name)[output.name] = output
        else:
            print('WARNING: {} already present in the Problem. skipped!'.format(output.__repr__()))

    def add_outputs(self, outputs):
        """Add multiple outputs to the Step object.

        Parameters
        ----------
        outputs : list
            list of `compas_fea2` Output objects. Can be both FieldOutput and HistoryOutput objects

        Returns
        -------
        None
        """
        for output in outputs:
            self.add_output(output)

    # =========================================================================
    #                           Loads methods
    # =========================================================================

    def add_load(self, load, keys, part):
        """Add a load to Step object.

        Parameters
        ----------
        load : obj
            `compas_fea2` Load objects
        key : int
            node or element key
        part : str
            part name

        Returns
        -------
        None
        """

       # check if load is valid
        if not isinstance(load, LoadBase):
            raise TypeError(f'{load} is not a `compas_fea2` Load object')
        if part not in self.loads:
            self._loads[part] = {key: load for key in keys}
        else:
            # TODO this wrong because a node can have more than one load applied to it
            # restructure the way the information is stored
            for key in keys:
                if key in self.loads[part]:
                    raise ValueError(f"overconstrained node: {self.parts[part].nodes[key]}")
                else:
                    self._loads[part][key] = load
        # if load.name not in self._applied_loads:
        #     self._applied_loads[load.name] = [(part, where)]
        # else:
        #     self._applied_load[load.name].append((part, where))

        # print(f'{load.__repr__()} added to {self.__repr__()}')
        # # check if where is valid
        # keys = []
        # if not isinstance(where, list):
        #     where = [where]
        # for i in where:
        #     if isinstance(i, (NodesGroupBase, ElementsGroupBase)):
        #         keys += [key+1 for key in i._selection]
        #     elif isinstance(i, int):
        #         keys.append(i+1)
        #     else:
        #         raise TypeError('You must provide either a (list of) key or a (list of) NodesGroup/ElementsGroup')

        # # check if load is valid
        # if not isinstance(load, LoadBase):
        #     raise TypeError(f'{load} is not a `compas_fea2` Load object')

        # # check if part is valid
        # if isinstance(part, PartBase):
        #     part = part.name
        # elif not isinstance(part, str):
        #     raise TypeError(f'{part} is not valid')

        # if load.name not in self.loads:
        #     self.loads[load.name] = load

        # if load.name not in self._applied_loads:
        #     self._applied_loads[load.name] = [(part, where)]
        # else:
        #     self._applied_load[load.name].append((part, where))

        # print(f'{load.__repr__()} added to {self.__repr__()}')

    def add_loads(self, loads):
        for load in loads:
            self.add_load(load)

    def add_point_load(self, name, part, nodes, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        load = m.PointLoad(name, x, y, z, xx, yy, zz, axes)
        self._loads.setdefault(part, {})[load] = nodes

    def add_gravity_load(self, name='gravity', g=9.81, x=0., y=0., z=-1.):
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        load = m.GravityLoad(name, g, x, y, z)
        self._gravity = load

    def add_prestress_load(self):
        raise NotImplemented

    def add_line_load(self):
        raise NotImplemented

    def add_area_load(self):
        raise NotImplemented

    def add_tributary_load(self):
        raise NotImplemented

    def add_harmonic_point_load(self):
        raise NotImplemented

    def add_harmonic_preassure_load(self):
        raise NotImplemented

    def add_acoustic_diffuse_field_load(self):
        raise NotImplemented

    # =========================================================================
    #                       Displacement methods
    # =========================================================================

    def add_displacement(self, displacement, where, part):
        """Add a displacement to Step object.

        Parameters
        ----------
        displacement : obj
            `compas_fea2` Displacement object.

        Returns
        -------
        None
        """
        # check if where is valid
        keys = []
        if not isinstance(where, list):
            where = [where]
        for i in where:
            if isinstance(i, (NodesGroupBase)):
                keys += [key+1 for key in i._selection]
            elif isinstance(i, int):
                keys.append(i+1)
            else:
                raise ValueError('You must provide either a (list of) key or a (list of) NodesGroup')

        # check if load is valid
        if not isinstance(displacement, GeneralDisplacementBase):
            raise ValueError(f'{load} is not a `compas_fea2` GeneralDisplacement object')

        # check if part is valid
        if isinstance(part, PartBase):
            part = part.name
        elif not isinstance(part, str):
            raise ValueError(f'{part} is not valid')

        if displacement.name not in self.displacements:
            self.displacements[displacement.name] = displacement

        if displacement.name not in self._applied_displacements:
            self._applied_displacements[displacement.name] = [(part, where)]
        else:
            self._applied_displacement[displacement.name].append((part, where))


class StaticCaseBase(CaseBase):
    """Initialises base Case object.

    Parameters
    ----------
    name : str
        Name of the Case object.
    loads : list
        `compas_fea2` Load objects.
    displacements : list
        `compas_fea2` Displacement objects.
    field_outputs : obj
        `compas_fea2` FieldOutput object.
    History_outputs : obj
        `compas_fea2` HistiryOutput object.
    """

    def __init__(self, name):
        super(StaticCaseBase, self).__init__(name)
        self.__name__ = 'StaticCaseBase'
        self._loads = {}
        self._displacements = {}

    @property
    def loads(self):
        """list : list of `compas_fea2` Load objects."""
        return self._loads

    @loads.setter
    def loads(self, value):
        self._loads = value

    @property
    def displacements(self):
        """list : list of `compas_fea2` Displacement objects."""
        return self._displacements


class GeneralStaticCaseBase(StaticCaseBase):
    """Initialises GeneralCase object for use in a static analysis.
    """

    def __init__(self, name, max_increments, initial_inc_size, min_inc_size, time):
        super(GeneralStaticCaseBase, self).__init__(name)

        self.__name__ = 'GeneralCase'

        self._max_increments = max_increments
        self._initial_inc_size = initial_inc_size
        self._min_inc_size = min_inc_size
        self._time = time

    @property
    def max_increments(self):
        """int : Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear problems. This might increase the
        analysis time.)."""
        return self._max_increments

    @max_increments.setter
    def max_increments(self, value):
        self._max_increments = value

    @property
    def initial_inc_size(self):
        """float : Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease the size automatically.)"""
        return self._initial_inc_size

    @initial_inc_size.setter
    def initial_inc_size(self, value):
        self._initial_inc_size = value

    @property
    def min_inc_size(self):
        """float : Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear problems. This might increase the
        analysis time.)"""
        return self._min_inc_size

    @min_inc_size.setter
    def min_inc_size(self, value):
        self._min_inc_size = value

    @property
    def time(self):
        """float : Total time of the case step. Note that this not actual 'time' in Abaqus, but rather a proportionality factor.
        (By default is 1, meaning that the analysis is complete when all the increments sum up to 1)"""
        return self._time

    @time.setter
    def time(self, value):
        self._time = value


# TODO CHECK this sis a duplicate of StaticCaseBase
class StaticLinearPerturbationCaseBase(StaticCaseBase):
    """Initialises LinearPertubationCase object for use in a linear analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralCase.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    """

    def __init__(self,  name):
        super(StaticLinearPerturbationCaseBase, self).__init__(name)
        self.__name__ = 'StaticLinearPerturbationCase'


class HeatCaseBase(CaseBase):
    """Initialises HeatCase object for use in a thermal analysis.

    Parameters
    ----------
    name : str
        Name of the HeatCase.
    interaction : str
        Name of the HeatTransfer interaction.
    increments : int
        Number of case step increments.
    temp0 : float
        Initial temperature of all nodes.
    dTmax : float
        Maximum temperature increase per increment.
    stype : str
        'heat transfer'.
    duration : float
        Duration of case step.

    Attributes
    ----------
    name : str
        Name of the HeatCase.
    interaction : str
        Name of the HeatTransfer interaction.
    increments : int
        Number of case step increments.
    temp0 : float
        Initial temperature of all nodes.
    dTmax : float
        Maximum temperature increase per increment.
    stype : str
        'heat transfer'.
    duration : float
        Duration of case step.
    """

    def __init__(self, name, interaction, field_outputs, history_outputs, increments=100, temp0=20, dTmax=1, duration=1):
        super(HeatCaseBase, self).__init__(name, field_outputs, history_outputs)

        self.__name__ = 'HeatCase'
        self.interaction = interaction
        self.increments = increments
        self.temp0 = temp0
        self.dTmax = dTmax
        self.duration = duration


class ModalCaseBase(CaseBase):
    """Initialises ModalCase object for use in a modal analysis.

    Parameters
    ----------
    name : str
        Name of the ModalCase.
    modes : int
        Number of modes to analyse.
    """

    def __init__(self, name, modes=1):
        super(ModalCaseBase, self).__init__(name)

        self.__name__ = 'ModalCase'
        self._modes = modes

    @property
    def modes(self):
        """int : Number of modes to analyse."""
        return self._modes

    @modes.setter
    def modes(self, value):
        self._modes = value


class HarmonicCaseBase(CaseBase):
    """Initialises HarmoniCaseBase object for use in a harmonic analysis.

    Parameters
    ----------
    name : str
        Name of the HarmoniCaseBase.
    freq_list : list
        Sorted list of frequencies to analyse.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    factor : float
        Proportionality factor on the loads and displacements.
    damping : float
        Constant harmonic damping ratio.
    stype : str
        'harmonic'.

    Attributes
    ----------
    name : str
        Name of the HarmoniCaseBase.
    freq_list : list
        Sorted list of frequencies to analyse.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    factor : float
        Proportionality factor on the loads and displacements.
    damping : float
        Constant harmonic damping ratio.
    stype : str
        'harmonic'.
    """

    def __init__(self, name, freq_list, displacements=None, loads=None, factor=1.0, damping=None):
        CaseBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        self.__name__ = 'HarmonicCaseBase'
        self.name = name
        self.freq_list = freq_list
        self.displacements = displacements
        self.loads = loads
        self.factor = factor
        self.damping = damping
        self.attr_list.extend(['freq_list', 'displacements', 'loads', 'factor', 'damping', 'stype'])


class BucklingCaseBase(CaseBase):
    """Initialises BucklingCase object for use in a buckling analysis.

    Parameters
    ----------
    name : str
        Name of the BucklingCase.
    modes : int
        Number of modes to analyse.
    increments : int
        Number of increments.
    factor : float, dict
        Proportionality factor on the loads and displacements.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    stype : str
        'buckle'.
    case : str
        Case to copy loads and displacements from.

    Attributes
    ----------
    name : str
        Name of the BucklingCase.
    modes : int
        Number of modes to analyse.
    increments : int
        Number of increments.
    factor : float, dict
        Proportionality factor on the loads and displacements.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    stype : str
        'buckle'.
    case : str
        Case to copy loads and displacements from.
    """

    def __init__(self, name, modes=5, increments=100, factor=1., displacements=None, loads=None, case=None):
        CaseBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        self.__name__ = 'BucklingCase'
        self.name = name
        self.modes = modes
        self.increments = increments
        self.factor = factor
        self.displacements = displacements
        self.loads = loads
        self.case = case
        self.attr_list.extend(['modes', 'increments', 'factor', 'displacements', 'loads', 'case'])


class AcousticCaseBase(CaseBase):
    """Initialises AcoustiCaseBase object for use in a acoustic analysis.

    Parameters
    ----------
    name : str
        Name of the AcoustiCaseBase.
    freq_range : list
        Range of frequencies to analyse.
    freq_step : int
        Step size for frequency range.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    sources : list
        List of source elements or element sets radiating sound.
    samples : int
        Number of samples for acoustic analysis.
    factor : float
        Proportionality factor on the loads and displacements.
    damping : float
        Constant harmonic damping ratio.
    type : str
        'acoustic'.

    Attributes
    ----------
    name : str
        Name of the AcoustiCaseBase.
    freq_range : list
        Range of frequencies to analyse.
    freq_step : int
        Case size for frequency range.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    sources : list
        List of source elements or element sets radiating sound.
    samples : int
        Number of samples for acoustic analysis.
    factor : float
        Proportionality factor on the loads and displacements.
    damping : float
        Constant harmonic damping ratio.
    type : str
        'acoustic'.
    """

    def __init__(self, name, freq_range, freq_step, displacements=None, loads=None, sources=None, samples=5,
                 factor=1.0, damping=None):
        CaseBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        if not sources:
            sources = []

        self.__name__ = 'AcousticCaseBase'
        self.name = name
        self.freq_range = freq_range
        self.freq_step = freq_step
        self.displacements = displacements
        self.sources = sources
        self.samples = samples
        self.loads = loads
        self.factor = factor
        self.damping = damping
        self.attr_list.extend(['freq_range', 'freq_step', 'displacements', 'sources', 'samples', 'loads', 'factor',
                               'damping'])
