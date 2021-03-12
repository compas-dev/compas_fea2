from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.geometry import add_vectors
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.rpc import Proxy

from compas_rhino.geometry import RhinoMesh

from compas_fea2 import utilities
from compas_fea2.preprocess import extrude_mesh
from compas_fea2.utilities import network_order


try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass

# try:
#     import rhinoscriptsyntax as rs
# except ImportError:
#     import platform
#     if platform.system() == 'Windows':
#         raise

import json

functions = Proxy('compas_fea2.utilities.functions')
meshing   = Proxy('compas_fea2.preprocess.meshing')


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'add_element_set',
    'add_node_set',
    'add_nodes_elements_from_layers',
    'add_sets_from_layers',
    'add_tets_from_mesh',
    'discretise_mesh',
    'mesh_extrude',
    'network_from_lines',
    'ordered_network',
]


def add_element_set(structure, guids, name):
    """
    Adds element set information from Rhino curve and mesh guids.

    Parameters
    ----------
    structure : obj
        Structure object to update.
    guids : list
        Rhino curve and Rhino mesh guids.
    name : str
        Name of the new element set.

    Returns
    -------
    None

    Notes
    -----
    - Meshes representing solids must have 'solid' in their name.
    """

    elements = []

    for guid in guids:

        if rs.IsCurve(guid):

            sp = structure.check_node_exists(rs.CurveStartPoint(guid))
            ep = structure.check_node_exists(rs.CurveEndPoint(guid))
            element = structure.check_element_exists([sp, ep])
            if element is not None:
                elements.append(element)

        elif rs.IsMesh(guid):

            vertices = rs.MeshVertices(guid)
            faces    = rs.MeshFaceVertices(guid)

            if rs.ObjectName(guid) and ('solid' in rs.ObjectName(guid)):
                nodes   = [structure.check_node_exists(i) for i in vertices]
                element = structure.check_element_exists(nodes)
                if element is not None:
                    elements.append(element)
            else:
                for face in faces:
                    nodes = [structure.check_node_exists(vertices[i]) for i in face]
                    if nodes[2] == nodes[3]:
                        del nodes[-1]
                    element = structure.check_element_exists(nodes)
                    if element is not None:
                        elements.append(element)

    structure.add_set(name=name, type='element', selection=elements)


# NOTE this is valid only for abaqus though!!
def add_node_set(structure, guids, name):
    """
    Adds node set information from Rhino point guids.

    Parameters
    ----------
    structure : obj
        Structure object to update.
    guids : list
        Rhino point guids.
    name : str
        Name of the new node set.

    Returns
    -------
    None

    """

    nodes = []

    for guid in guids:

        if rs.IsPoint(guid):

            node = structure.check_node_exists(rs.PointCoordinates(guid))
            if node is not None:
                nodes.append(node)

    structure.add_set(name=name, type='node', selection=nodes)


def add_nodes_elements_from_layers(structure, layers, line_type=None, mesh_type=None, thermal=False, pA=None, pL=None):
    """
    Adds node and element data from Rhino layers to the Structure object.

    Parameters
    ----------
    structure : obj
        Structure object to update.
    layers : list
        Layer string names to extract nodes and elements.
    line_type : str
        Element type for line objects.
    mesh_type : str
        Element type for mesh objects.
    thermal : bool
        Thermal properties on or off.
    pA : float
        Mass area density [kg/m2].
    pL : float
        Mass length density [kg/m].

    Returns
    -------
    list
        Node keys that were added to the Structure.
    list
        Element keys that were added to the Structure.

    """

    if isinstance(layers, str):
        layers = [layers]

    added_nodes    = set()
    added_elements = set()

    for layer in layers:

        elset = set()

        for guid in rs.ObjectsByLayer(layer):

            if line_type and rs.IsCurve(guid):

                sp_xyz = rs.CurveStartPoint(guid)
                ep_xyz = rs.CurveEndPoint(guid)
                ez = subtract_vectors(ep_xyz, sp_xyz)
                L  = length_vector(ez)
                m  = 0.5 * L * pL if pL else None

                sp = structure.add_node(xyz=sp_xyz, mass=m)
                ep = structure.add_node(xyz=ep_xyz, mass=m)
                added_nodes.add(sp)
                added_nodes.add(ep)

                try:
                    name = rs.ObjectName(guid).replace("'", '"')

                    if name[0] in ['_', '^']:
                        name = name[1:]

                    dic = json.loads(name)
                    ex  = dic.get('ex', None)
                    ey  = dic.get('ey', None)

                    if ex and not ey:
                        ey = cross_vectors(ex, ez)

                except:
                    ex = None
                    ey = None

                axes = {'ex': ex, 'ey': ey, 'ez': ez}

                ekey = structure.add_element(nodes=[sp, ep], etype=line_type, thermal=thermal, axes=axes)

                if (line_type == 'BeamElement') and (ex is None):

                    if (ez[0] == 0) and (ez[1] == 0):

                        print('***** WARNING: vertical BeamElement with no ex axis, element {0} *****'.format(ekey))

                if ekey is not None:
                    added_elements.add(ekey)
                    elset.add(ekey)

            elif mesh_type and rs.IsMesh(guid):

#                mesh = mesh_from_guid(Mesh(), guid)

                vertices = rs.MeshVertices(guid)
                nodes = []
                masses = []

                for c, vertex in enumerate(vertices):
                    m = mesh.vertex_area(c) * pA if pA else None
                    masses.append(m)
                    nodes.append(structure.add_node(xyz=vertex, mass=m))

                added_nodes.update(nodes)

                if mesh_type in ['HexahedronElement', 'TetrahedronElement', 'SolidElement', 'PentahedronElement']:
                    ekey = structure.add_element(nodes=nodes, type=mesh_type, thermal=thermal)

                    if ekey is not None:
                        added_elements.add(ekey)
                        elset.add(ekey)

                elif mesh_type=='MassElement':
                    node_iterator=0
                    for node in nodes:
                        ekey = structure.add_element(nodes=[node], type=mesh_type, thermal=thermal, mass=masses[node_iterator]) #structure.nodes[node].mass
                        node_iterator += 1
                        if ekey is not None:
                            added_elements.add(ekey)
                            elset.add(ekey)

                else:

                    try:
                        name = rs.ObjectName(guid).replace("'", '"')

                        if name[0] in ['_', '^']:
                            name = name[1:]

                        dic = json.loads(name)
                        ex  = dic.get('ex', None)
                        ey  = dic.get('ey', None)
                        ez  = dic.get('ez', None)

                        if (ex and ey) and (not ez):
                            ez = cross_vectors(ex, ey)

                    except:
                        ex = None
                        ey = None
                        ez = None

                    axes = {'ex': ex, 'ey': ey, 'ez': ez}

                    for face in rs.MeshFaceVertices(guid):

                        nodes = [structure.check_node_exists(vertices[i]) for i in face]
                        if nodes[-1] == nodes[-2]:
                            del nodes[-1]

                        ekey = structure.add_element(nodes=nodes, type=mesh_type, thermal=thermal, axes=axes)
                        if ekey is not None:
                            added_elements.add(ekey)
                            elset.add(ekey)

        structure.add_set(name=layer, type='element', selection=list(elset))

    return list(added_nodes), list(added_elements)


def add_sets_from_layers(structure, layers):
    """
    Add node and element sets to the Structure object from Rhino layers.

    Parameters
    ----------
    structure : obj
        Structure object to update.
    layers : list
        List of layer string names to take objects from.

    Returns
    -------
    None

    Notes
    -----
    - Layers should exclusively contain nodes or elements.
    - Mixed elements, e.g. lines and meshes, are allowed on a layer.
    - Sets will inherit the layer names as their set name.

    """

    if isinstance(layers, str):
        layers = [layers]

    for layer in layers:
        guids = rs.ObjectsByLayer(layer)

        if guids:
            name = layer.split('::')[-1] if '::' in layer else layer
            check_points = [rs.IsPoint(guid) for guid in guids]

            try:
                if all(check_points):
                    add_node_set(structure=structure, guids=guids, name=name)
                elif not any(check_points):
                    add_element_set(structure=structure, guids=guids, name=name)
                else:
                    print('***** Layer {0} contained a mixture of points and elements, set not created *****'.format(name))
            except:
                print('Sets are only valid in Abaqus')
                # raise NotImplementedError(NotImplementedType)


def add_tets_from_mesh(structure, name, mesh, draw_tets=False, volume=None, thermal=False):
    """
    Adds tetrahedron elements from a mesh in Rhino to the Structure object.

    Parameters
    ----------
    structure : obj
        Structure object to update.
    name : str
        Name for the element set of tetrahedrons.
    mesh : guid
        The mesh in Rhino representing the outer surface.
    draw_tets : str
        Layer to draw tetrahedrons on.
    volume : float
        Maximum volume for each tet.
    thermal : bool
        Thermal properties on or off.

    Returns
    -------
    None

    """

    rhinomesh = RhinoMesh.from_guid(mesh)
    vertices  = rhinomesh.vertices
    faces     = [face[:3] for face in rhinomesh.faces]

    try:
        tets_points, tets_elements = meshing.tets_from_vertices_faces(vertices=vertices, faces=faces, volume=volume)

        for point in tets_points:
            structure.add_node(point)

        ekeys = []

        for element in tets_elements:

            nodes = [structure.check_node_exists(tets_points[i]) for i in element]
            ekey  = structure.add_element(nodes=nodes, type='TetrahedronElement', thermal=thermal)
            ekeys.append(ekey)

        structure.add_set(name=name, type='element', selection=ekeys)

        if draw_tets:

            rs.EnableRedraw(False)
            rs.DeleteObjects(rs.ObjectsByLayer(draw_tets))
            rs.CurrentLayer(draw_tets)

            tet_faces = [[0, 2, 1, 1], [1, 2, 3, 3], [1, 3, 0, 0], [0, 3, 2, 2]]

            for i, points in enumerate(tets_elements):

                xyz = [tets_points[j] for j in points]
                rs.AddMesh(vertices=xyz, face_vertices=tet_faces)

            rs.EnableRedraw(True)

        print('***** MeshPy (TetGen) successfull *****')

    except:

        print('***** Error using MeshPy (TetGen) or drawing Tets *****')


def discretise_mesh(mesh, layer, target, min_angle=15, factor=1):
    """
    Discretise a mesh from an input triangulated coarse mesh into small denser meshes.

    Parameters
    ----------
    mesh : guid
        The guid of the Rhino input mesh.
    layer : str
        Layer name to draw results.
    target : float
        Target length of each triangle.
    min_angle : float
        Minimum internal angle of triangles.
    factor : float
        Factor on the maximum area of each triangle.

    Returns
    -------
    None

    """

    rhinomesh = RhinoMesh.from_guid(mesh)
    vertices  = rhinomesh.vertices
    faces     = [face[:3] for face in rhinomesh.faces]

    try:

        points, tris = meshing.discretise_faces(vertices=vertices, faces=faces, target=target, min_angle=min_angle, factor=factor)

        rs.CurrentLayer(rs.AddLayer(layer))
        rs.DeleteObjects(rs.ObjectsByLayer(layer))
        rs.EnableRedraw(False)

        for pts, tri in zip(points, tris):
            mesh_faces = []

            for i in tri:
                face_ = i + [i[-1]]
                mesh_faces.append(face_)
            rs.AddMesh(pts, mesh_faces)

        rs.EnableRedraw(True)

    except:

        print('***** Error using MeshPy (Triangle) or drawing faces *****')


def mesh_extrude(structure, guid, layers, thickness, mesh_name='', links_name='', blocks_name='', points_name='',
                 plot_mesh=False, plot_links=False, plot_blocks=False, plot_points=False):
    """
    Extrudes a Rhino mesh and adds/creates elements.

    Parameters
    ----------
    structure : obj
        Structure object to update.
    guid : guid
        Rhino mesh guid.
    layers : int
        Number of layers.
    thickness : float
        Layer thickness.
    mesh_name : str
        Name of set for mesh on final surface.
    links_name : str
        Name of set for adding links along extrusion.
    blocks_name : str
        Name of set for solid elements.
    points_name : str
        Name of aded points.
    plot_mesh : bool
        Plot outer mesh.
    plot_links : bool
        Plot links.
    plot_blocks : bool
        Plot blocks.
    plot_points : bool
        Plot end points.

    Returns
    -------
    None

    Notes
    -----
    - Extrusion is along the mesh vertex normals.

    """

    mesh = RhinoMesh.from_guid(guid).to_compas(cls=Mesh)
    extrude_mesh(structure=structure, mesh=mesh, layers=layers, thickness=thickness, mesh_name=mesh_name,
                 links_name=links_name, blocks_name=blocks_name)

    block_faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    xyz = structure.nodes_xyz()

    rs.EnableRedraw(False)

    if plot_blocks:

        rs.CurrentLayer(rs.AddLayer(blocks_name))
        rs.DeleteObjects(rs.ObjectsByLayer(blocks_name))

        for i in structure.sets[blocks_name]['selection']:
            nodes = structure.elements[i].nodes
            xyz   = structure.nodes_xyz(nodes)
            rs.AddMesh(xyz, block_faces)

    if plot_mesh:

        rs.CurrentLayer(rs.AddLayer(mesh_name))
        rs.DeleteObjects(rs.ObjectsByLayer(mesh_name))

        faces = []
        for i in structure.sets[mesh_name]['selection']:
            enodes = structure.elements[i].nodes
            if len(enodes) == 3:
                enodes.append(enodes[-1])
            faces.append(enodes)
        rs.AddMesh(xyz, faces)

    if plot_links:

        rs.CurrentLayer(rs.AddLayer(links_name))
        rs.DeleteObjects(rs.ObjectsByLayer(links_name))

        if plot_points:
            rs.CurrentLayer(rs.AddLayer(points_name))
            rs.DeleteObjects(rs.ObjectsByLayer(points_name))

        for i in structure.sets[links_name]['selection']:

            nodes = structure.elements[i].nodes
            xyz = structure.nodes_xyz(nodes)
            rs.CurrentLayer(links_name)
            rs.AddLine(xyz[0], xyz[1])

            if plot_points:
                rs.CurrentLayer(points_name)
                rs.AddPoint(xyz[1])

    rs.EnableRedraw(True)
    rs.CurrentLayer(rs.AddLayer('Default'))


def network_from_lines(guids=[], layer=None):
    """
    Creates a Network datastructure object from a list of Rhino curve guids.

    Parameters
    ----------
    guids : list
        guids of the Rhino curves to be made into a Network.
    layer : str
        Layer to grab line guids from.

    Returns
    -------
    obj
        Network datastructure object.

    """

    if layer:
        guids = rs.ObjectsByLayer(layer)
    lines = [[rs.CurveStartPoint(guid), rs.CurveEndPoint(guid)] for guid in guids if rs.IsCurve(guid)]

    return Network.from_lines(lines)


def ordered_network(structure, network, layer):
    """
    Extract vertex and edge orders from a Network for a given start-point.

    Parameters
    ----------
    structure : obj
        Structure object.
    network : obj
        Network Datastructure object.
    layer : str
        Layer to extract start-point (Rhino point).
    Returns
    -------
    list
        Ordered nodes for the Structure.
    list
        Ordered elements for the Structure.
    list
        Cumulative length at element mid-points.
    float
        Total length.
    Notes
    -----
    - This function is for a Network representing a single structural element, i.e. with two end-points (leaves).
    """

    start = rs.PointCoordinates(rs.ObjectsByLayer(layer)[0])

    return network_order(start=start, structure=structure, network=network)



# def weld_meshes_from_layer(layer_input, layer_output):
#     """
#     Grab meshes on an input layer and weld them onto an output layer.

#     Parameters
#     ----------
#     layer_input : str
#         Layer containing the Rhino meshes to weld.
#     layer_output : str
#         Layer to plot single welded mesh.

#     Returns
#     -------
#     None

#     """

#     print('Welding meshes on layer:{0}'.format(layer_input))

#     mdl = CoreStructure(path=' ')

#     add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=layer_input)

#     faces = []

#     for element in mdl.elements.values():
#         enodes = element.nodes

#         if len(enodes) == 3:
#             enodes.append(enodes[-1])

#         if len(enodes) == 4:
#             faces.append(enodes)

#     rs.DeleteObjects(rs.ObjectsByLayer(layer_output))
#     rs.CurrentLayer(layer_output)
#     rs.AddMesh(mdl.nodes_xyz(), faces)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
