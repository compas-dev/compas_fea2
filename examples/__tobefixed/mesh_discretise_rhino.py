
from compas_fea2.cad import rhino

import rhinoscriptsyntax as rs





# Check the layer and that it is already a triangulated mesh
# you can triangulate any mesh in rhino using the command _TriangulateMesh
guid = rs.ObjectsByLayer('mesh_input')[0]

# you can change the target (size) and min_angle
rhino.discretise_mesh(mesh=guid, layer='output_mesh', target=0.050, min_angle=15)
