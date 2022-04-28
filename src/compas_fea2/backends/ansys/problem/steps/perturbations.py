from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps.perturbations import BucklingAnalysis
from compas_fea2.problem.steps.perturbations import ComplexEigenValue
from compas_fea2.problem.steps.perturbations import LinearStaticPerturbation
from compas_fea2.problem.steps.perturbations import ModalAnalysis
from compas_fea2.problem.steps.perturbations import StedyStateDynamic
from compas_fea2.problem.steps.perturbations import SubstructureGeneration

class AnsysBucklingAnalysis(BucklingAnalysis):
    """Ansys implementation of :class:`compas_fea2.problem.steps.perturbations.BucklingAnalysis`.\n
    """
    __doc__ += BucklingAnalysis.__doc__

    def __init__(self, modes, vectors=None, iterations=30, algorithm=None, name=None, **kwargs):
        super(AnsysBucklingAnalysis, self).__init__(modes=modes, vectors=vectors, iterations=iterations, algorithm=algorithm, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysComplexEigenValue(ComplexEigenValue):
    """Ansys implementation of :class:`compas_fea2.problem.steps.perturbations.ComplexEigenValue`.\n
    """
    __doc__ += ComplexEigenValue.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysComplexEigenValue, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysLinearStaticPerturbation(LinearStaticPerturbation):
    """Ansys implementation of :class:`compas_fea2.problem.steps.perturbations.LinearStaticPerturbation`.\n
    """
    __doc__ += LinearStaticPerturbation.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysLinearStaticPerturbation, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysModalAnalysis(ModalAnalysis):
    """Ansys implementation of :class:`compas_fea2.problem.steps.perturbations.ModalAnalysis`.\n
    """
    __doc__ += ModalAnalysis.__doc__

    def __init__(self, modes=1, name=None, **kwargs):
        super(AnsysModalAnalysis, self).__init__(modes=modes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysStedyStateDynamic(StedyStateDynamic):
    """Ansys implementation of :class:`compas_fea2.problem.steps.perturbations.StedyStateDynamic`.\n
    """
    __doc__ += StedyStateDynamic.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysStedyStateDynamic, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysSubstructureGeneration(SubstructureGeneration):
    """Ansys implementation of :class:`compas_fea2.problem.steps.perturbations.SubstructureGeneration`.\n
    """
    __doc__ += SubstructureGeneration.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysSubstructureGeneration, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

