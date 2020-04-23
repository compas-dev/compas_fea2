# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from compas_rhino.geometry import RhinoMesh
except:
    pass

from compas.datastructures.mesh import Mesh
from compas.datastructures import Network
from compas.geometry import add_vectors
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.rpc import Proxy

from compas_fea2 import utilities
from compas_fea2.utilities import colorbar
from compas_fea2.preprocess import extrude_mesh
from compas_fea2.utilities import network_order

# NOTE this can be tricky!!
from compas_fea2._core import CoreStructure
# from compas_fea2.backends.abaqus.structure import Structure


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
# meshing   = Proxy('compas_fea2.preprocess.meshing')


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'plot_reaction_forces',
    'plot_concentrated_forces',
    'plot_mode_shapes',
    'plot_volmesh',
    'plot_axes',
    'plot_data',
    'plot_principal_stresses',
    'plot_voxels',
    'weld_meshes_from_layer',
]


def plot_reaction_forces(structure, step, layer=None, scale=1.0):
    """
    Plots reaction forces for the Structure analysis results.

    Parameters
    ----------
    structure : obj
        Structure object.
    step : str
        Name of the Step.
    layer : str
        Layer name for plotting.
    scale : float
        Scale of the arrows.

    Returns
    -------
    None

    """

    if not layer:
        layer = '{0}-{1}'.format(step, 'reactions')

    rs.CurrentLayer(rs.AddLayer(layer))
    rs.DeleteObjects(rs.ObjectsByLayer(layer))
    rs.EnableRedraw(False)

    rfx = structure.results[step]['nodal']['rfx']
    rfy = structure.results[step]['nodal']['rfy']
    rfz = structure.results[step]['nodal']['rfz']

    nkeys = rfx.keys()
    v     = [scale_vector([rfx[i], rfy[i], rfz[i]], -scale * 0.001) for i in nkeys]
    rm    = [length_vector(i) for i in v]
    rmax  = max(rm)
    nodes = structure.nodes_xyz(nkeys)

    for i in nkeys:

        if rm[i] > 0.001:
            l = rs.AddLine(nodes[i], add_vectors(nodes[i], v[i]))
            rs.CurveArrows(l, 1)
            col = [int(j) for j in colorbar(rm[i] / rmax, input='float', type=255)]
            rs.ObjectColor(l, col)
            vector = [rfx[i], rfy[i], rfz[i]]
            name = json.dumps({'rfx': rfx[i], 'rfy': rfy[i], 'rfz': rfz[i], 'rfm': length_vector(vector)})
            rs.ObjectName(l, '_' + name)

    rs.CurrentLayer(rs.AddLayer('Default'))
    rs.LayerVisible(layer, False)
    rs.EnableRedraw(True)


def plot_concentrated_forces(structure, step, layer=None, scale=1.0):
    """
    Plots concentrated forces forces for the Structure analysis results.

    Parameters
    ----------
    structure : obj
        Structure object.
    step : str
        Name of the Step.
    layer : str
        Layer name for plotting.
    scale : float
        Scale of the arrows.

    Returns
    -------
    None

    """

    if not layer:
        layer = '{0}-{1}'.format(step, 'forces')
    rs.CurrentLayer(rs.AddLayer(layer))
    rs.DeleteObjects(rs.ObjectsByLayer(layer))
    rs.EnableRedraw(False)

    cfx = structure.results[step]['nodal']['cfx']
    cfy = structure.results[step]['nodal']['cfy']
    cfz = structure.results[step]['nodal']['cfz']

    nkeys = cfx.keys()
    v = [scale_vector([cfx[i], cfy[i], cfz[i]], -scale * 0.001) for i in nkeys]
    rm = [length_vector(i) for i in v]
    rmax = max(rm)
    nodes = structure.nodes_xyz(nkeys)

    for i in nkeys:

        if rm[i]:
            l = rs.AddLine(nodes[i], add_vectors(nodes[i], v[i]))
            rs.CurveArrows(l, 1)
            col = [int(j) for j in colorbar(rm[i] / rmax, input='float', type=255)]
            rs.ObjectColor(l, col)
            vector = [cfx[i], cfy[i], cfz[i]]
            name = json.dumps({'cfx': cfx[i], 'cfy': cfy[i], 'cfz': cfz[i], 'cfm': length_vector(vector)})
            rs.ObjectName(l, '_' + name)

    rs.CurrentLayer(rs.AddLayer('Default'))
    rs.LayerVisible(layer, False)
    rs.EnableRedraw(True)


def plot_mode_shapes(structure, step, layer=None, scale=1.0, radius=1):
    """
    Plots modal shapes from structure.results.

    Parameters
    ----------
    structure : obj
        Structure object.
    step : str
        Name of the Step.
    layer : str
        Each mode will be placed in a layer with this string prefix.
    scale : float
        Scale displacements for the deformed plot.
    radius : float
        Radius of the pipe visualisation meshes.

    Returns
    -------
    None

    """

    if not layer:
        layer = step + '_mode_'

    try:
        it = structure.results[step]['frequencies']
    except:
        it = structure.results[step]['info']['description']

    if isinstance(it, list):
        for c, fk in enumerate(it, 1):
            layerk = layer + str(c)
            plot_data(structure=structure, step=step, field='um', layer=layerk, scale=scale, mode=c, radius=radius)

    elif isinstance(it, dict):
        for mode, value in it.items():
            print(mode, value)
            layerk = layer + str(mode)
            plot_data(structure=structure, step=step, field='um', layer=layerk, scale=scale, mode=mode, radius=radius)


def plot_volmesh(volmesh, layer=None, draw_cells=True):

    """
    Plot a volmesh datastructure.

    Parameters
    ----------
    volmesh : obj
        volmesh datastructure object.
    layer : str
        Layer name to draw on.
    draw_cells : bool
        Draw cells.

    Returns
    -------
    None

    """

    if layer:
        rs.CurrentLayer(layer)

    vkeys    = sorted(list(volmesh.vertices()), key=int)
    vertices = [volmesh.vertex_coordinates(vkey) for vkey in vkeys]

    if draw_cells:
        meshes = []
        for ckey in volmesh.cell:
            faces = [volmesh.halfface_vertices(fk, ordered=True) for fk in volmesh.cell_halffaces(ckey)]
            meshes.append(rs.AddMesh(vertices, faces))
        return meshes

    else:
        faces = []
        for fk in volmesh.halfface:
            face = volmesh.halfface_vertices(fk, ordered=True)
            faces.append(face)
        mesh = rs.AddMesh(vertices, faces)
        return mesh


def plot_axes(xyz, e11, e22, e33, layer, sc=1):
    """
    Plots a set of axes.

    Parameters
    ----------
    xyz : list
        Origin of the axes.
    e11 : list
        Normalised first axis component [x1, y1, z1].
    e22 : list
        Normalised second axis component [x2, y2, z2].
    e33 : list
        Normalised third axis component [x3, y3, z3].
    layer : str
        Layer to plot on.
    sc : float
         Size of the axis lines.

    Returns
    -------
    None

    """

    ex = rs.AddLine(xyz, add_vectors(xyz, scale_vector(e11, sc)))
    ey = rs.AddLine(xyz, add_vectors(xyz, scale_vector(e22, sc)))
    ez = rs.AddLine(xyz, add_vectors(xyz, scale_vector(e33, sc)))

    rs.ObjectColor(ex, [255, 0, 0])
    rs.ObjectColor(ey, [0, 255, 0])
    rs.ObjectColor(ez, [0, 0, 255])
    rs.ObjectLayer(ex, layer)
    rs.ObjectLayer(ey, layer)
    rs.ObjectLayer(ez, layer)


def plot_data(structure, step, field='um', layer=None, scale=1.0, radius=0.05, cbar=[None, None], iptype='mean',
              nodal='mean', mode='', cbar_size=1):
    """
    Plots analysis results on the deformed shape of the Structure.

    Parameters
    ----------
    structure : obj
        Structure object.
    step : str
        Name of the Step.
    field : str
        Field to plot, e.g. 'um', 'sxx', 'sm1'.
    layer : str
        Layer name for plotting.
    scale : float
        Scale on displacements for the deformed plot.
    radius : float
        Radius of the pipe visualisation meshes.
    cbar : list
        Minimum and maximum limits on the colorbar.
    iptype : str
        'mean', 'max' or 'min' of an element's integration point data.
    nodal : str
        'mean', 'max' or 'min' for nodal values.
    mode : int
        Mode or frequency number to plot, for modal, harmonic or buckling analysis.
    cbar_size : float
        Scale on the size of the colorbar.

    Returns
    -------
    None

    Notes
    -----
    - Pipe visualisation of line elements is not based on the element section.

    """

    if field in ['smaxp', 'smises']:
        nodal  = 'max'
        iptype = 'max'

    elif field in ['sminp']:
        nodal  = 'min'
        iptype = 'min'

    # Create and clear Rhino layer

    if not layer:
        layer = '{0}-{1}{2}'.format(step, field, mode)

    rs.CurrentLayer(rs.AddLayer(layer))
    rs.DeleteObjects(rs.ObjectsByLayer(layer))
    rs.EnableRedraw(False)

    # Node and element data

    nodes      = structure.nodes_xyz()
    elements   = [structure.elements[i].nodes for i in sorted(structure.elements, key=int)]
    nodal_data = structure.results[step]['nodal']
    nkeys      = sorted(structure.nodes, key=int)

    ux = [nodal_data['ux{0}'.format(mode)][i] for i in nkeys]
    uy = [nodal_data['uy{0}'.format(mode)][i] for i in nkeys]
    uz = [nodal_data['uz{0}'.format(mode)][i] for i in nkeys]

    try:
        data  = [nodal_data['{0}{1}'.format(field, mode)][i] for i in nkeys]
        dtype = 'nodal'

    except(Exception):
        data  = structure.results[step]['element'][field]
        dtype = 'element'

    # Postprocess

    result = functions.postprocess(nodes, elements, ux, uy, uz, data, dtype, scale, cbar, 255, iptype, nodal)

    print("worked here: 1")

    try:
        toc, U, cnodes, fabs, fscaled, celements, eabs = result
        print('\n***** Data processed : {0} s *****'.format(toc))

        # Plot meshes

        mesh_faces  = []
        line_faces  = [[0, 4, 5, 1], [1, 5, 6, 2], [2, 6, 7, 3], [3, 7, 4, 0]]
        block_faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
        tet_faces   = [[0, 2, 1, 1], [1, 2, 3, 3], [1, 3, 0, 0], [0, 3, 2, 2]]

        for element, nodes in enumerate(elements):

            n = len(nodes)

            if n == 2:

                u, v = nodes
                sp, ep = U[u], U[v]
                plane = rs.PlaneFromNormal(sp, subtract_vectors(ep, sp))
                xa = plane.XAxis
                ya = plane.YAxis
                r = radius
                xa_pr = scale_vector(xa, +r)
                xa_mr = scale_vector(xa, -r)
                ya_pr = scale_vector(ya, +r)
                ya_mr = scale_vector(ya, -r)
                pts = [add_vectors(sp, xa_pr), add_vectors(sp, ya_pr),
                       add_vectors(sp, xa_mr), add_vectors(sp, ya_mr),
                       add_vectors(ep, xa_pr), add_vectors(ep, ya_pr),
                       add_vectors(ep, xa_mr), add_vectors(ep, ya_mr)]
                guid = rs.AddMesh(pts, line_faces)

                if dtype == 'element':
                    col1 = col2 = celements[element]

                elif dtype == 'nodal':
                    col1 = cnodes[u]
                    col2 = cnodes[v]

                rs.MeshVertexColors(guid, [col1] * 4 + [col2] * 4)

            elif n == 3:

                mesh_faces.append(nodes + [nodes[-1]])

            elif n == 4:

                if structure.elements[element].__name__ in ['ShellElement', 'MembraneElement']:
                    mesh_faces.append(nodes)
                else:
                    for face in tet_faces:
                        mesh_faces.append([nodes[i] for i in face])

            elif n == 8:

                for block in block_faces:
                    mesh_faces.append([nodes[i] for i in block])

        if mesh_faces:
            guid = rs.AddMesh(U, mesh_faces)
            rs.MeshVertexColors(guid, cnodes)

        # Plot colorbar

        xr, yr, _ = structure.node_bounds()
        yran = yr[1] - yr[0] if yr[1] - yr[0] else 1
        s    = yran * 0.1 * cbar_size
        xmin = xr[1] + 3 * s
        ymin = yr[0]

        xl = [xmin, xmin + s]
        yl = [ymin + i * s for i in range(11)]
        verts = [[xi, yi, 0] for xi in xl for yi in yl]
        faces = [[i, i + 1, i + 12, i + 11] for i in range(10)]
        id = rs.AddMesh(verts, faces)

        y  = [i[1] for i in verts]
        yn = yran * cbar_size
        colors = [colorbar(2 * (yi - ymin - 0.5 * yn) / yn, input='float', type=255) for yi in y]
        rs.MeshVertexColors(id, colors)

        h = 0.4 * s

        for i in range(5):

            x0 = xmin + 1.2 * s
            yu = ymin + (5.8 + i) * s
            yl = ymin + (3.8 - i) * s
            vu = float(+max(eabs, fabs) * (i + 1) / 5.)
            vl = float(-max(eabs, fabs) * (i + 1) / 5.)
            rs.AddText('{0:.5g}'.format(vu), [x0, yu, 0], height=h)
            rs.AddText('{0:.5g}'.format(vl), [x0, yl, 0], height=h)

        rs.AddText('0', [x0, ymin + 4.8 * s, 0], height=h)
        rs.AddText('Step:{0}   Field:{1}'.format(step, field), [xmin, ymin + 12 * s, 0], height=h)

        if mode != '':
            try:
                freq = str(round(structure.results[step]['frequencies'][mode - 1], 3))
                rs.AddText('Mode:{0}   Freq:{1}Hz'.format(mode, freq), [xmin, ymin - 1.5 * s, 0], height=h)
            except:
                pass

        # Return to Default layer

        rs.CurrentLayer(rs.AddLayer('Default'))
        rs.LayerVisible(layer, False)
        rs.EnableRedraw(True)

    except:

        print('\n***** Error encountered during data processing or plotting *****')


def plot_principal_stresses(structure, step, ptype, scale, rotate=0, layer=None):
    """
    Plots the principal stresses of the elements.

    Parameters
    ----------
    structure : obj
        Structure object.
    step : str
        Name of the Step.
    ptype : str
        'max' or 'min' for maximum or minimum principal stresses.
    scale : float
        Scale on the length of the line markers.
    rotate : int
        Rotate lines by 90 deg, 0 or 1.
    layer : str
        Layer name for plotting.

    Returns
    -------
    None

    Notes
    -----
    - Currently an alpha script and only for triangular shell elements in Abaqus.
    - Centroids are taken on the undeformed geometry.

    """

    data    = structure.results[step]['element']
    result  = functions.principal_stresses(data, ptype, scale, rotate)

    try:

        vec1, vec5, pr1, pr5, pmax = result

        if not layer:
            layer = '{0}_principal_{1}'.format(step, ptype)
        rs.CurrentLayer(rs.AddLayer(layer))
        rs.DeleteObjects(rs.ObjectsByLayer(layer))
        rs.EnableRedraw(False)

        centroids = [structure.element_centroid(i) for i in sorted(structure.elements, key=int)]

        for c, centroid in enumerate(centroids):

            v1   = vec1[c]
            v5   = vec5[c]
            id1  = rs.AddLine(add_vectors(centroid, scale_vector(v1, -1)), add_vectors(centroid, v1))
            id5  = rs.AddLine(add_vectors(centroid, scale_vector(v5, -1)), add_vectors(centroid, v5))
            col1 = colorbar(pr1[c] / pmax, input='float', type=255)
            col5 = colorbar(pr5[c] / pmax, input='float', type=255)

            rs.ObjectColor(id1, col1)
            rs.ObjectColor(id5, col5)

        rs.EnableRedraw(True)

    except:

        print('\n***** Error calculating or plotting principal stresses *****')


def plot_voxels(structure, step, field='smises', cbar=[None, None], iptype='mean', nodal='mean', vdx=None, mode=''):
    """
    Voxel 4D visualisation.

    Parameters
    ----------
    structure : obj
        Structure object.
    step : str
        Name of the Step.
    field : str
        Field to plot, e.g. 'smises'.
    cbar : list
        Minimum and maximum limits on the colorbar.
    iptype : str
        'mean', 'max' or 'min' of an element's integration point data.
    nodal : str
        'mean', 'max' or 'min' for nodal values.
    vdx : float
        Voxel spacing.
    mode : int
        mode or frequency number to plot, in case of modal, harmonic or buckling analysis.

    Returns
    -------
    None

    """

    # Node and element data

    xyz        = structure.nodes_xyz()
    elements   = [structure.elements[i].nodes for i in sorted(structure.elements, key=int)]
    nodal_data = structure.results[step]['nodal']
    nkeys      = sorted(structure.nodes, key=int)

    ux = [nodal_data['ux{0}'.format(mode)][i] for i in nkeys]
    uy = [nodal_data['uy{0}'.format(mode)][i] for i in nkeys]
    uz = [nodal_data['uz{0}'.format(mode)][i] for i in nkeys]

    try:
        data = [nodal_data[field + str(mode)][key] for key in nkeys]
        dtype = 'nodal'

    except(Exception):
        data = structure.results[step]['element'][field]
        dtype = 'element'

    # Postprocess

    result = functions.postprocess(xyz, elements, ux, uy, uz, data, dtype, 1, cbar, 255, iptype, nodal)

    try:
        toc, U, cnodes, fabs, fscaled, celements, eabs = result
        print('\n***** Data processed : {0} s *****'.format(toc))

    except:
        print('\n***** Error post-processing *****')

    try:
        functions.plotvoxels(values=fscaled, U=U, vdx=vdx)
        print('\n***** Voxels finished *****')

    except:
        print('\n***** Error plotting voxels *****')


def weld_meshes_from_layer(layer_input, layer_output):
    """
    Grab meshes on an input layer and weld them onto an output layer.

    Parameters
    ----------
    layer_input : str
        Layer containing the Rhino meshes to weld.
    layer_output : str
        Layer to plot single welded mesh.

    Returns
    -------
    None

    """

    print('Welding meshes on layer:{0}'.format(layer_input))

    mdl = CoreStructure(path=' ')

    add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=layer_input)

    faces = []

    for element in mdl.elements.values():
        enodes = element.nodes

        if len(enodes) == 3:
            enodes.append(enodes[-1])

        if len(enodes) == 4:
            faces.append(enodes)

    rs.DeleteObjects(rs.ObjectsByLayer(layer_output))
    rs.CurrentLayer(layer_output)
    rs.AddMesh(mdl.nodes_xyz(), faces)

# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
