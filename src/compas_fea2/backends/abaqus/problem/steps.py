
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base.problem import StepBase
from compas_fea2.backends._base.problem import GeneralStepBase
from compas_fea2.backends._base.problem import HeatStepBase
from compas_fea2.backends._base.problem import ModalStepBase
from compas_fea2.backends._base.problem import HarmonicStepBase
from compas_fea2.backends._base.problem import BucklingStepBase
from compas_fea2.backends._base.problem import AcousticStepBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'GeneralStaticStep',
    'StaticLinearPertubationStep',
    # 'HeatStepBase',
    'ModalStep',
    'HarmoniStepBase',
    'BucklingStep',
    'AcoustiStepBase'
]

# TODO remove _GeneralStep and get everything forn _base
# TODO add field and history output requrests

class _GeneralStep(StepBase):
    """Initialises GeneralStep object for use in a static analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    max_increments : int
        Max number of increments to perform during the step.
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
        Total time of the step. Note that this not actual 'time' in Abaqus, but rather a proportionality factor.
        (By default is 1, meaning that the analysis is complete when all the increments sum up to 1)
    nlgeom : bool
        Analyse non-linear geometry effects.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    field_output : list
        FiledOutputRequest object
    history_output : list
        HistoryOutputRequest object
    """

    def __init__(self, name, max_increments, initial_inc_size, min_inc_size, time,
                nlgeom, displacements, loads, field_outputs, history_outputs):
        super(_GeneralStep, self).__init__(name=name)

        self.__name__           = 'GeneralStep'
        self.name               = name
        self.max_increments     = max_increments
        self.initial_inc_size   = initial_inc_size
        self.min_inc_size       = min_inc_size
        self.time               = time

        if nlgeom:
            self.nlgeom         = 'YES'
        else:
            self.nlgeom         = 'NO'

        self.displacements      = displacements
        self.loads              = loads
        self.field_outputs      = field_outputs
        self.history_outputs    = history_outputs

        # self.attr_list.extend(['increments', 'max_increments', 'initial_inc_size', 'min_inc_size', 'time', 'nlgeom',
        #                     'displacements', 'loads'])




class GeneralStaticStep(_GeneralStep):
    def __init__(self, name, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1,
                nlgeom=False, displacements=[], loads=[], field_outputs=[], history_outputs=[]):
        super(GeneralStaticStep, self).__init__(name, max_increments, initial_inc_size,min_inc_size, time, nlgeom,
                                                displacements, loads, field_outputs, history_outputs)
        self.stype = 'Static'
        self.attr_list.extend(['stype'])

        # self.data = self._generate_data()

    def _generate_data(self, displacements=[], loads=[], field_outputs=[], history_outputs=[]):  #todo: this could be moved outside the class

        section_data = []
        line = ("** ----------------------------------------------------------------\n"
                "**\n"
                "** STEP: {0}\n"
                "**\n"
                "* Step, name={0}, nlgeom={1}, inc={2}\n"
                "*{3}\n"
                "{4}, {5}, {6}, {5}\n"
                "**\n"
                "** DISPLACEMENTS\n"
                "**\n").format(self.name, self.nlgeom, self.max_increments, self.stype, self.initial_inc_size, self.time,
                               self.min_inc_size)
        section_data.append(line)

        for displacement in displacements:
            section_data.append(displacement._generate_data())

        line = """**\n** LOADS\n**\n"""
        section_data.append(line)

        for load in loads:
            section_data.append(load._generate_data())

        line = ("**\n"
                "** OUTPUT REQUESTS\n"
                "**\n"
                "*Restart, write, frequency=0\n"
                "**\n")
        section_data.append(line)

        for foutput in field_outputs:
            section_data.append(foutput.data)
        for houtput in history_outputs:
            section_data.append(houtput.data)
        section_data.append('*End Step\n')

        return ''.join(section_data)

class GeneralStaticRiksStep(_GeneralStep):
    NotImplemented
    # def __init__(self, name, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1,
    #             nlgeom=False, displacements=[], loads=[]):
    #     super(GeneralStaticRiksStep).__init__(name, max_increments, initial_inc_size, min_inc_size, time,
    #                                 nlgeom, displacements, loads)
    #     self.stype = 'Static, riks'
    #     self.attr_list.extend(['stype'])

    #     self.data = _generate_data(self)


class _LinearPertubationStep(StepBase):
    """Initialises LinearPertubationStep object for use in a linear analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    """

    def __init__(self, name, displacements, loads):
        super(_LinearPertubationStep, self).__init__(name)

        self.__name__      = 'LinearPerturbationStep'
        self.name          = name
        self.nlgeom        = 'NO'
        self.displacements = displacements
        self.loads         = loads
        self.attr_list.extend(['displacements', 'loads', ])


class StaticLinearPertubationStep(_LinearPertubationStep):
    """Initialises the StaticLinearPertubationStep object for use in a static analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    """

    def __init__(self, name, displacements, loads):
        super(StaticLinearPertubationStep, self).__init__(name, displacements, loads)

        self.__name__      = 'StaticPerturbationStep'
        self.name          = name
        self.nlgeom        = 'NO'  #TODO this depends on the previous step -> loop through the steps order and adjust this parameter
        self.displacements = displacements
        self.loads         = loads
        self.attr_list.extend(['displacements', 'loads'])
        self.type = 'Static'

        self.data = ("** ----------------------------------------------------------------\n"
                    "**\n"
                    "** STEP: {0}\n"
                    "**\n"
                    "* Step, name={0}, nlgeom={1}, perturbation\n"
                    "*{2}\n"
                    "**\n").format(self.name, self.nlgeom, self.stype)

class BuckleStep(_LinearPertubationStep):
    NotImplemented
#     """Initialises BuckleStep object for use in a buckling analysis.

#     Parameters
#     ----------
#     name : str
#         Name of the GeneralStep.
#     displacements : list
#         Displacement objects.
#     loads : list
#         Load objects.
#     """

#     def __init__(self, name, nmodes, displacements, loads):
#         super(BuckleStep).__init__(name=name, displacements=displacements, loads=loads)

#         self.__name__      = 'BuckleStep'
#         self.name          = name
#         self.nlgeom        = 'NO'  #TODO this depends on the previous step -> loop through the steps order and adjust this parameter
#         self.displacements = displacements
#         self.loads         = loads
#         self.attr_list.extend(['displacements', 'loads'])
#         self.type = 'Buckle'

#         self.data = """** ----------------------------------------------------------------
# **
# ** STEP: {0}
# **
# * Step, name={0}, nlgeom={1}, perturbation
# *{2}
# **\n""".format(self.name, self.nlgeom, self.stype)


class HeatStep(HeatStepBase):
    NotImplemented
    # def __init__(self, name, interaction, increments, temp0, dTmax, type, duration):
    #     super(HeatStep, self).__init__(name, interaction, increments, temp0, dTmax, type, duration)


class ModalStep(ModalStepBase):
    NotImplemented
    # def __init__(self, name, modes, increments, displacements, type):
    #     super(ModalStep, self).__init__(name, modes, increments, displacements, type)


class HarmoniStepBase(HarmonicStepBase):
    NotImplemented
    # def __init__(self, name, freq_list, displacements, loads, factor, damping, type):
    #     super(HarmoniStepBase, self).__init__(name, freq_list, displacements, loads, factor, damping, type)


class BucklingStep(BucklingStepBase):
    NotImplemented
    # def __init__(self, name, modes, increments, factor, displacements, loads, type,step):
    #     super(BucklingStep, self).__init__(name, modes, increments, factor, displacements, loads, type, step)


class AcoustiStepBase(AcousticStepBase):
    NotImplemented
    # def __init__(self, name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type):
    #     super(AcoustiStepBase, self).__init__(name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type)
