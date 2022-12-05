from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

from compas.geometry import Vector
from compas.geometry import sum_vectors


class Results(FEAData):
    """Results object. This ensures that the results from all
    the backends are consistent.

    Note
    ----
    Results are registered to a :class:`compas_fea2.problem.Problem`.

    Parameters
    ----------
    database_name : str
        name of the backend database containing the results
    database_path : str
        path to the backend database containing the results
    fields : list
        Data fields requested.
    steps : set(:class:`compas_fea2.results.StepResults)
        The results for each step

    """

    def __init__(self, *, database_path, database_name):
        super(Results, self).__init__()
        self.database_name = database_name
        self.database_path = database_path
        self._steps = set()

    @property
    def problem(self):
        return self._registration

    @property
    def steps(self):
        return self._steps

    def add_step_results(self, step_results):
        # type: (StepResults) -> StepResults
        """Adds a :class:`compas_fea2.results.StepResults` to the Results.

        Parameters
        ----------
        step_results : :class:`compas_fea2.results.StepResults`

        Returns
        -------
        :class:`compas_fea2.results.StepResults`

        Raises
        ------
        TypeError
            If the step_results is not valid.

        """
        if not isinstance(step_results, StepResults):
            raise TypeError("{!r} is not valid.".format(step_results))
        self._steps.add(step_results)
        return step_results
    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Extract results
    # ==========================================================================

    def to_file(self, *args, **kwargs):
        raise NotImplementedError("this function is not available for the selected backend")


class StepResults(FEAData):
    """Results object for a single step.

    Note
    ----
    StepResults are registered to a :class:`compas_fea2.problem.Step`.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step.
    model : :class:`compas_fea2.model.Model`
        Copy of the original model. This is used to store the results and to
        generate the deformed shape.

    """

    def __init__(self, name=None, **kwargs):
        super(StepResults, self).__init__(name=name, **kwargs)

    @property
    def step(self):
        return self._registration

    @property
    def problem(self):
        return self.step_registration

    @property
    def model(self):
        return self.problem._registration

    def _copy_results_in_model(self, results, fields=None):
        """Copy the results for the step in the model object at the nodal and
        element level.

        Parameters
        ----------
        database_path : _type_
            _description_
        database_name : _type_
            _description_
        file_format : str, optional
            _description_, by default 'pkl'
        fields : _type_, optional
            Fields results to save, by default `None` (all available fields are saved)
        """
        step_results = results[self.step.name]

        # Get part results
        for part_name, part_results in step_results:
            # Get node/element results
            for result_type, node_elements_results in part_results.items():
                if result_type not in ['nodes', 'elements']:
                    continue
                node_elements = getattr(self.model.find_part_by_name(part_name, casefold=True), result_type)
                # Get field results
                for key, res_field in node_elements_results.items():
                    if not fields or res_field in fields:
                        node_element = list(filter(lambda n_e: n_e.key == int(key), node_elements))[0]
                        node_element._results.setdefault(self.problem, {})[self.step] = res_field

    # TODO add moments
    def get_total_reaction(self):
        reactions_forces = []
        for part in self.step.problem.model.parts:
            for node in part.nodes:
                rf = node.results[[self.problem]][self.step].get('RF', None)
                if rf:
                    x, y, z = rf
                    vector = Vector(x=x,
                                    y=y,
                                    z=z)
                    if vector.length == 0:
                        continue
                    reactions_forces.append(vector)
        return sum_vectors(reactions_forces)

    def get_total_moment(self):
        raise NotImplementedError()

    def get_deformed_model(self, scale, **kwargs):
        from compas.geometry import distance_point_point_sqrd
        # TODO copy model first
        for part in self.step.problem.model.parts:
            for node in part.nodes:
                original_node = node.xyz
                x, y, z = node.results[self.step.name]['U']
                node.x += x*scale
                node.y += y*scale
                node.z += z*scale

        return self.model
