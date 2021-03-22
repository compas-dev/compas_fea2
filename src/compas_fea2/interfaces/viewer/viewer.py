import os
from compas_view2 import app
from compas.datastructures import Mesh
from compas.geometry import Scale

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
            elif mesh==None:
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
    from compas_fea2.backends.abaqus import Problem
    model = Model(name='structural_model')
    problem = Problem(name='test_solid_structure', model=model)
    problem.path ='C:/temp'
    v = OptiViewer(problem)
    v.show()
