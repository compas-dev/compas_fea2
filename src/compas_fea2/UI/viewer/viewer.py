import os
import numpy as np

from math import sqrt
from typing import Iterable
from compas_view2.app import App
from compas_view2.objects import Collection
from compas_view2.shapes import Arrow
from compas_view2.shapes import Text

from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Polyhedron
from compas.geometry import Vector
from compas.geometry import sum_vectors
from compas.utilities import hex_to_rgb

from compas_fea2.UI.viewer.shapes import PinBCShape
from compas_fea2.UI.viewer.shapes import FixBCShape
from compas_fea2.model.elements import ShellElement
from compas_fea2.model.elements import _Element3D
from compas_fea2.model.elements import BeamElement
from compas_fea2.model.bcs import FixedBC, PinnedBC

from compas_fea2.problem.loads import PointLoad
from compas_fea2.problem.steps import _GeneralStep

from compas_fea2.results import NodeFieldResults

def hextorgb(hex):
    return tuple(i / 255 for i in hex_to_rgb(hex))


class FEA2Viewer:
    """Wrapper for the compas_view2 viewer app.

    Parameters
    ----------
    width : int, optional
        Width of the viewport, by default 800.
    height : int, optional
        Height of the viewport, by default 500.
    scale_factor : float, optional
        Scale the content of the viewport, by default 1.

    Attributes
    ----------
    None
    """

    def __init__(self, obj, **kwargs):

        VIEWER_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config_default.json")
        sf = kwargs.get("scale_factor", 1)
        self.app = App(config=VIEWER_CONFIG_FILE)
        self.obj = obj

        self.app.view.camera.target = [i*sf for i in self.obj.center]
        # V = V1 + t * (V2 - V1) / | V2 - V1 |
        V1 = np.array([0, 0, 0])
        V2 = np.array(self.app.view.camera.target)
        delta = V2 - V1
        length = np.linalg.norm(delta)
        distance = length * 3
        unitSlope = delta / length
        new_position = V1 + unitSlope * distance
        self.app.view.camera.position = new_position.tolist()

        self.app.view.camera.near *= sf
        self.app.view.camera.far *= sf
        self.app.view.camera.scale *= sf
        self.app.view.grid.cell_size *= sf

    def draw_mesh(self, mesh):
        self.app.add(mesh, use_vertex_color=True)

    def draw_nodes(self, nodes=None, node_lables=False):
        """Draw nodes.

        Parameters
        ----------
        nodes : [:class:`compas_fea2.model.Node]
            The nodes to draw.
        node_lables : bool
            If `True` add the nodes.
        """
        if not nodes:
            nodes = self.obj.nodes
        pts = [node.point for node in nodes]
        self.app.add(Collection(pts), facecolor=hextorgb("#386641"))

        if node_lables:
            txts = [Text(str(node.key), node.point, height=35) for node in nodes]
        self.app.add(Collection(txts), facecolor=hextorgb("#386641"))

    def draw_solid_elements(self, elements, show_vertices=True):
        """Draw the elements of a part.

        Parameters
        ----------
        elements : :class:`compas_fea2.model.ShellElement` | :class:`compas_fea2.model._Element3D` | :class:`compas_fea2.model.BeamElement`
            _description_
        show_vertices : bool, optional
            If `True` show the vertices of the elements, by default True

        """
        collection_items = []
        for element in elements:
            pts = [node.point for node in element.nodes]
            collection_items.append(Polyhedron(pts, list(element._face_indices.values())))
        if collection_items:
            self.app.add(Collection(collection_items), facecolor=(0.9, 0.9, 0.9), show_points=show_vertices)

    def draw_shell_elements(self, elements, show_vertices=True):
        """Draw the elements of a part.

        Parameters
        ----------
        elements : :class:`compas_fea2.model.ShellElement` | :class:`compas_fea2.model.Element3D` | :class:`compas_fea2.model.BeamElement`
            _description_
        show_vertices : bool, optional
            If `True` show the vertices of the elements, by default True

        """
        collection_items = []
        for element in elements:
            pts = [node.point for node in element.nodes]
            if len(element.nodes) == 4:
                collection_items.append(Mesh.from_vertices_and_faces(pts, [[1, 2, 3, 0]]))
            elif len(element.nodes) == 3:
                collection_items.append(Mesh.from_vertices_and_faces(pts, [[0, 1, 2]]))
            else:
                raise NotImplementedError("only 3 and 4 vertices shells supported at the moment")
        if collection_items:
            self.app.add(Collection(collection_items), facecolor=(0.9, 0.9, 0.9), show_points=show_vertices)

    def draw_beam_elements(self, elements, show_vertices=True):
        """Draw the elements of a part.

        Parameters
        ----------
        elements :  :class:`compas_fea2.model.BeamElement`
            _description_
        show_vertices : bool, optional
            If `True` show the vertices of the elements, by default True

        """
        collection_items = []
        for element in elements:
            pts = [node.point for node in element.nodes]
            collection_items.append(Line(pts[0], pts[1]))
        if collection_items:
            self.app.add(Collection(collection_items), linewidth=10)

    def draw_bcs(self, model, parts=None, scale_factor=1.0):
        """Draw the support boundary conditions.

        Parameters
        ----------
        model : :class:`compas_fea2.model.Model`
            The model to draw.
        parts : [:class:`compas_fea2.model.DeformablePart`], optional
            List of parts. Only the boundary conditions of the parts in the list
            will be shown. By default `None`, meaning that all the parts will be
            shown.
        scale_factor : float, optional
            Scale the boundary condtions reppresentation to have a nicer drawing,
            by default 1.
        """
        if model.bcs:
            bcs_collection = []
            if not parts:
                parts = model.parts
            for bc, nodes in model.bcs.items():
                for node in nodes:
                    if node.part in parts:
                        if isinstance(bc, PinnedBC):
                            bcs_collection.append(PinBCShape(node.xyz, scale=scale_factor).shape)
                        if isinstance(bc, FixedBC):
                            bcs_collection.append(FixBCShape(node.xyz, scale=scale_factor).shape)
            if bcs_collection:
                self.app.add(Collection(bcs_collection), facecolor=(1, 0, 0), opacity=0.5)

    def draw_nodes_vector(self, pts, vectors, scale_factor=1, colors=None):
        """Draw vector arrows at nodes.

        Parameters
        ----------
        pts : _type_
            _description_
        vectors : _type_
            _description_
        colors : tuple, optional
            _description_, by default (0, 1, 0)
        """
        arrows = []
        arrows_properties = []
        if not colors:
            colors = [(0, 1, 0)] * len(pts)
        for pt, vector, color in zip(pts, vectors, colors):
            arrows.append(Arrow(pt, vector*scale_factor, head_portion=0.3, head_width=0.15, body_width=0.05))
            arrows_properties.append({"u": 3, "show_lines": False, "facecolor": color})
        if arrows:
            self.app.add(Collection(arrows, arrows_properties))

    def draw_loads(self, step, scale_factor=1.0, app_point="end"):
        """Draw the applied loads for given steps.

        Parameters
        ----------
        steps : [:class:`compas_fea2.problem.Step`]
            List of steps. Only the loads in these steps will be shown.
        scale_factor : float, optional
            Scale the loads reppresentation to have a nicer drawing,
            by default 1.
        """
        if isinstance(step, _GeneralStep):
            for pattern in step._patterns:
                if isinstance(pattern.load, PointLoad):
                    vector = Vector(
                        x=pattern.load.components["x"] or 0.0,
                        y=pattern.load.components["y"] or 0.0,
                        z=pattern.load.components["z"] or 0.0,
                    )
                    if vector.length == 0:
                        continue
                    vector.scale(scale_factor)
                    if app_point == "end":
                        pts = [
                            [node.x - vector.x, node.y - vector.y, node.z - vector.z] for node in pattern.distribution
                        ]
                    else:
                        pts = [node.point for node in pattern.distribution]
                    # TODO add moment components xx, yy, zz
                    vectors = [vector] * len(pts)
                    self.draw_nodes_vector(pts, vectors)
                else:
                    print("WARNING! Only point loads are currently supported!")

    def draw_reactions(self, step=None, scale_factor=1, colors=None, **kwargs):
        """Draw the reaction forces as vector arrows at nodes.

        Parameters
        ----------
        pts : _type_
            _description_
        vectors : _type_
            _description_
        colors : tuple, optional
            _description_, by default (0, 1, 0)
        """
        if not step:
            step = self.steps_order[-1]

        reactions = NodeFieldResults('RF', step)
        # min_value = reactions._min_components["magnitude"].components[f"MIN({'magnitude'})"]
        # max_value = reactions._max_components["magnitude"].components[f"MAX({'magnitude'})"]
        locations = []
        vectors = []
        for r in reactions.results:
            locations.append(r.location.xyz)
            vectors.append(r.vector)
        self.draw_nodes_vector(locations, vectors, scale_factor=scale_factor, colors=colors)

    def draw_deformed(self, step=None, scale_factor=1.0, **kwargs):
        """Display the structure in its deformed configuration.

        Parameters
        ----------
        step : :class:`compas_fea2.problem._Step`, optional
            The Step of the analysis, by default None. If not provided, the last
            step is used.

        Returns
        -------
        None

        """

        # TODO create a copy of the model first
        displacements = NodeFieldResults("U", step)
        for displacement in displacements.results:
            vector = displacement.vector.scaled(scale_factor)
            displacement.location.xyz = sum_vectors([Vector(*displacement.location.xyz), vector])

        for part in self.model.parts:
            self.draw_beam_elements(part.elements_by_dimension(dimension=1), show_vertices=False)
            self.draw_shell_elements(part.elements_by_dimension(dimension=2), show_vertices=False)
            self.draw_solid_elements(part.elements_by_dimension(dimension=3), show_vertices=False)


    def show(self):
        """Display the viewport."""
        self.app.show()

    def dynamic_show(self):
        """Display the viewport dynamically."""
        self.app.run()
