from typing import Iterable

import numpy as np
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Vector

from compas_fea2.base import FEAData

from .results import AccelerationResult
from .results import DisplacementResult
from .results import ReactionResult
from .results import ShellStressResult
from .results import SolidStressResult
from .results import VelocityResult
from .results import SectionForcesResult


class FieldResults(FEAData):
    """FieldResults object. This is a collection of Result objects that define a field.

    The objects uses SQLite queries to efficiently retrieve the results from the results database.

    The field results are defined over multiple steps

    You can use FieldResults to visualise a field over a part or the model, or to compute
    global quantiies, such as maximum or minimum values.

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
    model : :class:`compas_fea2.problem.Model
        The Model where the Step is registered.
    db_connection : :class:`sqlite3.Connection` | None
        Connection object or None
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.

    Notes
    -----
    FieldResults are registered to a :class:`compas_fea2.problem.Step`.

    """

    def __init__(self, step, field_name, *args, **kwargs):
        super(FieldResults, self).__init__(*args, **kwargs)
        self._registration = step
        self._field_name = field_name
        # self._table = step.problem.results_db.get_table(field_name)
        self._components_names = None
        self._invariants_names = None
        self._restuls_func = None

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step.problem

    @property
    def field_name(self):
        return self._field_name

    @property
    def model(self):
        return self.problem.model

    @property
    def rdb(self):
        return self.problem.results_db

    @property
    def results(self):
        return self._get_results_from_db(step=self.step, columns=self._components_names)[self.step]

    def _get_results_from_db(self, members=None, columns=None, filters=None, **kwargs):
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
        if not filters:
            filters = {}

        filters["step"] = [self.step.name]

        if members:
            if not isinstance(members, Iterable):
                members = [members]
            filters["key"] = set([member.key for member in members])
            filters["part"] = set([member.part.name for member in members])

        results_set = self.rdb.get_rows(self._field_name, ["step", "part", "key"] + self._components_names, filters)

        return self.rdb.to_result(results_set, self._results_class, self._restuls_func)

    def get_result_at(self, location):
        """Get the result for a given member and step.

        Parameters
        ----------
        member : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self._get_results_from_db(location, self.step)[self.step][0]

    def get_max_result(self, component):
        """Get the result where a component is maximum for a given step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        :class:`compas_fea2.results.Result`
            The appriate Result object.
        """
        results_set = self.rdb.get_func_row(self.field_name, self.field_name + str(component), "MAX", {"step": [self.step.name]}, self.results_columns)
        return self.rdb.to_result(results_set)[self.step][0]

    def get_min_result(self, component):
        results_set = self.rdb.get_func_row(self.field_name, self.field_name + str(component), "MIN", {"step": [self.step.name]}, self.results_columns)
        return self.rdb.to_result(results_set, self._results_class)[self.step][0]

    def get_max_component(self, component):
        """Get the result where a component is maximum for a given step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        :class:`compas_fea2.results.Result`
            The appriate Result object.
        """
        return self.get_max_result(component, self.step).vector[component - 1]

    def get_min_component(self, component):
        """Get the result where a component is minimum for a given step.

        Parameters
        ----------
        component : _type_
            _description_
        step : _type_
            _description_

        Returns
        -------
        :class:`compas_fea2.results.Result`
            The appropriate Result object.
        """
        return self.get_min_result(component, self.step).vector[component - 1]

    def get_limits_component(self, component):
        """Get the result objects with the min and max value of a given
        component in a step.

        Parameters
        ----------
        component : int
            The index of the component to retrieve (e.g., 0 for the first component).
        step : :class:`compas_fea2.problem.Step`
            The analysis step where the results are defined.

        Returns
        -------
        list
            A list containing the result objects with the minimum and maximum value of the given component in the step.
        """
        return [self.get_min_result(component, self.step), self.get_max_result(component, self.step)]

    def get_limits_absolute(self):
        limits = []
        for func in ["MIN", "MAX"]:
            limits.append(self.rdb.get_func_row(self.field_name, "magnitude", func, {"step": [self.step.name]}, self.results_columns))
        return [self.rdb.to_result(limit)[self.step][0] for limit in limits]

    @property
    def locations(self):
        """Return the locations where the field is defined.

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step, by default None

        Yields
        ------
        :class:`compas.geometry.Point`
            The location where the field is defined.
        """
        for r in self.results:
            yield r.location

    @property
    def points(self):
        """Return the locations where the field is defined.

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step, by default None

        Yields
        ------
        :class:`compas.geometry.Point`
            The location where the field is defined.
        """
        for r in self.results:
            yield r.location

    @property
    def vectors(self):
        """Return the locations where the field is defined.

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step, by default None

        Yields
        ------
        :class:`compas.geometry.Point`
            The location where the field is defined.
        """
        for r in self.results:
            yield r.vector

    def component(self, dof=None):
        """Return the locations where the field is defined.

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step, by default None

        Yields
        ------
        :class:`compas.geometry.Point`
            The location where the field is defined.
        """
        for r in self.results:
            if dof is None:
                yield r.vector.magnitude
            else:
                yield r.vector[dof]


class DisplacementFieldResults(FieldResults):
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

    def __init__(self, step, *args, **kwargs):
        super(DisplacementFieldResults, self).__init__(step=step, field_name="u", *args, **kwargs)
        self._components_names = ["ux", "uy", "uz", "uxx", "uyy", "uzz"]
        self._invariants_names = ["magnitude"]
        self._results_class = DisplacementResult
        self._restuls_func = "find_node_by_key"


class AccelerationFieldResults(FieldResults):
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

    def __init__(self, step, *args, **kwargs):
        super(AccelerationFieldResults, self).__init__(problem=step, field_name="a", *args, **kwargs)
        self._components_names = ["ax", "ay", "az", "axx", "ayy", "azz"]
        self._invariants_names = ["magnitude"]
        self._results_class = AccelerationResult
        self._restuls_func = "find_node_by_key"


class VelocityFieldResults(FieldResults):
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

    def __init__(self, step, *args, **kwargs):
        super(VelocityFieldResults, self).__init__(problem=step, field_name="v", *args, **kwargs)
        self._components_names = ["vx", "vy", "vz", "vxx", "vyy", "vzz"]
        self._invariants_names = ["magnitude"]
        self._results_class = VelocityResult
        self._restuls_func = "find_node_by_key"


class ReactionFieldResults(FieldResults):
    """Reaction field.

    Parameters
    ----------
    problem : :class:`compas_fea2.problem.Problem`
        The Problem where the Step is registered.
    """

    def __init__(self, step, *args, **kwargs):
        super(ReactionFieldResults, self).__init__(step=step, field_name="rf", *args, **kwargs)
        self._components_names = ["rfx", "rfy", "rfz", "rfxx", "rfyy", "rfzz"]
        self._invariants_names = ["magnitude"]
        self._results_class = ReactionResult
        self._restuls_func = "find_node_by_key"


class StressFieldResults(FieldResults):
    """_summary_

    Parameters
    ----------
    FieldResults : _type_
        _description_
    """

    def __init__(self, step, *args, **kwargs):
        super(StressFieldResults, self).__init__(step=step, field_name="s2d", *args, **kwargs)
        self._components_names = ["s11", "s22", "s12", "m11", "m22", "m12"]
        # self._components_names_2d = ["s11", "s22", "s12", "m11", "m22", "m12"]
        self._components_names_3d = ["s11", "s22", "s23", "s12", "s13", "s33"]
        self._field_name_2d = "s2d"
        self._field_name_3d = "s3d"
        self._results_class = ShellStressResult
        # self._results_class_2d = ShellStressResult
        self._results_class_3d = SolidStressResult
        self._restuls_func = "find_element_by_key"

    @property
    def global_stresses(self):
        """Stress field in global coordinates

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step, by default None


        Returns
        -------
        numpy array
            The stress tensor defined at each location of the field in
            global coordinates.
        """
        n_locations = len(self.results)
        new_frame = Frame.worldXY()

        # Initialize tensors and rotation_matrices arrays
        tensors = np.zeros((n_locations, 3, 3))
        rotation_matrices = np.zeros((n_locations, 3, 3))

        from_change_of_basis = Transformation.from_change_of_basis
        np_array = np.array

        for i, r in enumerate(self.results):
            tensors[i] = r.local_stress
            rotation_matrices[i] = np_array(from_change_of_basis(r.element.frame, new_frame).matrix)[:3, :3]

        # Perform the tensor transformation using numpy's batch matrix multiplication
        transformed_tensors = rotation_matrices @ tensors @ rotation_matrices.transpose(0, 2, 1)

        return transformed_tensors

    @property
    def principal_components(self):
        """Compute the eigenvalues and eigenvetors of the stress field at each location.

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step in which the stress filed is defined. If not
            provided, the last analysis step is used.

        Returns
        -------
        touple(np.array, np.array)
            The eigenvalues and the eigenvectors, not ordered.
        """
        return np.linalg.eig(self.global_stresses)

    @property
    def principal_components_vectors(self):
        """Compute the principal components of the stress field at each location
        as vectors.

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step in which the stress filed is defined. If not
            provided, the last analysis step is used.


        Yields
        ------
        list(:class:`compas.geometry.Vector)
            list with the vectors corresponding to max, mid and min principal componets.
        """
        eigenvalues, eigenvectors = self.principal_components
        sorted_indices = np.argsort(eigenvalues, axis=1)
        sorted_eigenvalues = np.take_along_axis(eigenvalues, sorted_indices, axis=1)
        sorted_eigenvectors = np.take_along_axis(eigenvectors, sorted_indices[:, np.newaxis, :], axis=2)
        for i in range(eigenvalues.shape[0]):
            yield [Vector(*sorted_eigenvectors[i, :, j]) * sorted_eigenvalues[i, j] for j in range(eigenvalues.shape[1])]

    def vonmieses(self):
        """Compute the principal components of the stress field at each location
        as vectors.

        Parameters
        ----------
        step : :class:`compas_fea2.problem.steps.Step`, optional
            The analysis step in which the stress filed is defined. If not
            provided, the last analysis step is used.


        Yields
        ------
        list(:class:`compas.geometry.Vector)
            list with the vectors corresponding to max, mid and min principal componets.
        """
        for r in self.results:
            yield r.von_mises_stress


class SectionForcesFieldResults(FieldResults):
    """_summary_

    Parameters
    ----------
    FieldResults : _type_
        _description_
    """

    def __init__(self, step, *args, **kwargs):
        super(SectionForcesFieldResults, self).__init__(step=step, field_name="sf", *args, **kwargs)
        self._components_names = ["Fx_1", "Fy_1", "Fz_1", "Mx_1", "My_1", "Mz_1", "Fx_2", "Fy_2", "Fz_2", "Mx_2", "My_2", "Mz_2"]
        self._invariants_names = ["magnitude"]
        self._results_class = SectionForcesResult
        self._restuls_func = "find_element_by_key"

    def get_element_forces(self, element):
        """_summary_

        Parameters
        ----------
        element : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        return self.get_result_at(element)

    def get_elements_forces(self, elements):
        """
        Get the section forces for a given element.

        Parameters
        ----------
        element : Element
            The element for which to retrieve section forces.

        Returns
        -------
        SectionForcesResult
            The section forces result for the specified element.
        """
        for element in elements:
            yield self.get_element_forces(element)

    def get_all_section_forces(self):
        """
        Retrieve section forces for all elements in the field.

        Returns
        -------
        dict
            A dictionary mapping elements to their section forces.
        """
        return {element: self.get_result_at(element) for element in self.elements}

    def filter_by_component(self, component_name, threshold=None):
        """
        Filter results by a specific component, optionally using a threshold.

        Parameters
        ----------
        component_name : str
            The name of the component to filter by (e.g., "Fx_1").
        threshold : float, optional
            A threshold value to filter results. Only results above this value are included.

        Returns
        -------
        dict
            A dictionary of filtered elements and their results.
        """
        if component_name not in self._components_names:
            raise ValueError(f"Component '{component_name}' is not valid. Choose from {self._components_names}.")

        filtered_results = {}
        for element, result in self.get_all_section_forces().items():
            component_value = getattr(result, component_name, None)
            if component_value is not None and (threshold is None or component_value >= threshold):
                filtered_results[element] = result

        return filtered_results

    def export_to_dict(self):
        """
        Export all field results to a dictionary.

        Returns
        -------
        dict
            A dictionary containing all section force results.
        """
        results_dict = {}
        for element, result in self.get_all_section_forces().items():
            results_dict[element] = {
                "forces": {
                    "Fx_1": result.force_vector_1.x,
                    "Fy_1": result.force_vector_1.y,
                    "Fz_1": result.force_vector_1.z,
                    "Fx_2": result.force_vector_2.x,
                    "Fy_2": result.force_vector_2.y,
                    "Fz_2": result.force_vector_2.z,
                },
                "moments": {
                    "Mx_1": result.moment_vector_1.x,
                    "My_1": result.moment_vector_1.y,
                    "Mz_1": result.moment_vector_1.z,
                    "Mx_2": result.moment_vector_2.x,
                    "My_2": result.moment_vector_2.y,
                    "Mz_2": result.moment_vector_2.z,
                },
                "invariants": {
                    "magnitude": result.net_force.length,
                },
            }
        return results_dict

    def export_to_csv(self, file_path):
        """
        Export all field results to a CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file.
        """
        import csv

        with open(file_path, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write headers
            writer.writerow(["Element", "Fx_1", "Fy_1", "Fz_1", "Mx_1", "My_1", "Mz_1", "Fx_2", "Fy_2", "Fz_2", "Mx_2", "My_2", "Mz_2", "Magnitude"])
            # Write results
            for element, result in self.get_all_section_forces().items():
                writer.writerow(
                    [
                        element,
                        result.force_vector_1.x,
                        result.force_vector_1.y,
                        result.force_vector_1.z,
                        result.moment_vector_1.x,
                        result.moment_vector_1.y,
                        result.moment_vector_1.z,
                        result.force_vector_2.x,
                        result.force_vector_2.y,
                        result.force_vector_2.z,
                        result.moment_vector_2.x,
                        result.moment_vector_2.y,
                        result.moment_vector_2.z,
                        result.net_force.length,
                    ]
                )
