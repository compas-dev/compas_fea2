from importlib.metadata import distribution
import os
from typing import Iterable
from compas_view2.app import App
from compas_view2.objects import Collection
from compas_view2.shapes import Arrow
from compas_view2.collections import Collection
from compas_view2.shapes import Text

from compas.datastructures import Mesh
from compas.geometry import Scale
from compas.geometry import Point
from compas.geometry import Cone
from compas.geometry import Circle
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Box
from compas.geometry import Polyhedron
from compas.geometry import Vector
from compas.utilities import hex_to_rgb
from compas.colors import Color

from compas_fea2.UI.viewer.shapes import PinBCShape
from compas_fea2.UI.viewer.shapes import FixBCShape
from compas_fea2.model.elements import ShellElement
from compas_fea2.model.elements import _Element3D
from compas_fea2.model.elements import BeamElement
from compas_fea2.model.constraints import _Constraint
from compas_fea2.model.bcs import FixedBC, PinnedBC

from compas_fea2.problem.loads import GravityLoad, PointLoad
from compas_fea2.problem.steps import _GeneralStep

from compas_fea2.utilities._utils import _compute_model_dimensions


def hextorgb(hex):
    return tuple(i / 255 for i in hex_to_rgb(hex))


class FEA2Viewer():
    """Wrapper for the compas_view2 viewer app.

    Parameters
    ----------
    width : int, optional
        Width of the viewport, by default 800.
    height : int, optional
        Height of the viewport, by default 500.
    scale_factor : float, optional
        Scale the content of the viewport, by default 1.
    """

    def __init__(self, width=800, height=500, **kwargs):
        self.width = width
        self.height = height
        self.app = App(width=width, height=height)

        self.app.view.camera.target = [3000, 3000, 100]
        self.app.view.camera.position = [7000, 7000, 5000]
        self.app.view.camera.near = 1
        self.app.view.camera.far = 100000
        self.app.view.camera.scale = 1000
        self.app.view.grid.cell_size = 1000

    def _scale_mesh(self, mesh):
        S = Scale.from_factors([self.scale_factor]*3)
        mesh.transform(S)
        return mesh

    def draw_mesh(self, mesh):
        self.app.add(mesh, use_vertex_color=True)

    def draw_parts(self, parts, draw_nodes=False, node_labels=False, solid=False):
        """Draw the parts.

        Parameters
        ----------
        parts : :class:`compas_fea2.model.DeformablePart` | [:class:`compas_fea2.model.DeformablePart`]
            The part or parts to draw.
        draw_nodes : bool, optional
            if `True` draw the nodes of the part, by default False
        node_labels : bool, optional
            if `True` add the node lables, by default False
        draw_envelope : bool, optional
            if `True` draw the outer boundary of the part, by default False
        solid : bool, optional
            if `True` draw all the elements (also the internal ones) of the part
            otherwise just show the boundary faces, by default True
        """
        parts = parts if isinstance(parts, Iterable) else [parts]
        for part in parts:
            if solid:
                self.draw_solid_elements(filter(lambda x: isinstance(x, _Element3D), part.elements), draw_nodes)
            else:
                if part.discretized_boundary_mesh:
                    self.app.add(part.discretized_boundary_mesh, use_vertex_color=True)
            self.draw_shell_elements(filter(lambda x: isinstance(x, ShellElement), part.elements), draw_nodes)
            self.draw_beam_elements(filter(lambda x: isinstance(x, BeamElement), part.elements), draw_nodes)
            if draw_nodes:
                self.draw_nodes(part.nodes, node_labels)

    def draw_nodes(self, nodes, node_lables):
        """Draw nodes.

        Parameters
        ----------
        nodes : [:class:`compas_fea2.model.Node]
            The nodes to draw.
        node_lables : bool
            If `True` add the nodes.
        """
        pts = [node.point for node in nodes]
        self.app.add(pts, colors=[hextorgb("#386641")]*len(pts))

        for node in nodes:
            if node_lables:
                txt = Text(str(node.key), node.point, height=35)
                self.app.add(txt, color=[1, 0, 0])

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
            self.app.add(Collection(collection_items), facecolor=(.9, .9, .9))

    def draw_shell_elements(self, elements, show_vertices=True):
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
            if len(element.nodes) == 4:
                collection_items.append(Mesh.from_vertices_and_faces(pts, [[1, 2, 3, 0]]))
            elif len(element.nodes) == 3:
                collection_items.append(Mesh.from_vertices_and_faces(pts, [[0, 1, 2]]))
            else:
                raise NotImplementedError("only 3 and 4 vertices shells supported at the moment")
        if collection_items:
            self.app.add(Collection(collection_items), facecolor=(.9, .9, .9))

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

    def draw_bcs(self, model, parts=None, scale_factor=1.):
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

    def draw_loads(self, step, scale_factor=1., app_point='end'):
        """Draw the applied loads for given steps.

        Parameters
        ----------
        steps : [:class:`compas_fea2.problem._Step`]
            List of steps. Only the loads in these steps will be shown.
        scale_factor : float, optional
            Scale the loads reppresentation to have a nicer drawing,
            by default 1.
        """
        if isinstance(step, _GeneralStep):
            for pattern in step._patterns:
                if isinstance(pattern.load, PointLoad):
                    vector = Vector(x=pattern.load.components['x'] or 0.,
                                    y=pattern.load.components['y'] or 0.,
                                    z=pattern.load.components['z'] or 0.)
                    if vector.length == 0:
                        continue
                    vector.scale(scale_factor)
                    if app_point=='end':
                        pts = [[node.x-vector.x, node.y-vector.y, node.z-vector.z] for node in pattern.distribution]
                    else:
                        pts = [node.point for node in pattern.distribution]
                    # TODO add moment components xx, yy, zz
                    vectors = [vector] * len(pts)
                    self.draw_nodes_vector(pts, vectors, scale_factor=scale_factor)
                else:
                    print("WARNING! Only point loads are currently supported!")

    def draw_nodes_vector(self, pts, vectors, colors=(0, 1, 0), scale_factor=1.):
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
        for pt, vector, color in zip(pts, vectors, colors):
            arrows.append(Arrow(pt, vector,
                                head_portion=3*scale_factor, head_width=0.5*scale_factor, body_width=0.25*scale_factor))
            arrows_properties.append({"u": 30,
                                      "show_lines": False,
                                      "facecolor": color})
        if arrows:
            self.app.add(Collection(arrows, arrows_properties))

    def show(self):
        """Display the viewport.
        """
        self.app.show()

    def dynamic_show(self):
        """Display the viewport dynamically.
        """
        self.app.run()

# class BeamViewer():
#     pass

# class ShellViewer():
#     pass

# class OptiViewer(ProblemViewer):
#     pass
