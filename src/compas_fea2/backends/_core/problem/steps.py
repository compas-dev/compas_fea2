from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez),
#            Francesco Ranaudo (github.com/franaudo)

# TODO: change 'Step' to 'Case' to make it less abaqus-dependent

__all__ = [
    'StepBase',
    'GeneralStepBase',
    'HeatStepBase',
    'ModalStepBase',
    'HarmonicStepBase',
    'BucklingStepBase',
    'AcousticStepBase'
]


class StepBase(object):
    """Initialises base Step object.

    Parameters
    ----------
    name : str
        Name of the Step object.

    Attributes
    ----------
    name : str
        Name of the Step object.

    """

    def __init__(self, name):

        self.__name__  = 'StepObject'
        self.name      = name
        self.attr_list = ['name']

    def __str__(self):
        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 10))
        for attr in self.attr_list:
            print('{0:<13} : {1}'.format(attr, getattr(self, attr)))
        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class GeneralStepBase(StepBase):
    """Initialises GeneralStep object for use in a static analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    increments : int
        Number of step increments.
    iterations : int
        Number of step iterations.
    tolerance : float
        A tolerance for analysis solvers.
    factor : float, dict
        Proportionality factor(s) on the loads and displacements.
    nlgeom : bool
        Analyse non-linear geometry effects.
    nlmat : bool
        Analyse non-linear material effects.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    type : str
        'static','static,riks'.
    modify : bool
        Modify the previously added loads.

    """

    def __init__(self, name, increments=100, iterations=100, tolerance=0.01, factor=1.0, nlgeom=False, nlmat=True, displacements=None, loads=None, stype='static', modify=True):
        StepBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        self.__name__      = 'GeneralStep'
        self.name          = name
        self.increments    = increments
        self.iterations    = iterations
        self.tolerance     = tolerance
        self.factor        = factor
        self.nlgeom        = nlgeom
        self.nlmat         = nlmat
        self.displacements = displacements
        self.loads         = loads
        self.modify        = modify
        self.stype          = stype
        self.attr_list.extend(['increments', 'iterations', 'factor', 'nlgeom', 'nlmat', 'displacements', 'loads',
                               'stype', 'tolerance', 'modify'])


class HeatStepBase(StepBase):
    """Initialises HeatStep object for use in a thermal analysis.

    Parameters
    ----------
    name : str
        Name of the HeatStep.
    interaction : str
        Name of the HeatTransfer interaction.
    increments : int
        Number of step increments.
    temp0 : float
        Initial temperature of all nodes.
    dTmax : float
        Maximum temperature increase per increment.
    type : str
        'heat transfer'.
    duration : float
        Duration of step.

    """

    def __init__(self, name, interaction, increments=100, temp0=20, dTmax=1, stype='heat transfer', duration=1):
        StepBase.__init__(self, name=name)

        self.__name__    = 'HeatStep'
        self.name        = name
        self.interaction = interaction
        self.increments  = increments
        self.temp0       = temp0
        self.dTmax       = dTmax
        self.stype        = stype
        self.duration    = duration
        self.attr_list.extend(['interaction', 'increments', 'temp0', 'dTmax', 'stype', 'duration'])


class ModalStepBase(StepBase):
    """Initialises ModalStep object for use in a modal analysis.

    Parameters
    ----------
    name : str
        Name of the ModalStep.
    modes : int
        Number of modes to analyse.
    increments : int
        Number of increments.
    displacements : list
        Displacement object names.
    type : str
        'modal'.

    """

    def __init__(self, name, modes=10, increments=100, displacements=None, stype='modal'):
        StepBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        self.__name__      = 'ModalStep'
        self.name          = name
        self.modes         = modes
        self.increments    = increments
        self.displacements = displacements
        self.stype          = stype
        self.attr_list.extend(['modes', 'increments', 'displacements', 'stype'])


class HarmonicStepBase(StepBase):
    """Initialises HarmoniStepBase object for use in a harmonic analysis.

    Parameters
    ----------
    name : str
        Name of the HarmoniStepBase.
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
    type : str
        'harmonic'.

    """

    def __init__(self, name, freq_list, displacements=None, loads=None, factor=1.0, damping=None, stype='harmonic'):
        StepBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        self.__name__      = 'HarmonicStepBase'
        self.name          = name
        self.freq_list     = freq_list
        self.displacements = displacements
        self.loads         = loads
        self.factor        = factor
        self.damping       = damping
        self.stype          = stype
        self.attr_list.extend(['freq_list', 'displacements', 'loads', 'factor', 'damping', 'stype'])


class BucklingStepBase(StepBase):
    """Initialises BucklingStep object for use in a buckling analysis.

    Parameters
    ----------
    name : str
        Name of the BucklingStep.
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
    type : str
        'buckle'.
    step : str
        Step to copy loads and displacements from.

    """

    def __init__(self, name, modes=5, increments=100, factor=1., displacements=None, loads=None, stype='buckle',
                 step=None):
        StepBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        self.__name__      = 'BucklingStep'
        self.name          = name
        self.modes         = modes
        self.increments    = increments
        self.factor        = factor
        self.displacements = displacements
        self.loads         = loads
        self.stype          = stype
        self.step          = step
        self.attr_list.extend(['modes', 'increments', 'factor', 'displacements', 'loads', 'stype', 'step'])


class AcousticStepBase(StepBase):
    """Initialises AcoustiStepBase object for use in a acoustic analysis.

    Parameters
    ----------
    name : str
        Name of the AcoustiStepBase.
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

    """

    def __init__(self, name, freq_range, freq_step, displacements=None, loads=None, sources=None, samples=5,
                 factor=1.0, damping=None, stype='acoustic'):
        StepBase.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        if not sources:
            sources = []

        self.__name__      = 'AcousticStepBase'
        self.name          = name
        self.freq_range    = freq_range
        self.freq_step     = freq_step
        self.displacements = displacements
        self.sources       = sources
        self.samples       = samples
        self.loads         = loads
        self.factor        = factor
        self.damping       = damping
        self.stype          = stype
        self.attr_list.extend(['freq_range', 'freq_step', 'displacements', 'sources', 'samples', 'loads', 'factor',
                               'damping', 'stype'])
