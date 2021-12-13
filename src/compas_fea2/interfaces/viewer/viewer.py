import os
from compas_view2 import app
from compas_view2.shapes import Arrow
from compas.datastructures import Mesh
from compas.geometry import Scale
from compas.geometry import Point
from compas.geometry import Cone
from compas.geometry import Circle
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Box

from compas_fea2.backends._base.model.elements import ShellElementBase
from compas_fea2.backends._base.model.elements import SolidElementBase
from compas_fea2.backends._base.model.elements import BeamElementBase
from compas_fea2.backends._base.model.bcs import PinnedBCBase

from compas_fea2.backends._base.problem.loads import PointLoadBase


# class Viewer():
#     """Viewer for analysis results.

#     Parameters
#     ----------
#     geometry : mesh, list
#         `compas` Mesh object or list of `compas` Mesh objects to renderself.
#     width : int
#         width of the application window
#     height : int
#         height of the application window
#     scale_factor : float
#         scale factor to apply to the original geoemtry. the viewer units are in millimiters.

#     Attributes
#     ----------
#     geometry : mesh, list
#         `compas` Mesh object or list of `compas` Mesh objects to renderself.
#     width : int
#         width of the application window
#     height : int
#         height of the application window
#     scale_factor : float
#         scale factor to apply to the original geoemtry. the viewer units are in millimiters.
#     app : ?
#         application
#     """

#     def __init__(self, geometry, width=800, height=500, scale_factor=.001):

#         self.width = width
#         self.height = height
#         self.app = app.App(width=width, height=height)
#         self.scale_factor = scale_factor
#         self._geometry = self._add_geometry(geometry)

#     @property
#     def geometry(self):
#         """The geometry property."""
#         return self._geometry

#     def _add_geometry(self, geometry):
#         if not isinstance(geometry, list):
#             geometry = [geometry]
#         for mesh in geometry:
#             if isinstance(mesh, Mesh):
#                 self._mesh = self._scale_mesh(mesh)
#                 self.app.add(self._mesh, show_vertices=False, hide_coplanaredges=False)
#             elif mesh == None:
#                 pass
#             else:
#                 raise TypeError('geometry not of `compas` Mesh type')
#         self._geometry = geometry

#     def _scale_mesh(self, mesh):
#         S = Scale.from_factors([self.scale_factor]*3)
#         mesh.transform(S)
#         return mesh

#     def show(self):
#         self.app.show()


class ModelViewer():

    def __init__(self, model, width, height, scale_factor):
        self.model = model
        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.app = app.App(width=width, height=height)
        self._add_nodes()
        self._add_elements()
        self._add_bcs()

    def _scale_mesh(self, mesh):
        S = Scale.from_factors([self.scale_factor]*3)
        mesh.transform(S)
        return mesh

    def _add_nodes(self):
        for part in self.model.parts.values():
            for node in part.nodes:
                point = Point(node.x, node.y, node.z)
                self.app.add(point, size=10)

    def _add_elements(self):
        for part in self.model.parts.values():
            for element in part.elements.values():
                pts = [Point(*part.nodes[node].xyz) for node in element.connectivity]
                if isinstance(element, ShellElementBase):
                    if len(element.connectivity) == 4:
                        mesh = Mesh.from_vertices_and_faces(pts, [[1, 2, 3, 0]])
                        self.app.add(mesh, show_vertices=False, hide_coplanaredges=False)
                    elif len(element.connectivity) == 3:
                        mesh = Mesh.from_vertices_and_faces(pts, [[0, 1, 2]])
                        self.app.add(mesh, show_vertices=False, hide_coplanaredges=False)
                    else:
                        raise NotImplementedError("only 4 vertices shells supported at the moment")
                elif isinstance(element, BeamElementBase):
                    line = Line(pts[0], pts[1])
                    self.app.add(line, linewidth=0.5)
                elif isinstance(element, SolidElementBase):
                    if len(element.connectivity) == 8:
                        mesh = Mesh.from_vertices_and_faces(pts, [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [
                                                            1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]])
                        self.app.add(mesh, show_vertices=False, hide_coplanaredges=False, opacity=0.1)
                else:
                    raise print(f'{element} is not supported byt the viewer')

    def _add_bcs(self):
        for bc in self.model.bcs.values():
            # TODO remove 'part-1'
            pts = [Point(*self.model.parts['part-1'].nodes[node].xyz) for node in bc.nodes]
            if isinstance(bc, PinnedBCBase):
                cone_height = 0.4
                cone_diameter = 0.2
                plane = Plane([0, 0, 0], [0, 0, 1])
                circle = Circle(plane, cone_diameter)
                cone = Cone(circle, cone_height)
                for pt in pts:
                    obj = self.app.add(cone, facecolor=(1, 0, 0))
                    obj.translation = (pt.x, pt.y, pt.z-cone_height)
        # box = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 0.4, 0.4, 0.4)
        # obj1 = self.app.add(box, color=(1, 0, 0))
        # obj1.translation = (0, 0, -5.2)

    def show(self):
        self.app.show()

    def dynamic_show(self):
        self.app.run()


class ProblemViewer(ModelViewer):
    def __init__(self, problem, width=800, height=500, scale_factor=.001):
        super(ProblemViewer, self).__init__(problem.model, width, height, scale_factor)
        self.problem = problem

        self._add_loads()

    def _add_loads(self):  # TODO split the steps
        for load in self.problem.loads.values():
            # TODO remove 'part-1'
            pts = [Point(*self.problem.model.parts['part-1'].nodes[node].xyz) for node in load.nodes]
            if isinstance(load, PointLoadBase):
                for pt in pts:
                    # TODO add moment components xx, yy, zz
                    # TODO add scale forces
                    arrow = Arrow(pt, [load.components['x']/10000, load.components['y']/10000, load.components['z']/10000],
                                  head_portion=0.2, head_width=0.07, body_width=0.02)
                    self.app.add(arrow, u=16, show_edges=False, facecolor=(0, 1, 0))


class ResultsViewer(ProblemViewer):
    pass


class BeamViewer():
    pass


class ShellViewer():
    pass


class OptiViewer(ProblemViewer):
    """Viewer for topology optimisation analysis results.

    Parameters
    ----------
    problem : Problem
        `compas_fea2` Problem object of the topology optimisation analysis. The promblem should have been previously
        solved.
    width : int
        width of the application window
    height : int
        height of the application window
    scale_factor : float
        scale factor to apply to the original geoemtry. the viewer units are in millimiters.

    Attributes
    ----------
    problem : Problem
        `compas_fea2` Problem object of the topology optimisation analysis. The promblem should have been previously
        solved.
    width : int
        width of the application window
    height : int
        height of the application window
    scale_factor : float
        scale factor to apply to the original geoemtry. the viewer units are in millimiters.
    app : ?
        application
    """

    def __init__(self, problem, width=800, height=500, scale_factor=.001):
        super().__init__(problem, width, height, scale_factor)
        self._get_scaled_mesh()

    def _get_scaled_mesh(self):
        path = os.path.join(self.problem.path, self.problem.name, 'TOSCA_POST', 'ISO_SMOOTHING_0_3.stl')
        mesh = self._scale_mesh(Mesh.from_stl(path))
        self.app.add(mesh, show_vertices=False, hide_coplanaredges=False, facecolor=(0.7, 0.7, 0.7))


if __name__ == '__main__':
    from compas_fea2.backends.abaqus.model import Model
    from compas_fea2.backends.abaqus.model import ShellSection
    from compas_fea2.backends.abaqus.model import ElasticIsotropic
    from compas_fea2.backends.abaqus.problem import Problem
    from compas.datastructures import Mesh
    from compas_fea2 import DATA

    # mesh = Mesh.from_obj(DATA + '/hypar.obj')
    # S = Scale.from_factors([0.001]*3)
    # mesh.transform(S)
    model = Model(name='structural_model')
    # section = ShellSection('section', 10, ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))
    # model.shell_from_mesh(mesh, section)

    # problem = Problem('simple_load', model)
    # v = ProblemViewer(problem)
    # v.show()

    problem = Problem(name='test_solid_structure_viewer', model=model)
    problem.path = 'C:/temp'
    v = OptiViewer(problem)
    v.show()
