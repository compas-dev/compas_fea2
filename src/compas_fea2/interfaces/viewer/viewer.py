import os
from compas_view2 import app
from compas_view2.shapes import Arrow
from compas.datastructures import Mesh
from compas.geometry import Scale
from compas.geometry import Point
from compas.geometry import Cone
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Box

from compas_fea2.backends._base.model.elements import ShellElementBase


class Viewer():
    """Viewer for analysis results.

    Parameters
    ----------
    geometry : mesh, list
        `compas` Mesh object or list of `compas` Mesh objects to renderself.
    width : int
        width of the application window
    height : int
        height of the application window
    scale_factor : float
        scale factor to apply to the original geoemtry. the viewer units are in millimiters.

    Attributes
    ----------
    geometry : mesh, list
        `compas` Mesh object or list of `compas` Mesh objects to renderself.
    width : int
        width of the application window
    height : int
        height of the application window
    scale_factor : float
        scale factor to apply to the original geoemtry. the viewer units are in millimiters.
    app : ?
        application
    """

    def __init__(self, geometry, width=800, height=500, scale_factor=.001):

        self.width = width
        self.height = height
        self.app = app.App(width=width, height=height)
        self.scale_factor = scale_factor
        self._geometry = self._add_geometry(geometry)

    @property
    def geometry(self):
        """The geometry property."""
        return self._geometry

    def _add_geometry(self, geometry):
        if not isinstance(geometry, list):
            geometry = [geometry]
        for mesh in geometry:
            if isinstance(mesh, Mesh):
                self._mesh = self._scale_mesh(mesh)
                self.app.add(self._mesh, show_vertices=False, hide_coplanaredges=False)
            elif mesh == None:
                pass
            else:
                raise TypeError('geometry not of `compas` Mesh type')
        self._geometry = geometry

    def _scale_mesh(self, mesh):
        S = Scale.from_factors([self.scale_factor]*3)
        mesh.transform(S)
        return mesh

    def show(self):
        self.app.show()


class ModelViewer():

    def __init__(self, model, width=800, height=500, scale_factor=.001):
        self.model = model
        self.width = width
        self.height = height
        self.app = app.App(width=width, height=height)
        self._add_nodes()
        self._add_elements()

    def _add_nodes(self):
        for part in self.model.parts.values():
            for node in part.nodes:
                point = Point(node.x, node.y, node.z)
                self.app.add(point, size=10)

    def _add_elements(self):
        for part in self.model.parts.values():
            for element in part.elements:
                if not isinstance(element, ShellElementBase):
                    break
                else:
                    if len(element.connectivity) == 4:
                        pts = [Point(*part.nodes[node].xyz) for node in element.connectivity]
                        mesh = Mesh.from_vertices_and_faces(pts, [[1, 2, 3, 0]])
                        self.app.add(mesh, show_vertices=False, hide_coplanaredges=False)
                    else:
                        raise NotImplementedError("only 4 vertices shells supported at the moment")

    def show(self):
        self.app.show()


class ProblemViewer(ModelViewer):
    def __init__(self, problem, width=800, height=500, scale_factor=.001):
        super(ProblemViewer, self).__init__(problem.model, width, height, scale_factor)
        self.problem = problem
        self._add_supports()
        self._add_loads()

    def _add_loads(self):
        arrow = Arrow([5, 0, 0], [0, 0.5, 0.3], head_portion=0.2, head_width=0.07, body_width=0.02)
        self.app.add(arrow, u=16, show_edges=False, facecolor=(0, 1, 0))

    def _add_supports(self):
        plane = Plane([0, 0, 0], [0, 0, 1])
        circle = Circle(plane, 0.2)
        cone = Cone(circle, 0.4)
        obj = self.app.add(cone, facecolor=(1, 0, 0))
        obj.translation = (5, 3, -5.4)
        box = Box(([0, 0, 0], [1, 0, 0], [0, 1, 0]), 0.4, 0.4, 0.4)
        obj1 = self.app.add(box, color=(1, 0, 0))
        obj1.translation = (0, 0, -5.2)


class OptiViewer(Viewer):
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
        super().__init__(None, width, height, scale_factor)
        self.problem = problem
        self._get_scaled_mesh()

    def _get_scaled_mesh(self):
        path = os.path.join(self.problem.path, self.problem.name, 'TOSCA_POST', 'ISO_SMOOTHING_0_3.stl')
        self.app.add(self._scale_mesh(Mesh.from_stl(path)), show_vertices=False, hide_coplanaredges=False)


if __name__ == '__main__':
    from compas_fea2.backends.abaqus.model import Model
    from compas_fea2.backends.abaqus.model import ShellSection
    from compas_fea2.backends.abaqus.model import ElasticIsotropic
    from compas_fea2.backends.abaqus.problem import Problem
    from compas.datastructures import Mesh
    from compas_fea2 import DATA

    mesh = Mesh.from_obj(DATA + '/hypar.obj')
    S = Scale.from_factors([0.001]*3)
    mesh.transform(S)
    model = Model(name='structural_model')
    section = ShellSection('section', 10, ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))
    model.shell_from_mesh(mesh, section)

    problem = Problem('simple_load', model)
    v = ProblemViewer(problem)
    v.show()

    # problem = Problem(name='test_solid_structure', model=model)
    # problem.path ='C:/temp'
    # v = OptiViewer(problem)
    # v.show()
