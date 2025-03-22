from typing import Iterable

import numpy as np
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Vector

from compas_fea2.base import FEAData

from .results import AccelerationResult  # noqa: F401
from .results import DisplacementResult  # noqa: F401
from .results import ReactionResult  # noqa: F401
from .results import SectionForcesResult  # noqa: F401
from .results import ShellStressResult  # noqa: F401
from .results import SolidStressResult  # noqa: F401
from .results import VelocityResult  # noqa: F401
from .database import ResultsDatabase  # noqa: F401
from itertools import groupby


class FieldResults(FEAData):
    """FieldResults object. This is a collection of Result objects that define a field.

    The objects use SQLite queries to efficiently retrieve the results from the results database.

    The field results are defined over multiple steps.

    You can use FieldResults to visualize a field over a part or the model, or to compute
    global quantities, such as maximum or minimum values.

    Parameters
    ----------
    field_name : str
        Name of the field.
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    field_name : str
        Name of the field.
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.
    problem : :class:`compas_fea2.problem.Problem`
        The Problem where the Step is registered.
    model : :class:`compas_fea2.problem.Model`
        The Model where the Step is registered.
    db_connection : :class:`sqlite3.Connection` | None
        Connection object or None.
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.

    Notes
    -----
    FieldResults are registered to a :class:`compas_fea2.problem.Step`.
    """

    def __init__(self, step, *args, **kwargs):
        super(FieldResults, self).__init__(*args, **kwargs)
        self._registration = step

    @property
    def sqltable_schema(self):
        fields = []
        predefined_fields = [
            ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
            ("key", "INTEGER"),
            ("step", "TEXT"),
            ("part", "TEXT"),
        ]

        fields.extend(predefined_fields)

        for comp in self.components_names:
            fields.append((comp, "REAL"))
        return {
            "table_name": self.field_name,
            "columns": fields,
        }

    @property
    def step(self) -> "Step":
        return self._registration

    @property
    def problem(self) -> "Problem":
        return self.step.problem

    @property
    def model(self) -> "Model":
        return self.problem.model

    @property
    def field_name(self) -> str:
        raise NotImplementedError("This method should be implemented in the subclass.")

    @property
    def results_func(self) -> str:
        raise NotImplementedError("This method should be implemented in the subclass.")

    @property
    def rdb(self) -> ResultsDatabase:
        return self.problem.rdb

    @property
    def results(self) -> list:
        return self._get_results_from_db(columns=self.components_names)[self.step]

    @property
    def results_sorted(self) -> list:
        return sorted(self.results, key=lambda x: x.key)

    @property
    def locations(self) -> Iterable:
        """Return the locations where the field is defined.

        Yields
        ------
        :class:`compas.geometry.Point`
            The location where the field is defined.
        """
        for r in self.results:
            yield r.location

    def _get_results_from_db(self, members=None, columns=None, filters=None, func=None, **kwargs):
        """Get the results for the given members and steps.

        Parameters
        ----------
        members : list, optional
            List of members to filter results.
        columns : list, optional
            List of columns to retrieve.
        filters : dict, optional
            Dictionary of filters to apply.

        Returns
        -------
        dict
            Dictionary of results.
        """
        if not columns:
            columns = self.components_names

        if not filters:
            filters = {}

        filters["step"] = [self.step.name]

        if members:
            if not isinstance(members, Iterable):
                members = [members]
            filters["key"] = set([member.key for member in members])
            filters["part"] = set([member.part.name for member in members])

        all_columns = ["step", "part", "key"] + columns

        results_set = self.rdb.get_rows(self.field_name, all_columns, filters, func)
        results_set = [{k: v for k, v in zip(all_columns, row)} for row in results_set]

        return self.rdb.to_result(results_set, results_func=self.results_func, field_name=self.field_name, **kwargs)

    def get_result_at(self, location):
        """Get the result for a given location.

        Parameters
        ----------
        location : object
            The location to retrieve the result for.

        Returns
        -------
        object
            The result at the given location.
        """
        return self._get_results_from_db(members=location, columns=self.components_names)[self.step][0]

    def get_max_result(self, component):
        """Get the result where a component is maximum for a given step.

        Parameters
        ----------
        component : str
            The component to retrieve the maximum result for.

        Returns
        -------
        :class:`compas_fea2.results.Result`
            The appropriate Result object.
        """
        func = ["DESC", component]
        return self._get_results_from_db(columns=self.components_names, func=func)[self.step][0]

    def get_min_result(self, component):
        """Get the result where a component is minimum for a given step.

        Parameters
        ----------
        component : str
            The component to retrieve the minimum result for.

        Returns
        -------
        :class:`compas_fea2.results.Result`
            The appropriate Result object.
        """
        func = ["ASC", component]
        return self._get_results_from_db(columns=self.components_names, func=func)[self.step][0]

    def get_limits_component(self, component):
        """Get the result objects with the min and max value of a given component in a step.

        Parameters
        ----------
        component : int
            The index of the component to retrieve.

        Returns
        -------
        list
            A list containing the result objects with the minimum and maximum value of the given component in the step.
        """
        return [self.get_min_result(component, self.step), self.get_max_result(component, self.step)]

    def component_scalar(self, component):
        """Return the value of selected component."""
        for result in self.results:
            yield getattr(result, component, None)

    def filter_by_component(self, component, threshold=None):
        """Filter results by a specific component, optionally using a threshold.

        Parameters
        ----------
        componen : str
            The name of the component to filter by (e.g., "Fx_1").
        threshold : float, optional
            A threshold value to filter results. Only results above this value are included.

        Returns
        -------
        dict
            A dictionary of filtered elements and their results.
        """
        if component not in self.components_names:
            raise ValueError(f"Component '{component}' is not valid. Choose from {self.components_names}.")

        for result in self.results:
            component_value = getattr(result, component, None)
            if component_value is not None and (threshold is None or component_value >= threshold):
                yield result


# ------------------------------------------------------------------------------
# Node Field Results
# ------------------------------------------------------------------------------
class NodeFieldResults(FieldResults):
    """Node field results.

    This class handles the node field results from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    components_names : list of str
        Names of the node components.
    invariants_names : list of str
        Names of the invariants of the node field.
    results_class : class
        The class used to instantiate the node results.
    results_func : str
        The function used to find nodes by key.
    """

    def __init__(self, step, *args, **kwargs):
        super(NodeFieldResults, self).__init__(step=step, *args, **kwargs)
        self._results_func = "find_node_by_key"

    @property
    def components_names(self):
        return ["x", "y", "z", "rx", "ry", "rz"]

    @property
    def field_name(self):
        return self._field_name

    @property
    def results_func(self):
        return self._results_func

    @property
    def vectors(self):
        """Return the vectors where the field is defined.

        Yields
        ------
        :class:`compas.geometry.Vector`
            The vector where the field is defined.
        """
        for r in self.results:
            yield r.vector

    @property
    def vectors_rotation(self):
        """Return the vectors where the field is defined.

        Yields
        ------
        :class:`compas.geometry.Vector`
            The vector where the field is defined.
        """
        for r in self.results:
            yield r.vector_rotation

    def compute_resultant(self, sub_set=None):
        """Compute the translation resultant, moment resultant, and location of the field.

        Parameters
        ----------
        sub_set : list, optional
            List of locations to filter the results. If None, all results are considered.

        Returns
        -------
        tuple
            The translation resultant as :class:`compas.geometry.Vector`, moment resultant as :class:`compas.geometry.Vector`, and location as a :class:`compas.geometry.Point`.
        """
        from compas.geometry import Point
        from compas.geometry import centroid_points_weighted
        from compas.geometry import cross_vectors
        from compas.geometry import sum_vectors

        results_subset = list(filter(lambda x: x.location in sub_set, self.results)) if sub_set else self.results
        vectors = [r.vector for r in results_subset]
        locations = [r.location.xyz for r in results_subset]
        resultant_location = Point(*centroid_points_weighted(locations, [v.length for v in vectors]))
        resultant_vector = sum_vectors(vectors)
        moment_vector = sum_vectors(cross_vectors(Vector(*loc) - resultant_location, vec) for loc, vec in zip(locations, vectors))

        return Vector(*resultant_vector), Vector(*moment_vector), resultant_location

    def components_vectors(self, components):
        """Return a vector representing the given components."""
        for vector in self.vectors:
            v_copy = vector.copy()
            for c in ["x", "y", "z"]:
                if c not in components:
                    setattr(v_copy, c, 0)
            yield v_copy

    def components_vectors_rotation(self, components):
        """Return a vector representing the given components."""
        for vector in self.results.vectors_rotation:
            v_copy = vector.copy()
            for c in ["x", "y", "z"]:
                if c not in components:
                    setattr(v_copy, c, 0)
            yield v_copy


class DisplacementFieldResults(NodeFieldResults):
    """Displacement field results.

    This class handles the displacement field results from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

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

    def __init__(self, step, *args, **kwargs):
        super(DisplacementFieldResults, self).__init__(step=step, *args, **kwargs)
        self._field_name = "u"


class AccelerationFieldResults(NodeFieldResults):
    """Acceleration field results.

    This class handles the acceleration field results from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    components_names : list of str
        Names of the acceleration components.
    invariants_names : list of str
        Names of the invariants of the acceleration field.
    results_class : class
        The class used to instantiate the acceleration results.
    results_func : str
        The function used to find nodes by key.
    """

    def __init__(self, step, *args, **kwargs):
        super(AccelerationFieldResults, self).__init__(step=step, *args, **kwargs)
        self._field_name = "a"


class VelocityFieldResults(NodeFieldResults):
    """Velocity field results.

    This class handles the velocity field results from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    components_names : list of str
        Names of the velocity components.
    invariants_names : list of str
        Names of the invariants of the velocity field.
    results_class : class
        The class used to instantiate the velocity results.
    results_func : str
        The function used to find nodes by key.
    """

    def __init__(self, step, *args, **kwargs):
        super(VelocityFieldResults, self).__init__(step=step, *args, **kwargs)
        self._field_name = "v"


class ReactionFieldResults(NodeFieldResults):
    """Reaction field results.

    This class handles the reaction field results from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    components_names : list of str
        Names of the reaction components.
    invariants_names : list of str
        Names of the invariants of the reaction field.
    results_class : class
        The class used to instantiate the reaction results.
    results_func : str
        The function used to find nodes by key.
    """

    def __init__(self, step, *args, **kwargs):
        super(ReactionFieldResults, self).__init__(step=step, *args, **kwargs)
        self._field_name = "rf"


class ContactForcesFieldResults(NodeFieldResults):
    """Reaction field results.

    This class handles the reaction field results from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    components_names : list of str
        Names of the reaction components.
    invariants_names : list of str
        Names of the invariants of the reaction field.
    results_class : class
        The class used to instantiate the reaction results.
    results_func : str
        The function used to find nodes by key.
    """

    def __init__(self, step, *args, **kwargs):
        super().__init__(step=step, *args, **kwargs)
        self._field_name = "c"


# ------------------------------------------------------------------------------
# Section Forces Field Results
# ------------------------------------------------------------------------------
class ElementFieldResults(FieldResults):
    """Element field results.

    This class handles the element field results from a finite element analysis.
    """

    def __init__(self, step, *args, **kwargs):
        super(ElementFieldResults, self).__init__(step=step, *args, **kwargs)
        self._results_func = "find_element_by_key"


class SectionForcesFieldResults(ElementFieldResults):
    """Section forces field results.

    This class handles the section forces field results from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    components_names : list of str
        Names of the section forces components.
    invariants_names : list of str
        Names of the invariants of the section forces field.
    results_class : class
        The class used to instantiate the section forces results.
    results_func : str
        The function used to find elements by key.
    """

    def __init__(self, step, *args, **kwargs):
        super(SectionForcesFieldResults, self).__init__(step=step, *args, **kwargs)
        self._results_func = "find_element_by_key"
        self._field_name = "sf"

    @property
    def field_name(self):
        return self._field_name

    @property
    def results_func(self):
        return self._results_func

    @property
    def components_names(self):
        return ["Fx1", "Fy1", "Fz1", "Mx1", "My1", "Mz1", "Fx2", "Fy2", "Fz2", "Mx2", "My2", "Mz2"]

    def get_element_forces(self, element):
        """Get the section forces for a given element.

        Parameters
        ----------
        element : object
            The element to retrieve the section forces for.

        Returns
        -------
        object
            The section forces result for the specified element.
        """
        return self.get_result_at(element)

    def get_elements_forces(self, elements):
        """Get the section forces for a list of elements.

        Parameters
        ----------
        elements : list
            The elements to retrieve the section forces for.

        Yields
        ------
        object
            The section forces result for each element.
        """
        for element in elements:
            yield self.get_element_forces(element)

    def export_to_dict(self):
        """Export all field results to a dictionary.

        Returns
        -------
        dict
            A dictionary containing all section force results.
        """
        raise NotImplementedError()

    def export_to_csv(self, file_path):
        """Export all field results to a CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file.
        """
        raise NotImplementedError()


# ------------------------------------------------------------------------------
# Stress Field Results
# ------------------------------------------------------------------------------


class StressFieldResults(ElementFieldResults):
    """
    Generalized stress field results for both 2D and 3D elements.
    Stress results are computed in the global coordinate system.
    Operations on stress results are performed on the field level to improve efficiency.
    """

    def __init__(self, step, *args, **kwargs):
        super().__init__(step=step, *args, **kwargs)
        self._results_func = "find_element_by_key"
        self._field_name = "s"

    @property
    def grouped_results(self):
        """Groups elements by their dimensionality (2D or 3D) correctly."""
        sorted_results = sorted(self.results, key=lambda r: r.element.ndim)  # Ensure sorting before grouping
        return {k: list(v) for k, v in groupby(sorted_results, key=lambda r: r.element.ndim)}

    @property
    def field_name(self):
        return self._field_name

    @property
    def results_func(self):
        return self._results_func

    @property
    def components_names(self):
        return ["s11", "s22", "s33", "s12", "s23", "s13"]

    @property
    def invariants_names(self):
        return ["von_mises_stress", "principal_stress_min", "principal_stress_mid", "principal_stress_max"]

    def get_component_value(self, component, **kwargs):
        """Return the value of the selected component."""
        if component not in self.components_names:
            for result in self.results:
                yield getattr(result, component, None)
        else:
            raise (ValueError(f"Component '{component}' is not valid. Choose from {self.components_names}."))

    def get_invariant_value(self, invariant, **kwargs):
        """Return the value of the selected invariant."""
        if invariant not in self.invariants_names:
            for result in self.results:
                yield getattr(result, invariant, None)
        else:
            raise (ValueError(f"Invariant '{invariant}' is not valid. Choose from {self.invariants_names}."))

    def global_stresses(self, plane="mid"):
        """Compute stress tensors in the global coordinate system."""
        new_frame = Frame.worldXY()
        transformed_tensors = []

        grouped_results = self.grouped_results

        # Process 2D elements
        if 2 in grouped_results:
            results_2d = grouped_results[2]
            local_stresses_2d = np.array([r.plane_results(plane).local_stress for r in results_2d])

            # Zero out out-of-plane components
            local_stresses_2d[:, 2, :] = 0.0
            local_stresses_2d[:, :, 2] = 0.0

            # Compute transformation matrices
            rotation_matrices_2d = np.array([Transformation.from_change_of_basis(r.element.frame, new_frame).matrix[:3, :3] for r in results_2d])

            # Apply tensor transformation
            transformed_tensors.append(np.einsum("nij,njk,nlk->nil", rotation_matrices_2d, local_stresses_2d, rotation_matrices_2d))

        # Process 3D elements
        if 3 in grouped_results:
            results_3d = grouped_results[3]
            local_stresses_3d = np.array([r.local_stress for r in results_3d])
            transformed_tensors.append(local_stresses_3d)

        if not transformed_tensors:
            return np.empty((0, 3, 3))

        return np.concatenate(transformed_tensors, axis=0)

    def average_stress_at_nodes(self, component="von_mises_stress"):
        """
        Compute the nodal average of von Mises stress using efficient NumPy operations.

        Returns
        -------
        np.ndarray
            (N_nodes,) array containing the averaged von Mises stress per node.
        """
        # Compute von Mises stress at element level
        element_von_mises = self.von_mises_stress()  # Shape: (N_elements,)

        # Extract all node indices in a single operation
        node_indices = np.array([n.key for e in self.results for n in e.element.nodes])  # Shape (N_total_entries,)

        # Repeat von Mises stress for each node in the corresponding element
        repeated_von_mises = np.repeat(element_von_mises, repeats=[len(e.element.nodes) for e in self.results], axis=0)  # Shape (N_total_entries,)

        # Get the number of unique nodes
        max_node_index = node_indices.max() + 1

        # Initialize accumulators for sum and count
        nodal_stress_sum = np.zeros(max_node_index)  # Summed von Mises stresses
        nodal_counts = np.zeros(max_node_index)  # Count occurrences per node

        # Accumulate stresses and counts at each node
        np.add.at(nodal_stress_sum, node_indices, repeated_von_mises)
        np.add.at(nodal_counts, node_indices, 1)

        # Prevent division by zero
        nodal_counts[nodal_counts == 0] = 1

        # Compute final nodal von Mises stress average
        nodal_avg_von_mises = nodal_stress_sum / nodal_counts

        return nodal_avg_von_mises  # Shape: (N_nodes,)

    def average_stress_tensor_at_nodes(self):
        """
        Compute the nodal average of the full stress tensor.

        Returns
        -------
        np.ndarray
            (N_nodes, 3, 3) array containing the averaged stress tensor per node.
        """
        # Compute global stress tensor at the element level
        element_stresses = self.global_stresses()  # Shape: (N_elements, 3, 3)

        # Extract all node indices in a single operation
        node_indices = np.array([n.key for e in self.results for n in e.element.nodes])  # Shape (N_total_entries,)

        # Repeat stress tensors for each node in the corresponding element
        repeated_stresses = np.repeat(element_stresses, repeats=[len(e.element.nodes) for e in self.results], axis=0)  # Shape (N_total_entries, 3, 3)

        # Get the number of unique nodes
        max_node_index = node_indices.max() + 1

        # Initialize accumulators for sum and count
        nodal_stress_sum = np.zeros((max_node_index, 3, 3))  # Summed stress tensors
        nodal_counts = np.zeros((max_node_index, 1, 1))  # Count occurrences per node

        # Accumulate stresses and counts at each node
        np.add.at(nodal_stress_sum, node_indices, repeated_stresses)
        np.add.at(nodal_counts, node_indices, 1)

        # Prevent division by zero
        nodal_counts[nodal_counts == 0] = 1

        # Compute final nodal stress tensor average
        nodal_avg_stress = nodal_stress_sum / nodal_counts

        return nodal_avg_stress  # Shape: (N_nodes, 3, 3)

    def von_mises_stress(self, plane="mid"):
        """
        Compute von Mises stress for 2D and 3D elements.

        Returns
        -------
        np.ndarray
            Von Mises stress values per element.
        """
        stress_tensors = self.global_stresses(plane)  # Shape: (N_elements, 3, 3)

        # Extract stress components
        S11, S22, S33 = stress_tensors[:, 0, 0], stress_tensors[:, 1, 1], stress_tensors[:, 2, 2]
        S12, S23, S13 = stress_tensors[:, 0, 1], stress_tensors[:, 1, 2], stress_tensors[:, 0, 2]

        # Compute von Mises stress
        sigma_vm = np.sqrt(0.5 * ((S11 - S22) ** 2 + (S22 - S33) ** 2 + (S33 - S11) ** 2 + 6 * (S12**2 + S23**2 + S13**2)))

        return sigma_vm

    def principal_components(self, plane="mid"):
        """
        Compute sorted principal stresses and directions.

        Returns
        -------
        tuple
            (principal_stresses, principal_directions)
            - `principal_stresses`: (N_elements, 3) array containing sorted principal stresses.
            - `principal_directions`: (N_elements, 3, 3) array containing corresponding eigenvectors.
        """
        stress_tensors = self.global_stresses(plane)  # Shape: (N_elements, 3, 3)

        # **✅ Ensure symmetry (avoiding numerical instability)**
        stress_tensors = 0.5 * (stress_tensors + np.transpose(stress_tensors, (0, 2, 1)))

        # **✅ Compute eigenvalues and eigenvectors (batch operation)**
        eigvals, eigvecs = np.linalg.eigh(stress_tensors)

        # **✅ Sort eigenvalues & corresponding eigenvectors (by absolute magnitude)**
        sorted_indices = np.argsort(np.abs(eigvals), axis=1)  # Sort based on absolute value
        sorted_eigvals = np.take_along_axis(eigvals, sorted_indices, axis=1)
        sorted_eigvecs = np.take_along_axis(eigvecs, sorted_indices[:, :, None], axis=2)

        # **✅ Ensure consistent orientation**
        reference_vector = np.array([1.0, 0.0, 0.0])  # Arbitrary reference vector
        alignment_check = np.einsum("nij,j->ni", sorted_eigvecs, reference_vector)  # Dot product with reference
        flip_mask = alignment_check < 0  # Identify vectors needing flipping
        sorted_eigvecs[flip_mask] *= -1  # Flip incorrectly oriented eigenvectors

        return sorted_eigvals, sorted_eigvecs
