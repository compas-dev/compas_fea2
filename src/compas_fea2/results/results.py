from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

from compas.geometry import Vector
from compas.geometry import sum_vectors


class Results(FEAData):
    """Results object. This ensures that the results from all
    the backends are consistent.

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
    def steps(self):
        return self._steps

    def add_step_results(self, step_results):
        # type: (StepResults) -> StepResults
        """Adds a :class:`compas_fea2.results.StepResults` to the Results.

        Parameters
        ----------
        step_resutls : :class:`compas_fea2.results.StepResults`

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

    def extract_data(self, *args, **kwargs):
        raise NotImplementedError("this function is not available for the selected backend")


class StepResults(FEAData):
    """Results object for a single step.

    Parameters
    ----------
    step : :class:`compas_fea2.problem._Step`
        The analysis step.
    model : :class:`compas_fea2.model.Model`
        Copy of the original model. This is used to store the results and to
        generate the deformed shape.

    """

    def __init__(self, step, model, name=None):
        super(StepResults, self).__init__(name=name)
        self._step = step
        self._model = model

    @property
    def step(self):
        return self._step

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    # TODO add moments
    def get_total_reactions(self):
        reactions_forces = []
        for part in self.model.parts:
            for node in part.nodes:
                if 'RF' in node.results[self.step.name]:
                    x, y, z = node.results[self.step.name]['RF']
                    vector = Vector(x=x,
                                    y=y,
                                    z=z)
                    if vector.length == 0:
                        continue
                    reactions_forces.append(vector)
        return sum_vectors(reactions_forces)

    def get_forces_at_interface(self, interface, side='master'):
        faces_group = getattr(interface, side)
        node_force_dict = {}
        for node in faces_group.nodes:
            if 'NFORC1' in node.results[self.step.name]:
                vector = Vector(x=node.results[self.step.name]['NFORC1'][0],
                                y=node.results[self.step.name]['NFORC2'][0],
                                z=node.results[self.step.name]['NFORC3'][0])
                node_force_dict[node] = vector
        return node_force_dict

    def get_resultant_force_at_interface(self, interface, side='master'):
        # NOTE this is valid only for planar interfaces
        # FIXME this is an approximation because it accounts only for the vertical components of the forces
        from compas.geometry import centroid_points_weighted, centroid_points
        from compas.geometry import sum_vectors
        from compas.geometry import Point
        node_force_dict = self.get_forces_at_interface(interface, side=side)
        vector = sum_vectors([v for v in node_force_dict.values()])
        vector = Vector(*vector)
        pt = centroid_points([node.xyz for node in node_force_dict.keys()])
        pt_x = centroid_points_weighted(points=[[node.x, 0., 0.] for node in node_force_dict.keys()],
                                        weights=[v.z for v in node_force_dict.values()])
        pt_y = centroid_points_weighted(points=[[0., node.y, 0.] for node in node_force_dict.keys()],
                                        weights=[v.z for v in node_force_dict.values()])
        pt_z = centroid_points_weighted(points=[[0., 0., node.z] for node in node_force_dict.keys()],
                                        weights=[v.z for v in node_force_dict.values()])
        # pt = [n.x * v.x / vector.length for n, v in node_force_dict.items()]
        # return [pt_x[0], pt_y[1], pt_z[2]], vector
        return (pt_x[0], pt_y[1], pt_z[2]), vector

    def get_deformed_model(self, scale):
        # TODO copy model first
        for part in self.model.parts:
            for node in part.nodes:
                x, y, z = node.results[self.step.name]['U']
                node.x += x*scale
                node.y += y*scale
                node.z += z*scale
        return self.model
