
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from compas_fea2.backends._base import model

from compas_fea2.utilities import plotvoxels
from compas_fea2.utilities import tets_from_vertices_faces
from compas_fea2.utilities import postprocess
from compas_fea2.utilities import discretise_faces
from compas_fea2.utilities import extrude_mesh
from compas_fea2.utilities import colorbar

from compas_blender.geometry import BlenderMesh
from compas_blender.utilities import create_layer
from compas_blender.utilities import clear_layer
from compas_blender.utilities import draw_cylinder
from compas_blender.utilities import draw_plane
from compas_blender.utilities import draw_line
from compas_blender.utilities import get_meshes
from compas_blender.utilities import get_objects
from compas_blender.utilities import get_points
from compas_blender.utilities import mesh_from_bmesh
from compas_blender.utilities import set_deselect
from compas_blender.utilities import set_select
from compas_blender.utilities import set_objects_coordinates
from compas_blender.utilities import get_object_property
from compas_blender.utilities import set_object_property
from compas_blender.utilities import draw_text
from compas_blender.utilities import xdraw_mesh

try:
    import bpy
except:
    pass

from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors


try:
    from numpy import array
    from numpy import hstack
    from numpy import max
    from numpy import newaxis
    from numpy import where
    from numpy.linalg import norm
except:
    pass

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'Modeller',
    'TroubleMaker'
]


class Modeller():
    """Initialises the Modeller object. This object operates on a compas_fea2
    Model object and changes its attributes using a Blender geometry as input.

    Parameters
    ----------
    model : obj
        compas_fea2 Model object.

    Attributes
    ----------

    """

    def __init__(self, model):
        self.model = model
        from importlib import import_module

        _backend = 'abaqus'
        _model = import_module('compas_fea2.backends.' + _backend + '.model')
        _problem = import_module(
            'compas_fea2.backends.' + _backend + '.problem')

    def add_nodes(self, ):
        pass

    def add_nodes_elements_from_bmesh(self, bmesh, line_type=None, mesh_type=None, thermal=False):
        """
        Adds the Blender mesh's nodes, edges and faces to the Structure object.

        Parameters
        ----------
        bmesh : obj
            Blender mesh object.
        line_type : str
            Element type for lines (bmesh edges).
        mesh_type : str
            Element type for meshes.
        thermal : bool
            Thermal properties on or off.

        Returns
        -------
        list
            Node keys that were added to the Structure.
        list
            Element keys that were added to the Structure.

        """

        blendermesh = BlenderMesh(bmesh)
        vertices = blendermesh.get_vertices_coordinates()
        edges = blendermesh.get_edges_vertex_indices()
        faces = blendermesh.get_faces_vertex_indices()

        added_nodes = set()
        added_elements = set()

        for xyz in vertices.values():

            node = self.model.add_node(xyz=xyz)
            added_nodes.add(node)

        if line_type and edges:

            ex = get_object_property(object=bmesh, property='ex')
            ey = get_object_property(object=bmesh, property='ey')
            axes = {'ex': list(ex) if ex else ex, 'ey': list(ey) if ey else ey}

            for u, v in edges.values():

                sp_xyz = vertices[u]
                ep_xyz = vertices[v]
                sp = structure.check_node_exists(sp_xyz)
                ep = structure.check_node_exists(ep_xyz)
                ez = subtract_vectors(ep_xyz, sp_xyz)
                if ex and not ey:
                    ey = cross_vectors(ex, ez)
                axes['ey'] = ey
                axes['ez'] = ez

                ekey = structure.add_element(
                    nodes=[sp, ep], type=line_type, thermal=thermal, axes=axes)

                if (line_type == 'BeamElement') and (ex is None):

                    if (abs(ez[0]) < 0.0001) and (abs(ez[1]) < 0.0001):

                        print(
                            '***** WARNING: vertical BeamElement with no ex axis, element {0} *****'.format(ekey))

                if ekey is not None:
                    added_elements.add(ekey)

        if mesh_type:

            if mesh_type in ['HexahedronElement', 'TetrahedronElement', 'SolidElement', 'PentahedronElement']:

                nodes = [structure.check_node_exists(i) for i in vertices]
                ekey = structure.add_element(
                    nodes=nodes, type=mesh_type, thermal=thermal)
                if ekey is not None:
                    added_elements.add(ekey)

            else:

                try:
                    ex = get_object_property(object=bmesh, property='ex')
                    ey = get_object_property(object=bmesh, property='ey')

                    if ex and ey:
                        ez = cross_vectors(ex, ey)
                    else:
                        ez = None

                except:
                    ex = None
                    ey = None
                    ez = None

                axes = {'ex': ex, 'ey': ey, 'ez': ez}

                for face in faces.values():

                    nodes = [structure.check_node_exists(
                        vertices[i]) for i in face]
                    ekey = structure.add_element(
                        nodes=nodes, type=mesh_type, thermal=thermal, axes=axes)
                    if ekey is not None:
                        added_elements.add(ekey)

        return list(added_nodes), list(added_elements)

    def add_nodes_elements_from_layers(structure, layers, line_type=None, mesh_type=None, thermal=False, pA=None, pL=None):
        """
        Adds node and element data from Blender layers to Structure object.

        Parameters
        ----------
        structure : obj
            Structure object to update.
        layers : list
            Layer string names to extract nodes and elements.
        line_type : str
            Element type for lines (bmesh edges).
        mesh_type : str
            Element type for meshes.
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

        added_nodes = set()
        added_elements = set()

        for layer in layers:

            elset = set()

            for bmesh in get_objects(layer=layer):

                # pA and pL

                nodes, elements = add_nodes_elements_from_bmesh(structure=structure, bmesh=bmesh, line_type=line_type,
                                                                mesh_type=mesh_type, thermal=thermal)
                added_nodes.update(nodes)
                added_elements.update(elements)
                elset.update(elements)

            structure.add_set(name=layer, type='element',
                              selection=list(elset))

        return list(added_nodes), list(added_elements)

    def add_nsets_from_layers(structure, layers):
        """
        Adds node sets from objects in layers.

        Parameters
        ----------
        structure : obj
            Structure object to update.
        layers : list
            Layers to get objects from.

        Returns
        -------
        None

        """

        if isinstance(layers, str):
            layers = [layers]

        for layer in layers:

            nodes = []

            for point in get_points(layer=layer):

                nodes.append(structure.check_node_exists(
                    xyz=list(point.location)))

            for mesh in get_meshes(layer=layer):

                for vertex in BlenderMesh(mesh).get_vertices_coordinates().values():

                    node = structure.check_node_exists(xyz=vertex)

                    if node is not None:
                        nodes.append(node)

            structure.add_set(name=layer, type='node', selection=nodes)

    def add_nset_from_meshes(structure, layer):
        """
        Adds the Blender meshes' vertices from a layer as a node set.

        Parameters
        ----------
        structure : obj
            Structure object to update.
        layer : str
            Layer to get meshes.

        Returns
        -------
        None

        """

        nodes = []

        for mesh in get_meshes(layer=layer):

            for vertex in BlenderMesh(mesh).get_vertices_coordinates().values():

                node = structure.check_node_exists(vertex)

                if node is not None:
                    nodes.append(node)

        structure.add_set(name=layer, type='node', selection=nodes)

    def add_tets_from_mesh(structure, name, mesh, draw_tets=False, volume=None, thermal=False):
        """
        Adds tetrahedron elements from a mesh to the Structure object.

        Parameters
        ----------
        structure : obj
            Structure object to update.
        name : str
            Name for the element set of tetrahedrons.
        mesh : obj
            The Blender mesh representing the outer surface.
        draw_tets : bool
            Layer to draw tetrahedrons on.
        volume : float
            Maximum volume for tets.
        thermal : bool
            Thermal properties on or off.

        Returns
        -------
        None

        """

        blendermesh = BlenderMesh(mesh)
        vertices = blendermesh.get_vertices_coordinates().values()
        faces = blendermesh.get_faces_vertex_indices().values()

        try:

            tets_points, tets_elements = tets_from_vertices_faces(
                vertices=vertices, faces=faces, volume=volume)

            for point in tets_points:
                structure.add_node(point)

            ekeys = []

            for element in tets_elements:

                nodes = [structure.check_node_exists(
                    tets_points[i]) for i in element]
                ekey = structure.add_element(
                    nodes=nodes, type='TetrahedronElement', thermal=thermal)
                ekeys.append(ekey)

            structure.add_set(name=name, type='element', selection=ekeys)

            if draw_tets:

                tet_faces = [[0, 1, 2], [1, 3, 2], [1, 3, 0], [0, 2, 3]]

                for i, points in enumerate(tets_elements):

                    xyz = [tets_points[j] for j in points]
                    xdraw_mesh(name=str(i), vertices=xyz,
                               faces=tet_faces, layer=draw_tets)

            print('***** MeshPy (TetGen) successfull *****')

        except:

            print('***** Error using MeshPy (TetGen) or drawing Tets *****')

    # TODO: move to _core
    def discretise_mesh(structure, mesh, layer, target, min_angle=15, factor=1):
        """
        Discretise a mesh from an input triangulated coarse mesh into small denser meshes.

        Parameters
        ----------
        structure : obj
            Structure object.
        mesh : obj
            The object of the Blender input mesh.
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

        blendermesh = BlenderMesh(mesh)
        vertices = list(blendermesh.get_vertices_coordinates().values())
        faces = list(blendermesh.get_faces_vertex_indices().values())

        try:

            points, tris = discretise_faces(vertices=vertices, faces=faces, target=target, min_angle=min_angle,
                                            factor=factor)

            for pts, tri in zip(points, tris):
                bmesh = xdraw_mesh(name='face', vertices=pts,
                                   faces=tri, layer=layer)
                add_nodes_elements_from_bmesh(
                    structure=structure, bmesh=bmesh, mesh_type='ShellElement')

        except:

            print('***** Error using MeshPy (Triangle) or drawing faces *****')


class TroubleMaker():
    """Creates a `compas_fea2` Problem object to be anaylized using a Blender
    geometry as input. The software used in the analysis is the one associated
    to the Model.

    """

    def __init__(self, model):
        self.model = model

    def add_point_load(self):
        pass

    def add_bcs(self):
        pass


# ==============================================================================
# Debugging
# ==============================================================================
if __name__ == "__main__":

    from compas_fea2.structure import Structure

    # mdl = Structure.load_from_obj(filename='/home/al/compas/compas_fea2/data/_workshop/example_tets.obj')
    # plot_voxels(mdl, step='step_load', field='smises', vdx=0.100)

    mdl = Structure.load_from_obj(filename='C:/Temp/block_tets.obj')
    plot_voxels(mdl, step='step_load', field='um', vdx=0.010)
