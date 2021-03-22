import compas

from compas_view2 import app
from compas.datastructures import Mesh
from compas.geometry import Translation, Scale

from compas_fea2 import DATA
from compas_fea2 import TEMP

viewer = app.App(width=800, height=500)

mesh = Mesh.from_stl('C:/temp/test_solid_structure_1/TOSCA_POST/ISO_SMOOTHING_0_3.stl')
# T = Translation.from_vector([0, 0, 1])
S = Scale.from_factors([.001, .001, .001])
mesh.transform(S)

viewer.add(mesh, show_vertices=False, hide_coplanaredges=False)
# viewer.add(mesh2, show_vertices=False, hide_coplanaredges=True)

viewer.show()
