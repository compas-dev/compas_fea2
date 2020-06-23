
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._core import StepBase
from compas_fea2.backends._core import GeneralStepBase
from compas_fea2.backends._core import HeatStepBase
from compas_fea2.backends._core import ModalStepBase
from compas_fea2.backends._core import HarmonicStepBase
from compas_fea2.backends._core import BucklingStepBase
from compas_fea2.backends._core import AcousticStepBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'GeneralStep',
    # 'HeatStepBase',
    'ModalStep',
    'HarmoniStepBase',
    'BucklingStep',
    'AcoustiStepBase'
]


# TODO add field and history output requrests
def _generate_data(obj):
    section_data = []
    line = """** ----------------------------------------------------------------
**
** STEP: {0}
**
* Step, name={0}, nlgeom={1}, inc={2}
*{3}
{4}, {5}, {6}, {7}
**
** BOUNDARY CONDITIONS
**\n""".format(obj.name, obj.nlgeom, obj.increments, obj.stype,
            obj.int_incr, obj.full_time, obj.min_incr, obj.max_incr)
    section_data.append(line)

    for displacement in obj.displacements:
        section_data.append(displacement.data)

    line = """**\n** LOADS\n**"""
    section_data.append(line)

    for load in obj.loads:
        section_data.append(load.data)

    line = """**
** OUTPUT REQUESTS
**
*Restart, write, frquency=0
**
** FIELD OUTPUT: F-Output-1
**
*Output, field, variable=PRESELECT
**
** HISTORY OUTPUT: H-Output-1
**
*Output, history, variable=PRESELECT
*End Step\n"""

    section_data.append(line)

    return ''.join(section_data)

class GeneralStep(GeneralStepBase):

    def __init__(self, name, increments, iterations, tolerance, factor, nlgeom, nlmat, displacements, loads, stype, modify):
        super(GeneralStep, self).__init__(name, increments, iterations, tolerance, factor, nlgeom, nlmat, displacements, loads, stype, modify)
        self.data = _generate_data(self)


class HeatStep(HeatStepBase):
    pass
    # def __init__(self, name, interaction, increments, temp0, dTmax, type, duration):
    #     super(HeatStep, self).__init__(name, interaction, increments, temp0, dTmax, type, duration)


class ModalStep(ModalStepBase):
    pass
    # def __init__(self, name, modes, increments, displacements, type):
    #     super(ModalStep, self).__init__(name, modes, increments, displacements, type)


class HarmoniStepBase(HarmonicStepBase):
    pass
    # def __init__(self, name, freq_list, displacements, loads, factor, damping, type):
    #     super(HarmoniStepBase, self).__init__(name, freq_list, displacements, loads, factor, damping, type)


class BucklingStep(BucklingStepBase):
    pass
    # def __init__(self, name, modes, increments, factor, displacements, loads, type,step):
    #     super(BucklingStep, self).__init__(name, modes, increments, factor, displacements, loads, type, step)


class AcoustiStepBase(AcousticStepBase):
    pass
    # def __init__(self, name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type):
    #     super(AcoustiStepBase, self).__init__(name, freq_range, freq_step, displacements, loads, sources, samples, factor, damping, type)
