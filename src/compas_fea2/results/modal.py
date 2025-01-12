from compas_fea2.base import FEAData
from .fields import FieldResults
from .fields import DisplacementResult
from .results import Result
import numpy as np

# from typing import Iterable


class ModalAnalysisResult(Result):
    def __init__(self, mode, eigenvalue, eigenvector, **kwargs):
        super(ModalAnalysisResult, self).__init__(mode, **kwargs)
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
        return self._eigenvalue

    @property
    def omega(self):
        return np.sqrt(self._eigenvalue)

    @property
    def period(self):
        return 2 * np.pi / self.omega

    @property
    def eigenvector(self):
        return self._eigenvector

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


class ModalAnalysisResults(FEAData):
    def __init__(self, step, **kwargs):
        super(ModalAnalysisResults, self).__init__(**kwargs)
        self._registration = step
        self._eigenvalues = None
        self._eigenvectors = None
        self._eigenvalues_table = step.problem.results_db.get_table("eigenvalues")
        self._eigenvalues_table = step.problem.results_db.get_table("eigenvectors")
        self._components_names = ["dof_1", "dof_2", "dof_3", "dof_4", "dof_5", "dof_6"]

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step.problem

    @property
    def model(self):
        return self.problem.model

    @property
    def rdb(self):
        return self.problem.results_db

    @property
    def components_names(self):
        return self._components_names

    def get_results(self, mode, members, steps, field_name, results_func, results_class, **kwargs):
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
        members_keys = set([member.input_key for member in members])
        parts_names = set([member.part.name for member in members])
        steps_names = set([step.name for step in steps])

        columns = ["step", "part", "input_key"] + self._components_names
        filters = {"input_key": members_keys, "part": parts_names, "step": steps_names, "mode": set([mode for _ in members])}

        results_set = self.rdb.get_rows(field_name, columns, filters)

        results = {}
        for r in results_set:
            step = self.problem.find_step_by_name(r[0])
            results.setdefault(step, [])
            part = self.model.find_part_by_name(r[1]) or self.model.find_part_by_name(r[1], casefold=True)
            if not part:
                raise ValueError(f"Part {r[1]} not in model")
            m = getattr(part, results_func)(r[2])
            results[step].append(results_class(m, *r[3:]))
        return self._to_result(results_set)


class ModalShape(FieldResults):
    """Displacement field results.

    This class handles the displacement field results from a finite element analysis.

    problem : :class:`compas_fea2.problem.Problem`
        The Problem where the Step is registered.

    Attributes
    ----------
    components_names : list of str
        Names of the displacement components.
    invariants_names : list of str
        Names of the invariants of the displacement field.
    results_class : class
        The class used to instantiate the displacement results.
    results_func : str
        The function used to find nodes by key.
    """

    def __init__(self, step, mode, *args, **kwargs):
        super(ModalShape, self).__init__(step=step, field_name="eigenvectors", *args, **kwargs)
        self._components_names = ["dof_1", "dof_2", "dof_3", "dof_4", "dof_5", "dof_6"]
        self._invariants_names = ["magnitude"]
        self._results_class = DisplacementResult
        self._results_func = "find_node_by_key"
        self.mode = mode

    def results(self, step):
        nodes = self.model.nodes
        return self._get_results_from_db(nodes, step=step, mode=self.mode)[step]
