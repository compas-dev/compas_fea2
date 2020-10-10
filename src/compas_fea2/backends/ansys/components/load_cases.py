
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base import StepBase
from compas_fea2.backends._base import GeneralStepBase
from compas_fea2.backends._base import HeatStepBase
from compas_fea2.backends._base import ModalStepBase
from compas_fea2.backends._base import HarmonicStepBase
from compas_fea2.backends._base import BucklingStepBase
from compas_fea2.backends._base import AcousticStepBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Step',
    'GeneralStep',
    # 'HeatStepBase',
    'ModalStep',
    'HarmoniStepBase',
    'BucklingStep',
    'AcoustiStepBase'
]


class Step(StepBase):

    """ Initialises base Step object.

    Parameters
    ----------
    name : str
        Name of the Step object.

    Attributes
    ----------
    name : str
        Name of the Step object.

    """
    pass
    # def __init__(self, name):
    #     super(Step, self).__init__(name)


class GeneralStep(GeneralStepBase):

    """ Initialises GeneralStep object for use in a static analysis.

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
    pass
    # def __init__(self, name, increments, iterations, tolerance, factor, nlgeom, nlmat, displacements, loads, type, modify):
    #     super(GeneralStep, self).__init__(name, increments, iterations, tolerance, factor, nlgeom, nlmat, displacements, loads, type, modify)


class HeatStep(HeatStepBase):

    """ Initialises HeatStep object for use in a thermal analysis.

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
    pass
    # def __init__(self, name, interaction, increments, temp0, dTmax, type, duration):
    #     super(HeatStep, self).__init__(name, interaction, increments, temp0, dTmax, type, duration)


class ModalStep(ModalStepBase):

    """ Initialises ModalStep object for use in a modal analysis.

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
    pass
    # def __init__(self, name, modes, increments, displacements, type):
    #     super(ModalStep, self).__init__(name, modes, increments, displacements, type)


class HarmoniStepBase(HarmonicStepBase):

    """ Initialises HarmoniStepBase object for use in a harmonic analysis.

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
    pass
    # def __init__(self, name, freq_list, displacements, loads, factor, damping, type):
    #     super(HarmoniStepBase, self).__init__(name, freq_list, displacements, loads, factor, damping, type)


class BucklingStep(BucklingStepBase):

    """ Initialises BucklingStep object for use in a buckling analysis.

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
    pass
    # def __init__(self, name, modes, increments, factor, displacements, loads, type,step):
    #     super(BucklingStep, self).__init__(name, modes, increments, factor, displacements, loads, type, step)


class AcoustiStepBase(AcousticStepBase):

    """ Initialises AcoustiStepBase object for use in a acoustic analysis.

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
    pass
    # def __init__(self, name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type):
    #     super(AcoustiStepBase, self).__init__(name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type)
