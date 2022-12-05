from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps.perturbations import BucklingAnalysis
from compas_fea2.problem.steps.perturbations import ComplexEigenValue
from compas_fea2.problem.steps.perturbations import LinearStaticPerturbation
from compas_fea2.problem.steps.perturbations import ModalAnalysis
from compas_fea2.problem.steps.perturbations import StedyStateDynamic
from compas_fea2.problem.steps.perturbations import SubstructureGeneration

class SofistikBucklingAnalysis(BucklingAnalysis):
    """Sofistik implementation of :class:`compas_fea2.problem.steps.perturbations.BucklingAnalysis`.\n
    """
    __doc__ += BucklingAnalysis.__doc__

    def __init__(self, modes, vectors=None, iterations=30, algorithm=None, name=None, **kwargs):
        super(SofistikBucklingAnalysis, self).__init__(modes=modes, vectors=vectors, iterations=iterations, algorithm=algorithm, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikComplexEigenValue(ComplexEigenValue):
    """Sofistik implementation of :class:`compas_fea2.problem.steps.perturbations.ComplexEigenValue`.\n
    """
    __doc__ += ComplexEigenValue.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikComplexEigenValue, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikLinearStaticPerturbation(LinearStaticPerturbation):
    """Sofistik implementation of :class:`compas_fea2.problem.steps.perturbations.LinearStaticPerturbation`.\n
    """
    __doc__ += LinearStaticPerturbation.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikLinearStaticPerturbation, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikModalAnalysis(ModalAnalysis):
    """Sofistik implementation of :class:`compas_fea2.problem.steps.perturbations.ModalAnalysis`.\n
    """
    __doc__ += ModalAnalysis.__doc__

    def __init__(self, modes=1, name=None, **kwargs):
        super(SofistikModalAnalysis, self).__init__(modes=modes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikStedyStateDynamic(StedyStateDynamic):
    """Sofistik implementation of :class:`compas_fea2.problem.steps.perturbations.StedyStateDynamic`.\n
    """
    __doc__ += StedyStateDynamic.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikStedyStateDynamic, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikSubstructureGeneration(SubstructureGeneration):
    """Sofistik implementation of :class:`compas_fea2.problem.steps.perturbations.SubstructureGeneration`.\n
    """
    __doc__ += SubstructureGeneration.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikSubstructureGeneration, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

