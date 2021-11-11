from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase

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

    Attributes
    ----------
    name : str
        Name of the Case object.

    """

    def __init__(self, name, field_outputs, history_outputs):

        self.__name__ = 'CaseBase'
        self._name = name
        self._field_outputs = field_outputs
        self._history_outputs = history_outputs

    @property
    def name(self):
        """str : Name of the Case object."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def field_outputs(self):
        """obj : `compas_fea2` FieldOutput object"""
        return self._field_outputs

    @field_outputs.setter
    def field_outputs(self, value):
        self._field_outputs = value

    @property
    def history_outputs(self):
        """obj : `compas_fea2` HistoryOutput object"""
        return self._history_outputs

    @history_outputs.setter
    def history_outputs(self, value):
        self._history_outputs = value

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class GeneralStaticCaseBase(CaseBase):
    """Initialises GeneralCase object for use in a static analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralCase.
    max_increments : int
        Max number of increments to perform during the case step.
        (Typically 100 but you might have to increase it in highly non-linear problems. This might increase the
        analysis time.).
    initial_inc_size : float
        Sets the the size of the increment for the first iteration.
        (By default is equal to the total time, meaning that the software decrease the size automatically.)
    min_inc_size : float
        Minimum increment size before stopping the analysis.
        (By default is 1e-5, but you can set a smaller size for highly non-linear problems. This might increase the
        analysis time.)
    time : float
        Total time of the case step. Note that this not actual 'time' in Abaqus, but rather a proportionality factor.
        (By default is 1, meaning that the analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        Analyse non-linear geometry effects.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    modify : bool #TODO not implemented yet
        Modify the previously added loads.
    field_output : list
        FiledOutputRequest object
    history_output : list
        HistoryOutputRequest object
    """

    def __init__(self, name, max_increments, initial_inc_size, min_inc_size, time,
                 nlgeom, displacements, loads, modify, field_outputs, history_outputs):
        super(GeneralStaticCaseBase, self).__init__(name, field_outputs, history_outputs)

        self.__name__ = 'GeneralCase'
        self.max_increments = max_increments
        self.initial_inc_size = initial_inc_size
        self.min_inc_size = min_inc_size
        self.time = time

        if nlgeom:
            self.nlgeom = 'YES'
        else:
            self.nlgeom = 'NO'

        self.displacements = displacements
        self.loads = loads


class StaticLinearPerturbationCaseBase(CaseBase):
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

    def __init__(self, name, displacements, loads, field_outputs, history_outputs):
        super(StaticLinearPerturbationCaseBase, self).__init__(name, field_outputs, history_outputs)

        self.__name__ = 'StaticLinearPerturbationCase'
        self.displacements = displacements
        self.loads = loads


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
