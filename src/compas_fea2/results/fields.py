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
        return self.problem.results_db

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

        results_set = self.rdb.get_rows(self.field_name, ["step", "part", "key"] + columns, filters, func)

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

    def create_sql_table(self, connection, results):
        """
        Delegate the table creation to the ResultsDatabase class.
        """
        ResultsDatabase.create_table_for_output_class(self, connection, results)


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

        return resultant_vector, moment_vector, resultant_location

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
    """Stress field results for 2D elements.

    This class handles the stress field results for 2D elements from a finite element analysis.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step where the results are defined.

    Attributes
    ----------
    components_names : list of str
        Names of the stress components.
    results_func : str
        The function used to find elements by key.
    """

    def __init__(self, step, *args, **kwargs):
        super(StressFieldResults, self).__init__(step=step, *args, **kwargs)
        self._results_func = "find_element_by_key"
        self._field_name = "s"

    @property
    def components_names(self):
        return ["sxx", "syy", "sxy", "szz", "syz", "szx"]

    @property
    def field_name(self):
        return self._field_name

    @property
    def results_func(self):
        return self._results_func

    def global_stresses(self, plane="mid"):
        """Stress field in global coordinates.

        Parameters
        ----------
        plane : str, optional
            The plane to retrieve the stress field for, by default "mid".

        Returns
        -------
        numpy.ndarray
            The stress tensor defined at each location of the field in global coordinates.
        """
        n_locations = len(self.results)
        new_frame = Frame.worldXY()

        # Initialize tensors and rotation_matrices arrays
        tensors = np.zeros((n_locations, 3, 3))
        rotation_matrices = np.zeros((n_locations, 3, 3))

        from_change_of_basis = Transformation.from_change_of_basis
        np_array = np.array

        for i, r in enumerate(self.results):
            r = r.plane_results(plane)
            tensors[i] = r.local_stress
            rotation_matrices[i] = np_array(from_change_of_basis(r.element.frame, new_frame).matrix)[:3, :3]

        # Perform the tensor transformation using numpy's batch matrix multiplication
        transformed_tensors = rotation_matrices @ tensors @ rotation_matrices.transpose(0, 2, 1)

        return transformed_tensors

    def principal_components(self, plane):
        """Compute the eigenvalues and eigenvectors of the stress field at each location.

        Parameters
        ----------
        plane : str
            The plane to retrieve the principal components for.

        Returns
        -------
        tuple(numpy.ndarray, numpy.ndarray)
            The eigenvalues and the eigenvectors, not ordered.
        """
        return np.linalg.eig(self.global_stresses(plane))

    def principal_components_vectors(self, plane):
        """Compute the principal components of the stress field at each location as vectors.

        Parameters
        ----------
        plane : str
            The plane to retrieve the principal components for.

        Yields
        ------
        list(:class:`compas.geometry.Vector`)
            List with the vectors corresponding to max, mid and min principal components.
        """
        eigenvalues, eigenvectors = self.principal_components(plane=plane)
        sorted_indices = np.argsort(eigenvalues, axis=1)
        sorted_eigenvalues = np.take_along_axis(eigenvalues, sorted_indices, axis=1)
        sorted_eigenvectors = np.take_along_axis(eigenvectors, sorted_indices[:, np.newaxis, :], axis=2)
        for i in range(eigenvalues.shape[0]):
            yield [Vector(*sorted_eigenvectors[i, :, j]) * sorted_eigenvalues[i, j] for j in range(eigenvalues.shape[1])]

    def vonmieses(self, plane):
        """Compute the von Mises stress field at each location.

        Parameters
        ----------
        plane : str
            The plane to retrieve the von Mises stress for.

        Yields
        ------
        float
            The von Mises stress at each location.
        """
        for r in self.plane_results:
            r = r.plane_results(plane)
            yield r.von_mises_stress
