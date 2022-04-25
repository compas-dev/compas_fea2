from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import ModalAnalysis
from compas_fea2.problem.steps import BucklingAnalysis
from compas_fea2.problem.steps import ComplexEigenValue
from compas_fea2.problem.steps import LinearStaticPerturbation
from compas_fea2.problem.steps import StedyStateDynamic
from compas_fea2.problem.steps import SubstructureGeneration


class OpenseesModalAnalysis(ModalAnalysis):
    """"""
    __doc__ += ModalAnalysis.__doc__

    def __init__(self, modes=1, name=None, **kwargs):
        super(OpenseesModalAnalysis, self).__init__(modes, name=name, **kwargs)
        raise NotImplementedError()
    # def _generate_jobdata(self):
    #     'timeSeries Constant {0} -factor 1.0'.format(s_index)
    #     'pattern Plain {0} {0} -fact {1} {2}'.format(s_index, 1, '{')


class OpenseesComplexEigenValue(ComplexEigenValue):
    """"""
    __doc__ += ComplexEigenValue.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesComplexEigenValue, self).__init__(name, **kwargs)
        raise NotImplementedError()


class OpenseesBucklingAnalysis(BucklingAnalysis):
    """"""
    __doc__ += BucklingAnalysis.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesBucklingAnalysis, self).__init__(name, **kwargs)
        raise NotImplementedError()


class OpenseesLinearStaticPerturbation(LinearStaticPerturbation):
    """"""
    __doc__ += LinearStaticPerturbation.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesLinearStaticPerturbation, self).__init__(name=name, **kwargs)
        raise NotImplementedError()


class OpenseesStedyStateDynamic(StedyStateDynamic):
    """"""
    __doc__ += StedyStateDynamic.__doc__

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        raise NotImplementedError()


class OpenseesSubstructureGeneration(SubstructureGeneration):
    """"""
    __doc__ += SubstructureGeneration.__doc__

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        raise NotImplementedError()
