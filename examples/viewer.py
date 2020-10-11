from compas.datastructures import Mesh
from compas_viewers.meshviewer import MeshViewer

viewer = MeshViewer()
viewer.mesh = Mesh.from_polyhedron(6)

viewer.show()