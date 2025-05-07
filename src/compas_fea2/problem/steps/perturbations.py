from compas.geometry import Vector
from compas.geometry import sum_vectors

from compas_fea2.results import ModalAnalysisResult
from compas_fea2.UI import FEA2Viewer

from .step import Step


class _Perturbation(Step):
    """A perturbation is a change of the state of the structure after an analysis
    step. Perturbations' changes are not carried over to the next step.
    """

    def __init__(self, **kwargs):
        super(_Perturbation, self).__init__(**kwargs)

    def __data__(self):
        data = super(_Perturbation, self).__data__()
        data.update(
            {
                "type": self.__class__.__name__,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        return cls(**data)


class ModalAnalysis(_Perturbation):
    """Perform a modal analysis of the Model from the resulting state after an
    analysis Step.

    Parameters
    ----------
    modes : int
        Number of modes.

    """

    def __init__(self, modes=1, **kwargs):
        super(ModalAnalysis, self).__init__(**kwargs)
        self.modes = modes

    @property
    def rdb(self):
        return self.problem.rdb

    def _get_results_from_db(self, mode, **kwargs):
        """Get the results for the given members and steps.

        Parameters
        ----------
        members : _type_
            _description_
        steps : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        filters = {}
        filters["step"] = [self.name]
        filters["mode"] = [mode]

        # Get the eigenvalue
        eigenvalue = self.rdb.get_rows("eigenvalues", ["lambda"], filters)[0][0]

        # Get the eiginvectors
        all_columns = ["step", "part", "key", "x", "y", "z", "xx", "yy", "zz"]
        results_set = self.rdb.get_rows("eigenvectors", ["step", "part", "key", "x", "y", "z", "xx", "yy", "zz"], filters)
        results_set = [{k: v for k, v in zip(all_columns, row)} for row in results_set]
        eigenvector = self.rdb.to_result(results_set, "find_node_by_key", "u")[self]

        return eigenvalue, eigenvector

    @property
    def results(self):
        for mode in range(self.modes):
            yield self.mode_result(mode + 1)

    @property
    def frequencies(self):
        for mode in range(self.modes):
            yield self.mode_frequency(mode + 1)

    @property
    def shapes(self):
        for mode in range(self.modes):
            yield self.mode_shape(mode + 1)

    def mode_shape(self, mode):
        return self.mode_result(mode).shape

    def mode_frequency(self, mode):
        return self.mode_result(mode).frequency

    def mode_result(self, mode):
        eigenvalue, eigenvector = self._get_results_from_db(mode)
        return ModalAnalysisResult(step=self, mode=mode, eigenvalue=eigenvalue, eigenvector=eigenvector)

    def show_mode_shape(self, mode, fast=True, opacity=1, scale_results=1, show_bcs=True, show_original=0.25, show_contour=False, show_vectors=False, **kwargs):
        """Show the mode shape of a given mode.

        Parameters
        ----------
        mode : int
            The mode to show.
        fast : bool, optional
            Show the mode shape fast, by default True
        opacity : float, optional
            Opacity of the model, by default 1
        scale_results : float, optional
            Scale the results, by default 1
        show_bcs : bool, optional
            Show the boundary conditions, by default True
        show_original : float, optional
            Show the original model, by default 0.25
        show_contour : bool, optional
            Show the contour, by default False
        show_vectors : bool, optional
            Show the vectors, by default False

        """
        viewer = FEA2Viewer(center=self.model.center, scale_model=1)

        if show_original:
            viewer.add_model(self.model, show_parts=True, fast=True, opacity=show_original, show_bcs=False, **kwargs)

        shape = self.mode_shape(mode)
        if show_vectors:
            viewer.add_mode_shape(shape, fast=fast, show_parts=False, component=None, show_vectors=show_vectors, show_contour=show_contour, **kwargs)

        # TODO create a copy of the model first
        for displacement in shape.results:
            vector = displacement.vector.scaled(scale_results)
            displacement.node.xyz = sum_vectors([Vector(*displacement.location.xyz), vector])

        if show_contour:
            viewer.add_mode_shape(shape, fast=fast, component=None, show_vectors=False, show_contour=show_contour, **kwargs)
        viewer.add_model(self.model, fast=fast, opacity=opacity, show_bcs=show_bcs, **kwargs)
        viewer.show()

    def __data__(self):
        data = super(ModalAnalysis, self).__data__()
        data.update(
            {
                "modes": self.modes,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        return cls(modes=data["modes"], **data)


class ComplexEigenValue(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError

    def __data__(self):
        return super(ComplexEigenValue, self).__data__()

    @classmethod
    def __from_data__(cls, data):
        return cls(**data)


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

    def __data__(self):
        data = super(BucklingAnalysis, self).__data__()
        data.update(
            {
                "modes": self._modes,
                "vectors": self._vectors,
                "iterations": self._iterations,
                "algorithm": self._algorithm,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        return cls(modes=data["_modes"], vectors=data["_vectors"], iterations=data["_iterations"], algorithm=data["_algorithm"], **data)


class LinearStaticPerturbation(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError

    def __data__(self):
        return super(LinearStaticPerturbation, self).__data__()

    @classmethod
    def __from_data__(cls, data):
        return cls(**data)


class SteadyStateDynamic(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError

    def __data__(self):
        return super(SteadyStateDynamic, self).__data__()

    @classmethod
    def __from_data__(cls, data):
        return cls(**data)


class SubstructureGeneration(_Perturbation):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError

    def __data__(self):
        return super(SubstructureGeneration, self).__data__()

    @classmethod
    def __from_data__(cls, data):
        return cls(**data)
