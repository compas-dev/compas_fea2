import compas
from compas.datastructures import Mesh

def gmesh_to_compas(gmshModel):
    nodes = gmshModel.mesh.getNodes()
    node_tags = nodes[0]
    node_coords = nodes[1].reshape((-1, 3), order='C')
    node_paramcoords = nodes[2]
    xyz = {}
    for tag, coords  in zip(node_tags, node_coords):
        xyz[int(tag)] = coords.tolist()
    elements = gmshModel.mesh.getElements()
    triangles = []
    for etype, etags, ntags in zip(*elements):
        if etype == 2:
            for i, etag in enumerate(etags):
                n = gmshModel.mesh.getElementProperties(etype)[3]
                triangle = ntags[i * n: i * n + n]
                triangles.append(triangle.tolist())
    # gmshModel.finalize()
    return Mesh.from_vertices_and_faces(xyz, triangles)
