from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.colors import Color
from compas.colors import ColorMap
from compas.geometry import Vector
from compas.scene import SceneObject  # noqa: F401
from compas_viewer.scene import BufferGeometry  # noqa: F401
from compas_viewer.scene import Collection
from compas_viewer.scene import GroupObject  # noqa: F401

from compas_fea2.model.bcs import FixedBC
from compas_fea2.model.bcs import PinnedBC
from compas_fea2.model.bcs import RollerBCX
from compas_fea2.model.bcs import RollerBCY
from compas_fea2.model.bcs import RollerBCZ
from compas_fea2.UI.viewer.primitives import FixBCShape
from compas_fea2.UI.viewer.primitives import PinBCShape
from compas_fea2.UI.viewer.primitives import RollerBCShape

from .drawer import draw_field_contour
from .drawer import draw_field_vectors

color_palette = {
    "faces": Color.from_hex("#e8e5d4"),
    "edges": Color.from_hex("#4554ba"),
    "nodes": Color.black,
}


class FEA2NodeObject(GroupObject):
    """Node object for visualization.

    Parameters
    ----------
    node : :class:`compas_fea2.model.Node`
        The node to visualize.

    """

    def __init__(self, node, **kwargs):
        node = kwargs.pop("item")
        data = (
            node.point,
            {
                "pointcolor": Color.grey(),
                "pointßsize": 10,
                "opacity": 0.5,
                "name": node.name,
            },
        )

        super().__init__(item=data, **kwargs)


class FEA2ModelObject(GroupObject):
    """Model object for visualization.

    Parameters
    ----------
    model : :class:`compas_fea2.model.Structure`
        The model to visualize.
    fast : bool
        If True, the visualization will be faster.
    show_bcs : bool
        If True, the boundary conditions will be displayed.
    show_parts : bool
        If True, the parts will be displayed.
    """

    def __init__(self, fast=False, show_bcs=True, show_parts=True, show_connectors=True, **kwargs):
        model = kwargs.pop("item")

        face_color = kwargs.get("face_color", color_palette["faces"])
        line_color = kwargs.get("line_color", color_palette["edges"])
        show_faces = kwargs.get("show_faces", True)
        show_lines = kwargs.get("show_lines", False)
        show_nodes = kwargs.get("show_nodes", True)
        opacity = kwargs.get("opacity", 1.0)
        part_meshes = []
        if show_parts:
            # DRAW PARTS
            for part in model.parts:
                # DRAW NODES
                if not fast:
                    for node in part.nodes:
                        if show_nodes:
                            part_meshes.append(
                                (
                                    node.point,
                                    {
                                        "pointcolor": Color.grey(),
                                        "pointsize": 10,
                                        "opacity": 0.5,
                                        "name": node.name,
                                    },
                                )
                            )
                else:
                    collection = []
                    for node in part.nodes:
                        # if part._discretized_boundary_mesh:
                        collection.append(node.point)
                    part_meshes.append((Collection(collection), {"name": "nodes", "colors": Color.grey()}))

                # DRAW ELEMENTS
                if not fast:
                    for element in part.elements:
                        part_meshes.append(
                            (
                                element.outermesh,
                                {
                                    "show_faces": show_faces,
                                    "show_lines": show_lines,
                                    "show_points": False,
                                    "facecolor": face_color,
                                    "linecolor": line_color,
                                    "opacity": opacity,
                                    "name": element.name,
                                },
                            )
                        )
                else:
                    collection = []
                    for element in part.elements:
                        # if part._discretized_boundary_mesh:
                        collection.append(
                            element.outermesh
                            # (
                            #     # part._boundary_mesh,
                            #     part._discretized_boundary_mesh,
                            #     {
                            #         "show_faces": show_faces,
                            #         "show_lines": show_lines,
                            #         "show_points": show_points,
                            #         "linecolor": line_color,
                            #         "facecolor": face_color,
                            #         "opacity": opacity,
                            #         "name": part.name,
                            #     },
                            # )
                        )
                    part_meshes.append((Collection(collection), {"name": "elements"}))

        # DRAW BOUNDARY CONDITIONS
        bcs_meshes = []
        if show_bcs:
            if model.bcs:
                for bc, nodes in model.bcs.items():
                    for node in nodes:
                        if isinstance(bc, PinnedBC):
                            shape = PinBCShape(node.xyz, scale=show_bcs).shape
                        if isinstance(bc, FixedBC):
                            shape = FixBCShape(node.xyz, scale=show_bcs).shape
                        if isinstance(bc, (RollerBCX, RollerBCY, RollerBCZ)):
                            shape = RollerBCShape(node.xyz, scale=show_bcs).shape
                        bcs_meshes.append(
                            (
                                shape,
                                {
                                    "show_faces": show_faces,
                                    "facecolor": Color.red(),
                                    "linecolor": Color.red(),
                                    "show_points": False,
                                    "opacity": 0.5,
                                    "name": bc.name,
                                },
                            )
                        )

        # DRAW INTERFACES
        # DRAW CONSTRAINTS
        # DRAW CONNECTORS
        connectors_meshes = []
        if show_connectors:
            for connector in model.connectors:
                connectors_meshes.append(
                    (
                        connector.nodes[0].point,
                        {
                            "pointcolor": Color.red(),
                            "pointsize": 50,
                            "opacity": 0.2,
                            "name": connector.name,
                        },
                    )
                )

        parts = (part_meshes, {"name": "parts"})
        interfaces = ([], {"name": "interfaces"})
        connectors = (connectors_meshes, {"name": "connectors"})
        bcs = (bcs_meshes, {"name": "bcs"})
        super().__init__(item=[parts, interfaces, bcs, connectors], name="Model", **kwargs)


class FEA2StepObject(GroupObject):
    """Step object for visualization.

    Parameters
    ----------
    step : :class:`compas_fea2.problem.steps.Step`
        The step to visualize.
    scale_factor : float
        The scale factor for the visualization.

    """

    def __init__(self, scale_factor=1, **kwargs):
        step = kwargs.pop("item")

        # DRAW PATTERNS
        loadfields = []
        for load_field in step.load_fields:
            loadfield_forces = []
            for node, load in load_field.node_load:
                x = load.x or 0
                y = load.y or 0
                z = load.z or 0
                loadfield_forces.append(
                    (
                        Vector(x * scale_factor, y * scale_factor, z * scale_factor),  # .to_mesh(anchor=node.point)
                        {
                            "anchor": node.point,
                            "linecolor": Color.purple(),
                            "linewidth": 4,
                        },
                    )
                )
            loadfields.append(
                (
                    loadfield_forces,
                    {
                        "name": f"LOADFIELD-{load_field.name}",
                    },
                )
            )

        super().__init__(item=loadfields, name=f"STEP-{step.name}", componets=None, **kwargs)


class FEA2Stress2DFieldResultsObject(GroupObject):
    """StressFieldResults object for visualization.

    Parameters
    ----------
    field : :class:`compas_fea2.results.Field`
        The field to visualize.
    step : :class:`compas_fea2.problem.steps.Step`
        The step to visualize.
    scale_factor : float
        The scale factor for the visualization.
    components : list
        The components to visualize.

    """

    def __init__(self, model, components=None, show_vectors=1, plane="mid", show_contour=False, **kwargs):
        field = kwargs.pop("item")

        field_locations = [e.reference_point for e in field.locations]

        if not components:
            components = [0, 1, 2]
        names = {0: "min", 1: "mid", 2: "max"}
        colors = {0: Color.blue(), 1: Color.yellow(), 2: Color.red()}

        collections = []
        if show_vectors:
            for component in components:
                field_results = [v[component] for v in field.principal_components_vectors(plane)]
                lines, _ = draw_field_vectors(field_locations, field_results, show_vectors, translate=-0.5)
                collections.append((Collection(lines), {"name": f"PS-{names[component]}", "linecolor": colors[component], "linewidth": 3}))

        if show_contour:
            raise NotImplementedError("Contour visualization not implemented for stress fields.")

        super().__init__(item=collections, name=f"STRESS-{field.name}", **kwargs)


class FEA2NodeFieldResultsObject(GroupObject):
    """DisplacementFieldResults object for visualization.

    Parameters
    ----------
    field : :class:`compas_fea2.results.Field`
        The field to visualize.
    step : :class:`compas_fea2.problem.steps.Step`
        The step to visualize.
    scale_factor : float
        The scale factor for the visualization.
    components : list
        The components to visualize.

    """

    def __init__(self, components=None, show_vectors=1, show_contour=False, **kwargs):
        field = kwargs.pop("item")
        cmap = kwargs.get("cmap", ColorMap.from_palette("hawaii"))
        components = components or ["x", "y", "z"]

        group_elements = []
        if show_vectors:
            vectors, colors = draw_field_vectors([n.point for n in field.locations], list(field.components_vectors(components)), show_vectors, translate=0, cmap=cmap)

            for v, c in zip(vectors, colors):
                group_elements.append((v, {"name": f"DISP-{''.join(components)}", "linecolor": c, "linewidth": 3}))

        if show_contour:
            from compas_fea2.model.elements import BeamElement

            field_locations = list(field.locations)
            field_results = [v.length for v in field.components_vectors(components)]
            min_value = min(field_results)
            max_value = max(field_results)
            part_vertexcolor = draw_field_contour(field.model, field_locations, field_results, min_value, max_value, cmap)

            # DRAW CONTOURS ON 2D and 3D ELEMENTS
            for part, vertexcolor in part_vertexcolor.items():
                group_elements.append((part._discretized_boundary_mesh, {"name": part.name, "vertexcolor": vertexcolor, "use_vertexcolors": True}))

            # DRAW CONTOURS ON 1D ELEMENTS
            for part in field.model.parts:
                for element in part.elements:
                    vertexcolor = {}
                    if isinstance(element, BeamElement):
                        for c, n in enumerate(element.nodes):
                            v = field_results[field_locations.index(n)]
                            for p in range(len(element.section._shape.points)):
                                vertexcolor[p + c * len(element.section._shape.points)] = cmap(v, minval=min_value, maxval=max_value)
                        # vertexcolor = {c: Color.red() for c in range(2*len(element.section._shape.points))}
                        group_elements.append((element.outermesh, {"name": element.name, "vertexcolor": vertexcolor, "use_vertexcolors": True}))

        super().__init__(item=group_elements, name=f"RESULTS-{field.name}", **kwargs)
