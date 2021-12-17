
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base.problem import GeneralStaticCaseBase
from compas_fea2.backends._base.problem import StaticLinearPerturbationCaseBase
from compas_fea2.backends._base.problem import HeatCaseBase
from compas_fea2.backends._base.problem import ModalCaseBase
from compas_fea2.backends._base.problem import HarmonicCaseBase
from compas_fea2.backends._base.problem import BucklingCaseBase
from compas_fea2.backends._base.problem import AcousticCaseBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

# __all__ = [
#     'GeneralStaticStep',
#     'StaticLinearPertubationStep',
#     # 'HeatStepBase',
#     'ModalStep',
#     'HarmoniStepBase',
#     'BucklingStep',
#     'AcoustiStepBase'
# ]

# TODO add field and history output requrests


class GeneralStaticStep(GeneralStaticCaseBase):
    """
    Notes
    -----
    the data for the input file for this object is generated at runtime.
    """
    # __doc__ += GeneralStaticCaseBase.__doc__

    def __init__(self, name, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True,):
        super(GeneralStaticStep, self).__init__(name, max_increments, initial_inc_size, min_inc_size, time)
        self._stype = 'Static'
        self._nlgeom = 'YES' if nlgeom else 'NO'
        self._modify = modify

        @property
        def nlgeometry(self):
            """The nlgeometry property."""
            return self.nlgeom

        @nlgeometry.setter
        def nlgeometry(self, value):
            self._nlgeom = 'YES' if value else 'NO'

        @property
        def modify(self):
            """The modify property."""
            return self._modify

        @modify.setter
        def modify(self, value):
            self._modify = value

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """

        return f"""**
{self._generate_header_section()}**
** DISPLACEMENTS
**
{self._generate_displacements_section()}**
** LOADS
**
{self._generate_loads_section()}**
** OUTPUT REQUESTS
**
{self._generate_output_section()}**
"""

    def _generate_header_section(self):
        data_section = []
        line = ("** ----------------------------------------------------------------\n"
                "**\n"
                f"** STEP: {0}\n"
                "**\n"
                "*Step, name={0}, nlgeom={1}, inc={2}\n"
                "*{3}\n"
                "{4}, {5}, {6}, {5}\n").format(self._name, self._nlgeom, self._max_increments, self._stype,
                                               self._initial_inc_size, self._time, self._min_inc_size)
        data_section.append(line)
        return ''.join(data_section)

    def _generate_displacements_section(self):
        data_section = []
        for part in self.displacements:
            data_section += [displacement._generate_jobdata(f'{part}-1', node)
                             for node, displacement in self.displacements[part].items()]
        return '\n'.join(data_section)

    def _generate_loads_section(self):
        data_section = []
        if self.gravity:
            data_section.append(self._gravity._generate_jobdata())
        for part in self.loads:
            data_section += [load._generate_jobdata(f'{part}-1', nodes)
                             for load, nodes in self.loads[part].items()]
        return '\n'.join(data_section)

    def _generate_output_section(self):
        # TODO check restart option
        data_section = ["**\n"
                        "*Restart, write, frequency=0\n"
                        "**"]

        if self._field_outputs:
            for foutput in self._field_outputs.values():
                data_section.append(foutput._generate_jobdata())
        if self._history_outputs:
            for houtput in self._history_outputs.values():
                data_section.append(houtput._generate_jobdata())
        data_section.append('*End Step\n')

        return '\n'.join(data_section)


# TODO fix also the steps below
class GeneralStaticRiksStep(GeneralStaticCaseBase):

    def __init__(self, name, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False):
        super(GeneralStaticRiksStep).__init__(name, max_increments, initial_inc_size, min_inc_size, time)
        raise NotImplementedError


class StaticLinearPertubationStep(StaticLinearPerturbationCaseBase):
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

    def __init__(self, name, nlgeom=False):
        super(StaticLinearPertubationStep, self).__init__(name)

        self.__name__ = 'StaticPerturbationStep'
        # TODO this depends on the previous step -> loop through the steps order and adjust this parameter
        self._nlgeom = 'NO' if not nlgeom else 'YES'
        self._stype = 'Static'

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """

        return ("** ----------------------------------------------------------------\n"
                "**\n"
                "** STEP: {0}\n"
                "**\n"
                "*Step, name={0}, nlgeom={1}, perturbation\n"
                "*{2}\n"
                "**\n").format(self._name, self._nlgeom, self._stype)


class BuckleStep(StaticLinearPerturbationCaseBase):

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

    def __init__(self, name, nmodes):
        super(BuckleStep).__init__(name)
        raise NotImplementedError
#         self.__name__      = 'BuckleStep'
#         self.name          = name
#         self.nlgeom        = 'NO'  #TODO this depends on the previous step -> loop through the steps order and adjust this parameter
#         self.displacements = displacements
#         self.loads         = loads
#         self.attr_list.extend(['displacements', 'loads'])
#         self.type = 'Buckle'
    # def _generate_jobdata(self):
    #     """Generates the string information for the input file.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     input file data line (str).
    #     """
#         return """** ----------------------------------------------------------------
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

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return ("** ----------------------------------------------------------------\n"
                "**\n"
                "** STEP: {0}\n"
                "**\n"
                "* Step, name={0}\n"
                "*FREQUENCY, EIGENSOLVER=LANCZOS, NORMALIZATION=DISPLACEMENT\n"
                "{1}\n"
                "*END STEP").format(self.name, self.modes)


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
