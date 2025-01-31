# from .results import Result
import numpy as np

from compas_fea2.base import FEAData

from .fields import NodeFieldResults


class ModalAnalysisResult(FEAData):
    """Modal analysis result.

    Parameters
    ----------
    mode : int
        Mode number.
    eigenvalue : float
        Eigenvalue.
    eigenvector : list
        List of DisplacementResult objects.

    Attributes
    ----------
    mode : int
        Mode number.
    eigenvalue : float
        Eigenvalue.
    frequency : float
        Frequency of the mode.
    omega : float
        Angular frequency of the mode.
    period : float
        Period of the mode.
    eigenvector : list
        List of DisplacementResult objects.
    """

    _field_name = "eigen"
    _results_func = "find_node_by_key"
    _components_names = ["x", "y", "z", "xx", "yy", "zz"]
    _invariants_names = ["magnitude"]

    def __init__(self, *, step, mode, eigenvalue, eigenvector, **kwargs):
        super(ModalAnalysisResult, self).__init__(**kwargs)
        self.step = step
        self._mode = mode
        self._eigenvalue = eigenvalue
        self._eigenvector = eigenvector

    @property
    def mode(self):
        return self._mode

    @property
    def eigenvalue(self):
        return self._eigenvalue

    @property
    def frequency(self):
        return self.omega / (2 * np.pi)

    @property
    def omega(self):
        return np.sqrt(self._eigenvalue)

    @property
    def period(self):
        return 1 / self.frequency

    @property
    def eigenvector(self):
        return self._eigenvector

    @property
    def shape(self):
        return ModalShape(step=self.step, results=self._eigenvector)

    def _normalize_eigenvector(self):
        """
        Normalize the eigenvector to obtain the mode shape.
        Mode shapes are typically scaled so the maximum displacement is 1.
        """
        max_val = np.max(np.abs(self._eigenvector))
        return self._eigenvector / max_val if max_val != 0 else self._eigenvector

    def participation_factor(self, mass_matrix):
        """
        Calculate the modal participation factor.
        :param mass_matrix: Global mass matrix.
        :return: Participation factor.
        """
        if len(self.eigenvector) != len(mass_matrix):
            raise ValueError("Eigenvector length must match the mass matrix size")
        return np.dot(self.eigenvector.T, np.dot(mass_matrix, self.eigenvector))

    def modal_contribution(self, force_vector):
        """
        Calculate the contribution of this mode to the global response for a given force vector.
        :param force_vector: External force vector.
        :return: Modal contribution.
        """
        return np.dot(self.eigenvector, force_vector) / self.eigenvalue

    def to_dict(self):
        """
        Export the modal analysis result as a dictionary.
        """
        return {
            "mode": self.mode,
            "eigenvalue": self.eigenvalue,
            "frequency": self.frequency,
            "omega": self.omega,
            "period": self.period,
            "eigenvector": self.eigenvector.tolist(),
            "mode_shape": self.mode_shape.tolist(),
        }

    def to_json(self, filepath):
        import json

        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_csv(self, filepath):
        import csv

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Mode", "Eigenvalue", "Frequency", "Omega", "Period", "Eigenvector", "Mode Shape"])
            writer.writerow([self.mode, self.eigenvalue, self.frequency, self.omega, self.period, ", ".join(map(str, self.eigenvector)), ", ".join(map(str, self.mode_shape))])

    def __repr__(self):
        return f"ModalAnalysisResult(mode={self.mode}, eigenvalue={self.eigenvalue:.4f}, " f"frequency={self.frequency:.4f} Hz, period={self.period:.4f} s)"


class ModalShape(NodeFieldResults):
    """ModalShape result applied as Displacement field.

    Parameters
    ----------
    step : :class:`compas_fea2.problem.Step`
        The analysis step
    results : list
        List of DisplcementResult objects.
    """

    def __init__(self, step, results, *args, **kwargs):
        super(ModalShape, self).__init__(step=step, results_cls=ModalAnalysisResult, *args, **kwargs)
        self._results = results

    @property
    def results(self):
        return self._results

    def _get_results_from_db(self, members=None, columns=None, filters=None, **kwargs):
        raise NotImplementedError("this method is not applicable for ModalShape results")

    def get_result_at(self, location):
        raise NotImplementedError("this method is not applicable for ModalShape results")

    def get_max_result(self, component):
        raise NotImplementedError("this method is not applicable for ModalShape results")

    def get_min_result(self, component):
        raise NotImplementedError("this method is not applicable for ModalShape results")

    def get_max_component(self, component):
        raise NotImplementedError("this method is not applicable for ModalShape results")

    def get_min_component(self, component):
        raise NotImplementedError("this method is not applicable for ModalShape results")

    def get_limits_component(self, component):
        raise NotImplementedError("this method is not applicable for ModalShape results")

    def get_limits_absolute(self):
        raise NotImplementedError("this method is not applicable for ModalShape results")
