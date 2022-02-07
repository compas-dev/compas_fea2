
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.problem import GeneralStaticCaseBase
from compas_fea2.problem import StaticLinearPerturbationCaseBase
from compas_fea2.problem import HeatCaseBase
from compas_fea2.problem import ModalCaseBase
from compas_fea2.problem import HarmonicCaseBase
from compas_fea2.problem import BucklingCaseBase
from compas_fea2.problem import AcousticCaseBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'GeneralStaticStep',
    # 'StaticLinearPertubationStep',
    # # 'HeatStepBase',
    # 'ModalStep',
    # 'HarmoniStepBase',
    # 'BucklingStep',
    # 'AcoustiStepBase'
]


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

    def __init__(self, name):
        super(StaticLinearPertubationStep, self).__init__(name)

    def _generate_jobdata(self, problem):
        return """#
# {0}
#
#
timeSeries Constant {1} -factor 1.0
pattern Plain {1} {1} -fact 1 {{
{2}
}}""".format(self.name, problem.steps_order.index(self.name), '\n'.join([load._generate_jobdata() for load in self.loads]))
