
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.problem import GeneralStaticCase
from compas_fea2.problem import StaticLinearPerturbationCase
from compas_fea2.problem import HeatCase
from compas_fea2.problem import ModalCase
from compas_fea2.problem import HarmonicCase
from compas_fea2.problem import BucklingCase
from compas_fea2.problem import AcousticCase


class LinearStaticStep(LinearStaticStep):
    """Abaqus implementation of the :class:`LinearStaticStep`.\n
    """
    __doc__ += LinearStaticStep.__doc__

    def __init__(self, name):
        super(LinearStaticStep, self).__init__(name)

    def _generate_jobdata(self, problem):
        return """#
# {0}
#
#
timeSeries Constant {1} -factor 1.0
pattern Plain {1} {1} -fact 1 {{
{2}
}}""".format(self.name, problem.steps_order.index(self.name), '\n'.join([load._generate_jobdata() for load in self.loads]))
