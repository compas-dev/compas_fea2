import os
from typing import Iterable

import numpy as np
from compas.colors import Color
from compas.colors import ColorMap
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polyhedron
from compas.geometry import Translation
from compas.geometry import Vector
from compas.geometry import sum_vectors

import compas_fea2
from compas_fea2.model.bcs import FixedBC
from compas_fea2.model.bcs import PinnedBC
from compas_fea2.model.bcs import RollerBCX
from compas_fea2.model.bcs import RollerBCY
from compas_fea2.model.bcs import RollerBCZ
from compas_fea2.problem.steps import GeneralStep
from compas_fea2.UI.viewer.primitives import FixBCShape
from compas_fea2.UI.viewer.primitives import PinBCShape
from compas_fea2.UI.viewer.primitives import RollerBCShape
from compas_fea2.model.elements import _Element1D


import os
from compas_viewer.viewer import Viewer
from compas_viewer.scene import GroupObject
from compas_viewer.scene import Collection


HERE = os.path.dirname(__file__)
CONFIG = os.path.join(HERE, "config.json")

color_palette = {
    "faces": Color.from_hex("#e8e5d4"),
    "edges": Color.from_hex("#4554ba"),
    "nodes": Color.black,
}


class FEA2Viewer:
    def __init__(self, center=[1, 1, 1], scale_model=1000, **kwargs):
        self.viewer = Viewer(**kwargs)
        self.viewer.renderer.camera.target = [i * scale_model for i in center]
        self.viewer.config.vectorsize = 0.5
        V1 = np.array([0, 0, 0])
        V2 = np.array(self.viewer.renderer.camera.target)
        delta = V2 - V1
        length = np.linalg.norm(delta)
        distance = length * 3
        unitSlope = delta / length
        new_position = V1 + unitSlope * distance
        self.viewer.renderer.camera.position = new_position.tolist()
        self.viewer.renderer.camera.near *= 1
        self.viewer.renderer.camera.far *= 10000
        self.viewer.renderer.camera.scale *= scale_model


class FEA2ModelObject(GroupObject):
    def __init__(self, model, show_bcs=True, show_parts=True, **kwargs):
        from compas.geometry import Sphere

        model = kwargs.pop("item")

        face_color = kwargs.get("face_color", color_palette["faces"])
        line_color = kwargs.get("line_color", color_palette["edges"])
        show_faces = kwargs.get("show_faces", True)
        show_lines = kwargs.get("show_lines", False)
        show_points = kwargs.get("show_points", False)
        show_nodes = kwargs.get("show_nodes", True)
        opacity = kwargs.get("opacity", 1.0)
        part_meshes = []
        if show_parts:
            for part in model.parts:
                if part._discretized_boundary_mesh:
                    part_meshes.append(
                        (
                            # part._boundary_mesh,
                            part._discretized_boundary_mesh,
                            {
                                "show_faces": show_faces,
                                "show_lines": show_lines,
                                "show_points": show_points,
                                "facecolor": face_color,
                                "linecolor": line_color,
                                "opacity": opacity,
                            },
                        )
                    )
                for element in part.elements:
                    if isinstance(element, _Element1D):
                        part_meshes.append(
                            (
                                element.outermesh,
                                {"show_faces": show_faces, 
                                 "show_lines": show_lines, 
                                 "show_points": show_points, 
                                 "facecolor": face_color, 
                                 "linecolor": line_color, 
                                 "opacity": opacity},
                            )
                        )
                for node in part.nodes:
                    if show_nodes:
                        part_meshes.append(
                            (
                                Sphere(radius=10, point=node.point).to_mesh(),
                                {
                                    "show_faces": True,
                                    "facecolor": Color.red(),
                                    "linecolor": Color.red(),
                                    "show_points": False,
                                },
                            )
                        )

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
                                },
                            )
                        )

        parts = (part_meshes, {"name": "parts"})
        interfaces = ([], {"name": "interfaces"})
        bcs = (bcs_meshes, {"name": "bcs"})
        super().__init__(item=[parts, interfaces, bcs], name=model.name, **kwargs)
