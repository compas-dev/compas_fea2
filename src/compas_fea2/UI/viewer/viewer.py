import os
import numpy as np

from math import sqrt
from typing import Iterable
from compas_view2.app import App
from compas_view2.objects import Collection
from compas_view2.shapes import Arrow
from compas_view2.shapes import Text

from compas.colors import ColorMap, Color

from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polyhedron
from compas.geometry import Vector
from compas.geometry import Transformation, Translation
from compas.geometry import sum_vectors

from compas_fea2.UI.viewer.shapes import (
    PinBCShape,
    FixBCShape,
    RollerBCShape,
    )

from compas_fea2.model.bcs import (
    FixedBC,
    PinnedBC,
    RollerBCX,
    RollerBCY,
    RollerBCZ,
    RollerBCXY,
    RollerBCXZ,
    RollerBCYZ,
    )

from compas_fea2.postprocess import principal_stresses

from compas_fea2.problem.loads import NodeLoad
from compas_fea2.problem.steps import GeneralStep

from compas_fea2.results import DisplacementFieldResults, StressFieldResults

# def hextorgb(hex):
#     return tuple(i / 255 for i in hex_to_rgb(hex))


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

    def draw_mesh(self, mesh, opacity=1):
        self.app.add(mesh, use_vertex_color=True, opacity=opacity)

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
        self.app.add(Collection(pts), facecolor=Color.from_hex("#386641"))

        if node_lables:
            txts = [Text(str(node.key), node.point, height=35) for node in nodes]
        self.app.add(Collection(txts), facecolor=Color.from_hex("#386641"))

    def draw_solid_elements(self, elements, show_vertices=True, opacity=1.):
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
            self.app.add(Collection(collection_items), facecolor=(0.9, 0.9, 0.9), show_points=show_vertices, opacity=opacity)

    def draw_shell_elements(self, elements, show_vertices=True, opacity=1, thicken=True):
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
                mesh = Mesh.from_vertices_and_faces(pts, [[1, 2, 3, 0]])
            elif len(element.nodes) == 3:
                mesh = Mesh.from_vertices_and_faces(pts, [[0, 1, 2]])
            else:
                raise NotImplementedError("only 3 and 4 vertices shells supported at the moment")
            if thicken:
                mesh.thickened(element.section.t)
            collection_items.append(mesh)
        if collection_items:
            self.app.add(Collection(collection_items), facecolor=(0.9, 0.9, 0.9), show_points=show_vertices, opacity=opacity)

    def draw_beam_elements(self, elements, show_vertices=True, opacity=1):
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
            self.app.add(Collection(collection_items), linewidth=10, show_points=show_vertices, opacity=opacity)

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
                        if isinstance(bc, (RollerBCX, RollerBCY, RollerBCZ)):
                            bcs_collection.append(RollerBCShape(node.xyz, scale=scale_factor).shape)
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
            if vector.length:
                arrows.append(Arrow(position=pt, direction=vector*scale_factor, head_portion=0.3, head_width=0.15, body_width=0.05))
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
        if isinstance(step, GeneralStep):
            pts, vectors = [], []
            for node, load in step.combination.node_load:
                    vector = Vector(
                        x=load.components["x"] or 0.0,
                        y=load.components["y"] or 0.0,
                        z=load.components["z"] or 0.0,
                    )
                    if vector.length == 0:
                        continue
                    vector.scale(scale_factor)
                    vectors.append(vector)
                    if app_point == "end":
                        pts.append([node.x - vector.x, node.y - vector.y, node.z - vector.z])
                    else:
                        pts.append([node.point])
                    # TODO add moment components xx, yy, zz

            self.draw_nodes_vector(pts, vectors, colors=[(0, 1, 1)]*len(pts))
        else:
            print("WARNING! Only point loads are currently supported!")

    def draw_reactions(self, step, scale_factor=1, colors=None, **kwargs):
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
        reactions = step.problem.reaction_field
        locations = []
        vectors = []
        for r in reactions.results(step):
            locations.append(r.location.xyz)
            vectors.append(r.vector)
        self.draw_nodes_vector(locations, vectors, scale_factor=scale_factor, colors=colors)

    def draw_deformed(self, step, scale_factor=1.0, opacity=1., **kwargs):
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
        displacements = step.problem.displacement_field
        for displacement in displacements.results(step):
            vector = displacement.vector.scaled(scale_factor)
            displacement.location.xyz = sum_vectors([Vector(*displacement.location.xyz), vector])

        for part in self.obj.parts:
            self.draw_beam_elements(part.elements_by_dimension(dimension=1), show_vertices=False, opacity=opacity)
            self.draw_shell_elements(part.elements_by_dimension(dimension=2), show_vertices=False, opacity=opacity)
            self.draw_solid_elements(part.elements_by_dimension(dimension=3), show_vertices=False, opacity=opacity)


    def draw_nodes_field_vector(self, field_results, component, step, vector_sf=1, **kwargs):
        """Display a given vector field.

        Parameters
        ----------
        field : str
            The field to display, e.g. 'U' for displacements.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        component : str
            The compoenet of the field to display, e.g. 'U3' for displacements
            along the 3 axis.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        step : :class:`compas_fea2.problem.Step`, optional
            The step to show the results of, by default None.
            if not provided, the last step of the analysis is used.
        deformed : bool, optional
            Choose if to display on the deformed configuration or not, by default False
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Options
        -------
        draw_loads : float
            Displays the loads at the step scaled by the given value
        draw_bcs : float
            Displays the bcs of the model scaled by the given value
        bound : float
            limit the results to the given value

        Raises
        ------
        ValueError
            _description_

        """

        # cmap = kwargs.get("cmap", ColorMap.from_palette("hawaii"))

        # Get values
        # min_value = field.min_invariants["magnitude"].invariants["MIN(magnitude)"]
        # max_value = field.max_invariants["magnitude"].invariants["MAX(magnitude)"]

        # Color the vector field
        pts, vectors, colors = [], [], []
        for r in field_results.results(step):
            if r.vector.length == 0:
                continue
            vectors.append(r.vector.scaled(vector_sf))
            pts.append(r.location.xyz)
            # colors.append(cmap(r.invariants["magnitude"], minval=min_value, maxval=max_value))

        # Display results
        self.draw_nodes_vector(pts=pts, vectors=vectors, colors=colors)

    def draw_nodes_field_contour(self, field_results, component, step, **kwargs):
        """Display a contour plot of a given field and component. The field must
        de defined at the nodes of the model (e.g displacement field).

        Parameters
        ----------
        field : str
            The field to display, e.g. 'U' for displacements.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        component : str
            The compoenet of the field to display, e.g. 'U3' for displacements
            along the 3 axis.
            Check the :class:`compas_fea2.problem.FieldOutput` for more info about
            valid components.
        step : :class:`compas_fea2.problem.Step`, optional
            The step to show the results of, by default None.
            if not provided, the last step of the analysis is used.
        deformed : bool, optional
            Choose if to display on the deformed configuration or not, by default False
        width : int, optional
            Width of the viewer window, by default 1600
        height : int, optional
            Height of the viewer window, by default 900

        Options
        -------
        draw_loads : float
            Displays the loads at the step scaled by the given value
        draw_bcs : float
            Displays the bcs of the model scaled by the given value
        bound : float
            limit the results to the given value

        Raises
        ------
        ValueError
            _description_

        """
        cmap = kwargs.get("cmap", ColorMap.from_palette("hawaii"))

        # Get mesh
        parts_gkey_vertex = {}
        parts_mesh = {}
        for part in step.model.parts:
            if mesh := part.discretized_boundary_mesh:
                colored_mesh = mesh.copy()
                #FIXME change precision
                parts_gkey_vertex[part.name] = colored_mesh.gkey_vertex(3)
                parts_mesh[part.name] = colored_mesh
            else:
                raise AttributeError("Discretized boundary mesh not found")

        # Set the bounding limits
        if kwargs.get("bound", None):
            if not isinstance(kwargs["bound"], Iterable) or len(kwargs["bound"]) != 2:
                raise ValueError("You need to provide an upper and lower bound -> (lb, up)")
            if kwargs["bound"][0] > kwargs["bound"][1]:
                kwargs["bound"][0], kwargs["bound"][1] = kwargs["bound"][1], kwargs["bound"][0]

        # Get values
        min_result, max_result = field_results.get_limits_component(component, step=step)
        comp_str = field_results.field_name+str(component)
        min_value = min_result.components[comp_str]
        max_value = max_result.components[comp_str]

        # Color the mesh
        for r in field_results.results(step):
            if min_value - max_value == 0.0:
                color = Color.red()
            elif kwargs.get("bound", None):
                if r.components[comp_str] >= kwargs["bound"][1] or r.components[comp_str] <= kwargs["bound"][0]:
                    color = Color.red()
                else:
                    color = cmap(r.components[comp_str], minval=min_value, maxval=max_value)
            else:
                color = cmap(r.components[comp_str], minval=min_value, maxval=max_value)
            if r.location.gkey in parts_gkey_vertex[part.name]:
                parts_mesh[part.name].vertex_attribute(parts_gkey_vertex[part.name][r.location.gkey], "color", color)

        # Display results
        for part in step.model.parts:
            self.draw_mesh(parts_mesh[part.name], opacity=0.75)

    def draw_elements_field_vector(self, field_results, step, vector_sf=1, **kwargs):
        # cmap = kwargs.get("cmap", ColorMap.from_palette("hawaii"))

        # Color the vector field
        # FIXME temporary test - > change components
        pts, vectors, colors = [], [], []
        for r in field_results.results(step):
            ps_results_mid = list(r.principal_stresses)
            ps_results_top = list(r.principal_stresses_top) if hasattr(r, "principal_stresses_top") else None
            ps_results_bottom = list(r.principal_stresses_bottom) if hasattr(r, "principal_stresses_bottom") else None
            all_ps_results = {"mid":ps_results_mid, "top":ps_results_top, "bottom":ps_results_bottom}

            for k, v in all_ps_results.items():
                if v:
                    if len(v) == 2:
                        ps_colors = ((0, 1, 1), (1, 0, 0))
                    else:
                        ps_colors = ((0, 1, 1), (1, 1, 0), (1, 0, 0))

                    for ps, color in zip(v, ps_colors):
                        for dir in (-0.5, 0.5):
                            if k == "mid":
                                pts.append(r.location.reference_point)
                            elif k == "top":
                                X = Translation.from_vector(r.location.frame.zaxis.unitized() * r.location.section.t/2)
                                pts.append(Point(*r.location.reference_point).transformed(X))
                            elif k == "bottom":
                                X = Translation.from_vector(-r.location.frame.zaxis.unitized() * r.location.section.t/2)
                                pts.append(Point(*r.location.reference_point).transformed(X))
                            vectors.append(ps[1].scaled(vector_sf*dir))
                            colors.append(color)

            # colors.append(color)
            # colors.append(cmap(r.invariants["magnitude"], minval=min_value, maxval=max_value))

        # Display results
        self.draw_nodes_vector(pts=pts, vectors=vectors, colors=colors)

    def draw_nodes_contour(self, model, nodes_values, **kwargs):
        """

        """
        cmap = kwargs.get("cmap", ColorMap.from_palette("hawaii"))

        # Get mesh
        parts_gkey_vertex = {}
        parts_mesh = {}
        for part in model.parts:
            if mesh := part.discretized_boundary_mesh:
                colored_mesh = mesh.copy()
                #FIXME change precision
                parts_gkey_vertex[part.name] = colored_mesh.gkey_vertex(3)
                parts_mesh[part.name] = colored_mesh
            else:
                raise AttributeError("Discretized boundary mesh not found")

        # Set the bounding limits
        if kwargs.get("bound", None):
            if not isinstance(kwargs["bound"], Iterable) or len(kwargs["bound"]) != 2:
                raise ValueError("You need to provide an upper and lower bound -> (lb, up)")
            if kwargs["bound"][0] > kwargs["bound"][1]:
                kwargs["bound"][0], kwargs["bound"][1] = kwargs["bound"][1], kwargs["bound"][0]

        # Get values
        values = list(nodes_values.values())
        min_value = kwargs["bound"][0] if kwargs.get("bound", None) else min(values)
        max_value = kwargs["bound"][1] if kwargs.get("bound", None) else min(values)

        # Color the mesh
        for n, v in nodes_values.items():
            if min_value - max_value == 0.0:
                color = Color.red()
            elif kwargs.get("bound", None):
                if v >= kwargs["bound"][1] or v <= kwargs["bound"][0]:
                    color = Color.red()
                else:
                    color = cmap(v, minval=min_value, maxval=max_value)
            else:
                color = cmap(v, minval=min_value, maxval=max_value)
            if n.gkey in parts_gkey_vertex[part.name]:
                parts_mesh[part.name].vertex_attribute(parts_gkey_vertex[part.name][n.gkey], "color", color)

        # Display results
        for part in model.parts:
            self.draw_mesh(parts_mesh[part.name], opacity=0.75)

    def show(self):
        """Display the viewport."""
        self.app.show()

    def dynamic_show(self):
        """Display the viewport dynamically."""
        self.app.run()
