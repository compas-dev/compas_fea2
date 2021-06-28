
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base.problem import GeneralCaseBase
from compas_fea2.backends._base.problem import LinearPerturbationCaseBase
from compas_fea2.backends._base.problem import HeatCaseBase
from compas_fea2.backends._base.problem import ModalCaseBase
from compas_fea2.backends._base.problem import HarmonicCaseBase
from compas_fea2.backends._base.problem import BucklingCaseBase
from compas_fea2.backends._base.problem import AcousticCaseBase

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

# TODO add field and history output requrests


class GeneralStaticStep(GeneralCaseBase):
    """
    Notes
    -----
    the data for the input file for this object is generated at runtime.
    """
    __doc__ += GeneralCaseBase.__doc__

    def __init__(self, name, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1,
                 nlgeom=False, displacements=None, loads=None, modify=True, field_outputs=None, history_outputs=None):
        super(GeneralStaticStep, self).__init__(name, max_increments, initial_inc_size, min_inc_size, time, nlgeom,
                                                displacements, loads, modify, field_outputs, history_outputs)
        self.stype = 'Static'
        self.attr_list.extend(['stype'])

    def _generate_data(self, problem):
        """generate the data for the input file. Since the `Problem` object is required,
        the data is generated just before writing the input file.
        """
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

        if self.displacements:
            for displacement in self.displacements:
                section_data.append(problem.displacements[displacement]._generate_data())

        line = """**\n** LOADS\n**\n"""
        section_data.append(line)

        if self.loads:
            for load in self.loads:
                section_data.append(problem.loads[load]._generate_data())

        line = ("**\n"
                "** OUTPUT REQUESTS\n"
                "**\n"
                "*Restart, write, frequency=0\n"
                "**\n")
        section_data.append(line)

        for foutput in self.field_outputs:
            section_data.append(problem.field_outputs[foutput].data)
        for houtput in self.history_outputs:
            section_data.append(problem.history_outputs[houtput].data)
        section_data.append('*End Step\n')

        return ''.join(section_data)


class GeneralStaticRiksStep(GeneralCaseBase):

    def __init__(self, name, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, displacements=[], loads=[]):
        super(GeneralStaticRiksStep).__init__(name, max_increments,
                                              initial_inc_size, min_inc_size, time, nlgeom, displacements, loads)
        raise NotImplementedError


class StaticLinearPertubationStep(LinearPerturbationCaseBase):
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

        self.__name__ = 'StaticPerturbationStep'
        self.name = name
        self.nlgeom = 'NO'  # TODO this depends on the previous step -> loop through the steps order and adjust this parameter
        self.displacements = displacements
        self.loads = loads
        self.attr_list.extend(['displacements', 'loads'])
        self.type = 'Static'

        self.data = ("** ----------------------------------------------------------------\n"
                     "**\n"
                     "** STEP: {0}\n"
                     "**\n"
                     "* Step, name={0}, nlgeom={1}, perturbation\n"
                     "*{2}\n"
                     "**\n").format(self.name, self.nlgeom, self.stype)


class BuckleStep(LinearPerturbationCaseBase):

    """Initialises BuckleStep object for use in a buckling analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    """

    def __init__(self, name, nmodes, displacements, loads):
        super(BuckleStep).__init__(name, displacements, loads)
        raise NotImplementedError
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


class HeatStep(HeatCaseBase):
    def __init__(self, name, interaction, increments, temp0, dTmax, type, duration):
        super(HeatStep, self).__init__(name, interaction, increments, temp0, dTmax, type, duration)
        raise NotImplementedError


class ModalStep(ModalCaseBase):
    def __init__(self, name, modes):
        super(ModalStep, self).__init__(name, modes)

    def _generate_data(self):

        data = ("** ----------------------------------------------------------------\n"
                "**\n"
                "** STEP: {0}\n"
                "**\n"
                "* Step, name={0}\n"
                "*FREQUENCY, EIGENSOLVER=LANCZOS, NORMALIZATION=DISPLACEMENT\n"
                "{1}\n"
                "*END STEP").format(self.name, self.modes)

        return data


class HarmoniStepBase(HarmonicCaseBase):

    def __init__(self, name, freq_list, displacements, loads, factor, damping, type):
        super(HarmoniStepBase, self).__init__(name, freq_list, displacements, loads, factor, damping, type)
        raise NotImplementedError


class BucklingStep(BucklingCaseBase):
    def __init__(self, name, modes, increments, factor, displacements, loads, type, step):
        super(BucklingStep, self).__init__(name, modes, increments, factor, displacements, loads, type, step)
        raise NotImplementedError


class AcoustiStepBase(AcousticCaseBase):

    def __init__(self, name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type):
        super(AcoustiStepBase, self).__init__(name, freq_range, freq_step,
                                              displacements, loads, sources, samples, factor, damping, type)
        raise NotImplementedError
