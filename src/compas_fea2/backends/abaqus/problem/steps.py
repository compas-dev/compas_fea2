from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import StaticStep
from compas_fea2.problem import GeneralStep
# from compas_fea2.problem import StaticLinearPerturbationCase
# from compas_fea2.problem import HeatCase
# from compas_fea2.problem import ModalCase
# from compas_fea2.problem import HarmonicCase
# from compas_fea2.problem import BucklingCase
# from compas_fea2.problem import AcousticCase

# TODO add field and history output requrests


# class AbaqusGeneralStep(GeneralStep):
#     """
#     Notes
#     -----
#     the data for the input file for this object is generated at runtime.
#     """

#     def __init__(self, max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name=None, **kwargs):
#         super(AbaqusGeneralStep, self).__init__(max_increments, initial_inc_size,
#                                                 min_inc_size, time, nlgeom, modify, name=name, **kwargs)


class AbaqusStaticStep(StaticStep):
    """Abaqus implementation of the :class:`compas_fea2.Proble.StaticStep`.

    Note
    ----
    the data for the input file for this object is generated at runtime.

    """
    __doc__ += StaticStep.__doc__

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(AbaqusStaticStep, self).__init__(max_increments, initial_inc_size,
                                               min_inc_size, time, nlgeom, modify, name=name, **kwargs)
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

        return f"""**
{self._generate_header_section()}**
** - Displacements
**   -------------
{self._generate_displacements_section()}**
** - Loads
**   -----
{self._generate_loads_section()}**
** - Output Requests
**   ---------------
{self._generate_output_section()}**
"""

    def _generate_header_section(self):
        data_section = []
        line = ("** STEP: {0}\n"
                "**\n"
                "*Step, name={0}, nlgeom={1}, inc={2}\n"
                "*{3}\n"
                "{4}, {5}, {6}, {5}\n").format(self._name, self._nlgeom, self._max_increments, self._stype, self._initial_inc_size, self._time, self._min_inc_size)
        data_section.append(line)
        return ''.join(data_section)

    def _generate_displacements_section(self):
        data_section = []
        for part in self.displacements:
            data_section += [displacement._generate_jobdata('{}-1'.format(part.name), node)
                             for node, displacement in self.displacements[part].items()]
        return '\n'.join(data_section)

    def _generate_loads_section(self):
        data_section = []
        if self.gravity:
            data_section.append(self._gravity._generate_jobdata())
        for part in self.loads:
            data_section += [load._generate_jobdata('{}-1'.format(part.name), nodes)
                             for load, nodes in self.loads[part].items()]
        return '\n'.join(data_section)

    def _generate_output_section(self):
        # TODO check restart option
        data_section = ["**",
                        "*Restart, write, frequency=0",
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


class AbaqusStaticRiksStep(StaticStep):

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False):
        super(AbaqusStaticRiksStep).__init__(max_increments, initial_inc_size, min_inc_size, time)
        raise NotImplementedError


# class AbaqusStaticLinearPertubationStep(StaticLinearPerturbationCase):
#     """Initialises the StaticLinearPertubationStep object for use in a static analysis.

#     Parameters
#     ----------
#     name : str
#         Name of the GeneralStep.
#     displacements : list
#         Displacement objects.
#     loads : list
#         Load objects.

#    """
#     __doc__ += StaticLinearPerturbationCase.__doc__

#     def __init__(self, name):
#         super(AbaqusStaticLinearPertubationStep, self).__init__(name)

#         # TODO this depends on the previous step -> loop through the steps order and adjust this parameter
#         self._nlgeom = 'NO'  # if not nlgeom else 'YES'
#         self._stype = 'Static'

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#        Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line(str).
#         """

#         return ("** STEP: {0}\n"
#                 "**\n"
#                 "*Step, name={0}, nlgeom={1}, perturbation\n"
#                 "*{2}\n"
#                 "**\n").format(self._name, self._nlgeom, self._stype)


# class AbaqusBuckleStep(StaticLinearPerturbationCase):
#     """Initialises BuckleStep object for use in a buckling analysis.
#     """

#     def __init__(self, name, nmodes):
#         super(AbaqusBuckleStep).__init__(name)
#         raise NotImplementedError


# class AbaqusHeatStep(HeatCase):

#     def __init__(self, name, interaction, increments, temp0, dTmax, type, duration):
#         super(AbaqusHeatStep, self).__init__(name, interaction, increments, temp0, dTmax, type, duration)
#         raise NotImplementedError


# class AbaqusModalStep(ModalCase):

#     def __init__(self, name, modes):
#         super(AbaqusModalStep, self).__init__(name, modes)

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#        Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line(str).
#         """
#         return ("** ----------------------------------------------------------------\n"
#                 "**\n"
#                 "** STEP: {0}\n"
#                 "**\n"
#                 "* Step, name={0}\n"
#                 "*FREQUENCY, EIGENSOLVER=LANCZOS, NORMALIZATION=DISPLACEMENT\n"
#                 "{1}\n"
#                 "*END STEP").format(self.name, self.modes)


# class AbaqusHarmoniStep(HarmonicStep):

#     def __init__(self, name, freq_list, displacements, loads, factor, damping, type):
#         super(AbaqusHarmoniStep, self).__init__(name, freq_list, displacements, loads, factor, damping, type)
#         raise NotImplementedError


# class AbaqusBucklingStep(BucklingStep):

#     def __init__(self, name, modes, increments, factor, displacements, loads, type, step):
#         super(AbaqusBucklingStep, self).__init__(name, modes, increments, factor, displacements, loads, type, step)
#         raise NotImplementedError


# class AbaqusAcoustiStep(AcousticStep):

#     def __init__(self, name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type):
#         super(AbaqusAcoustiStep, self).__init__(name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type)
#         raise NotImplementedError

# class BuckleStep(StaticLinearPerturbationStep):

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

#     def __init__(self, name, nmodes):
#         super(BuckleStep).__init__(name)
#         raise NotImplementedError
# #         self.__name__      = 'BuckleStep'
# #         self.name          = name
# #         self.nlgeom        = 'NO'  #TODO this depends on the previous step -> loop through the steps order and adjust this parameter
# #         self.displacements = displacements
# #         self.loads         = loads
# #         self.attr_list.extend(['displacements', 'loads'])
# #         self.type = 'Buckle'
#     # def _generate_jobdata(self):
#     #     """Generates the string information for the input file.

#     #     Parameters
#     #     ----------
#     #     None

#     #     Returns
#     #     -------
#     #     input file data line (str).
#     #     """
# #         return """** ----------------------------------------------------------------
# # **
# # ** STEP: {0}
# # **
# # * Step, name={0}, nlgeom={1}, perturbation
# # *{2}
# # **\n""".format(self.name, self.nlgeom, self.stype)
