from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .step import Step


class _Perturbation(Step):
    """A perturbation is a change of the state of the structure after an analysis
    step. Differently from Steps, perturbations' changes are not carried over to
    the next step.

    Parameters
    ----------
    Step : _type_
        _description_
    """

    def __init__(self, **kwargs):
        super(_Perturbation, self).__init__(**kwargs)


class ModalAnalysis(_Perturbation):
    """Perform a modal analysis of the Model from the resulting state after an
    analysis Step.

    Parameters
    ----------
    name : str
        Name of the ModalStep.
    modes : int
        Number of modes to analyse.

    """

    def __init__(self, modes=1, **kwargs):
        super(ModalAnalysis, self).__init__(**kwargs)
        self.modes = modes


class ComplexEigenValue(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError


class BucklingAnalysis(_Perturbation):
    """"""

    def __init__(self, modes, vectors=None, iterations=30, algorithm=None, **kwargs):
        super().__init__(**kwargs)
        self._modes = modes
        self._vectors = vectors or self._compute_vectors(modes)
        self._iterations = iterations
        self._algorithm = algorithm

    def _compute_vectors(self, modes):
        self._vectors = modes * 2
        if modes > 9:
            self._vectors += modes

    @staticmethod
    def Lanczos(modes):
        return BucklingAnalysis(modes=modes, vectors=None, algorithhm="Lanczos")

    @staticmethod
    def Subspace(
        modes,
        iterations,
        vectors=None,
    ):
        return BucklingAnalysis(
            modes=modes,
            vectors=vectors,
            iterations=iterations,
            algorithhm="Subspace",
        )


class LinearStaticPerturbation(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError


class StedyStateDynamic(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError


class SubstructureGeneration(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError
