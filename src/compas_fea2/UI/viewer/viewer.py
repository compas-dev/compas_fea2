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

from compas_fea2.UI.viewer.shapes import PinBCShape
from compas_fea2.UI.viewer.shapes import FixBCShape
from compas_fea2.model.elements import ShellElement
from compas_fea2.model.elements import SolidElement
from compas_fea2.model.elements import BeamElement
from compas_fea2.model.bcs import FixedBC, PinnedBC

from compas_fea2.problem.loads import GravityLoad, PointLoad
from compas_fea2.problem.steps import _GeneralStep

from compas_fea2.utilities._utils import _compute_model_dimensions


def hextorgb(hex):
    return tuple(i / 255 for i in hex_to_rgb(hex))


class FEA2Viewer():

    def __init__(self, width=800, height=500, scale_factor=1, **kwargs):
        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.app = App(width=width, height=height)

    def _scale_mesh(self, mesh):
        S = Scale.from_factors([self.scale_factor]*3)
        mesh.transform(S)
        return mesh

    def draw_parts(self, parts, draw_elements=True, draw_nodes=False, node_labels=False):
        parts = parts if isinstance(parts, Iterable) else [parts]
        for part in parts:
            if draw_elements:
                self.draw_elements(part.elements)
            if draw_nodes:
                self.draw_nodes(part.nodes, node_labels)

    def draw_elements(self, elements):
        shells_collection = []
        solid_collection = []
        lines_collection = []
        for element in elements:
            pts = [Point(*node.xyz) for node in element.nodes]
            if isinstance(element, ShellElement):
                if len(element.nodes) == 4:
                    mesh = Mesh.from_vertices_and_faces(pts, [[1, 2, 3, 0]])
                elif len(element.nodes) == 3:
                    mesh = Mesh.from_vertices_and_faces(pts, [[0, 1, 2]])
                else:
                    raise NotImplementedError("only 3 and 4 vertices shells supported at the moment")
                shells_collection.append(mesh)

            elif isinstance(element, BeamElement):
                line = Line(pts[0], pts[1])
                lines_collection.append(line)

            elif isinstance(element, SolidElement):
                # mesh = Mesh.from_vertices_and_faces(pts, list(element._face_indices.values()))
                mesh = Polyhedron(pts, list(element._face_indices.values()))
                solid_collection.append(mesh)

        if shells_collection:
            self.app.add(Collection(shells_collection), show_vertices=True,
                         hide_coplanaredges=False, facecolor=(.9, .9, .9))
        if solid_collection:
            self.app.add(Collection(solid_collection), show_vertices=True,
                         hide_coplanaredges=False, facecolor=(.9, .9, .9))
        if lines_collection:
            self.app.add(Collection(lines_collection), linewidth=0.5, show_vertices=True)

    def draw_nodes(self, nodes, node_lables):
        pts = [Point(*node.xyz) for node in nodes]
        self.app.add(pts, colors=[hextorgb("#386641")]*len(pts))

        for node in nodes:
            if node_lables:
                txt = Text(str(node.key), Point(*node.xyz), height=35)
                self.app.add(txt, color=[1, 0, 0])

    def draw_bcs(self, model, parts, scale_factor=1.):
        if model.bcs:
            bcs_collection = []
            for part, bc_node in model.bcs.items():
                if part in parts:
                    for bc, nodes in bc_node.items():
                        pts = [Point(*node.xyz) for node in nodes]
                        for pt in pts:
                            xyz = [pt.x, pt.y, pt.z]
                            if isinstance(bc, PinnedBC):
                                bcs_collection.append(PinBCShape(xyz, scale=scale_factor).shape)
                            if isinstance(bc, FixedBC):
                                bcs_collection.append(FixBCShape(xyz, scale=scale_factor).shape)
            if bcs_collection:
                self.app.add(Collection(bcs_collection), facecolor=(1, 0, 0), opacity=0.5)

    def draw_loads(self, steps, scale_factor=1.):
        for step in steps:
            if isinstance(step, _GeneralStep):
                for part, load_nodes in step.loads.items():
                    for load, nodes in load_nodes.items():
                        if isinstance(load, PointLoad):
                            pts = [Point(*node.xyz) for node in nodes]
                            vector = Vector(x=load.components['x'] or 0.,
                                            y=load.components['y'] or 0.,
                                            z=load.components['z'] or 0.)
                            if vector.length == 0:
                                continue
                            # TODO add moment components xx, yy, zz
                            vector.scale(scale_factor)
                            vectors = [vector] * len(pts)
                            self.draw_nodes_vector(pts, vectors)
                        else:
                            print("WARNING! Only point loads are currently supported!")

    def draw_nodes_vector(self, pts, vectors, colors=(0, 1, 0)):
        arrows = []
        for pt, vector in zip(pts, vectors):
            arrows.append(Arrow(pt, vector,
                                head_portion=0.2, head_width=0.07, body_width=0.02))
        if arrows:
            self.app.add(Collection(arrows), u=3, show_edges=False, colors=colors)

    def show(self):
        self.app.show()

    def dynamic_show(self):
        self.app.run()


# class BeamViewer():
#     pass


# class ShellViewer():
#     pass


# class OptiViewer(ProblemViewer):
#     pass
# #     """Viewer for topology optimisation analysis results.

# #     Parameters
# #     ----------
# #     problem : Problem
# #         `compas_fea2` Problem object of the topology optimisation analysis. The promblem should have been previously
# #         solved.
# #     width : int
# #         width of the application window
# #     height : int
# #         height of the application window
# #     scale_factor : float
# #         scale factor to apply to the original geoemtry. the viewer units are in millimiters.

# #     Attributes
# #     ----------
# #     problem : Problem
# #         `compas_fea2` Problem object of the topology optimisation analysis. The promblem should have been previously
# #         solved.
# #     width : int
# #         width of the application window
# #     height : int
# #         height of the application window
# #     scale_factor : float
# #         scale factor to apply to the original geoemtry. the viewer units are in millimiters.
# #     app : ?
# #         application
# #     """

# #     def __init__(self, problem, width=800, height=500, scale_factor=.001, node_labels=None):
# #         super().__init__(problem, width, height, scale_factor, node_labels)
# #         self._get_scaled_mesh()

# #     def _get_scaled_mesh(self):
# #         path = os.path.join(self.problem.path, self.problem.name, 'TOSCA_POST', 'ISO_SMOOTHING_0_3.stl')
# #         mesh = self._scale_mesh(Mesh.from_stl(path))
# #         self.app.add(mesh, show_vertices=False, hide_coplanaredges=False, facecolor=(0.7, 0.7, 0.7))


# # # if __name__ == '__main__':
# # #     from compas_fea2.backends.abaqus.model import Model
# # #     from compas_fea2.backends.abaqus.model import ShellSection
# # #     from compas_fea2.backends.abaqus.model import ElasticIsotropic
# # #     from compas_fea2.backends.abaqus.problem import Problem
# # #     from compas.datastructures import Mesh
# # #     from compas_fea2 import DATA

# # #     # mesh = Mesh.from_obj(DATA + '/hypar.obj')
# # #     # S = Scale.from_factors([0.001]*3)
# # #     # mesh.transform(S)
# # #     model = Model(name='structural_model')
# # #     # section = ShellSection('section', 10, ElasticIsotropic(name='mat_A', E=29000, v=0.17, density=2.5e-9))
# # #     # model.shell_from_mesh(mesh, section)

# # #     # problem = Problem('simple_load', model)
# # #     # v = ProblemViewer(problem)
# # #     # v.show()

# # #     problem = Problem(name='test_solid_structure_viewer', model=model)
# # #     problem.path = 'C:/temp'
# # #     v = OptiViewer(problem)
# # #     v.show()
