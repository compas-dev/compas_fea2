
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from compas_fea.utilities import combine_all_sets
from compas_fea2.utilities import group_keys_by_attribute
from compas_fea2.utilities import group_keys_by_attributes

from compas_fea2._core.mixins.nodemixins import cNodeMixins
from compas_fea2._core.mixins.elementmixins import cElementMixins
from compas_fea2._core.mixins.objectmixins import cObjectMixins
# from compas_fea2._core.bcs import *

import pickle
import os


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
        'cStructure',
        ]


class cStructure(cObjectMixins, cElementMixins, cNodeMixins):

    """ Initialises Structure object for use in finite element analysis.

    Parameters
    ----------
    path : str
        Path to save all compas_fea associated files.
    name : str
        Name of the structure.

    Attributes
    ----------
    constraints : dict
        Constraint objects.
    displacements : dict
        Displacement objects.
    elements : dict
        Element objects.
    element_index : dict
        Index of elements (element centroid geometric keys).
    element_properties : dict
        ElementProperties objects.
    interactions : dict
        Interaction objects.
    loads : dict
        Load objects.
    materials : dict
        Material objects.
    misc : dict
        Misc objects.
    name : str
        Structure name.
    nodes : dict
        Node objects.
    node_index : dict
        Index of nodes (node geometric keys).
    path : str
        Path to save files.
    results : dict
        Dictionary containing analysis results.
    sections : dict
        Section objects.
    sets : dict
        Set objects.
    steps : dict
        Step objects.
    steps_order : list
        Sorted list of Step object names.
    tol : str
        Geometric key tolerance.
    virtual_nodes : dict
        Node objects for virtual nodes.
    virtual_elements : dict
        Element objects for virtual elements.
    virtual_element_index : dict
        Index of virtual elements (element centroid geometric keys).

    """
    # TODO move sets from here to abaqus
    def __init__(self, path, name='compas_fea-Structure'):

        self.constraints           = {}
        self.displacements         = {}
        self.elements              = {}
        self.element_index         = {}
        self.element_properties    = {}
        self.interactions          = {}
        self.loads                 = {} #TODO add cases and combos (change numbering)
        self.materials             = {}
        self.misc                  = {}
        self.name                  = name
        self.nodes                 = {}
        self.node_index            = {}
        self.path                  = path
        self.results               = {}
        self.sections              = {}
        # self.collections           = {} #TODO maybe add 'collections'
        self.steps                 = {}
        self.steps_order           = []
        self.tol                   = '3'
        self.virtual_nodes         = {}
        self.virtual_node_index    = {}
        self.virtual_elements      = {}
        self.virtual_element_index = {}

    # TODO move sets from here to abaqus
    def __str__(self):

        n = self.node_count()
        m = self.element_count()
        data = [
            # self.collections,
            self.materials,
            self.sections,
            self.loads,
            self.displacements,
            self.constraints,
            self.interactions,
            self.misc,
            self.steps,
        ]

        d = []

        for entry in data:

            if entry:
                d.append('\n'.join(['  {0} : {1}'.format(i, j.__name__) for i, j in entry.items()]))
            else:
                d.append('n/a')

        return """

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea Structure: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Nodes
-----
{}

Elements
--------
{}


Materials
---------
{}

Sections
--------
{}

Loads
-----
{}

Displacements
-------------
{}

Constraints
-----------
{}

Interactions
------------
{}

Misc
----
{}

Steps
-----
{}

""".format(self.name, n, m, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])


    def add_nodes_elements_from_mesh(self, mesh, element_type, thermal=False, elset=None):

        """ Adds the nodes and faces of a Mesh to the Structure object.

        Parameters
        ----------
        mesh : obj
            Mesh datastructure object.
        element_type : str
            Element type: 'ShellElement', 'MembraneElement' etc.
        thermal : bool
            Thermal properties on or off.

        Returns
        -------
        list
            Keys of the created elements.

        """

        for key in sorted(list(mesh.vertices()), key=int):
            self.add_node(mesh.vertex_coordinates(key))

        ekeys = []

        for fkey in list(mesh.faces()):
            face = [self.check_node_exists(mesh.vertex_coordinates(i)) for i in mesh.face[fkey]]
            ekeys.append(self.add_element(nodes=face, type=element_type, thermal=thermal))

        return ekeys


    def add_nodes_elements_from_network(self, network, element_type, thermal=False, elset=None, axes={}):

        """ Adds the nodes and edges of a Network to the Structure object.

        Parameters
        ----------
        network : obj
            Network datastructure object.
        element_type : str
            Element type: 'BeamElement', 'TrussElement' etc.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez' for all elements.

        Returns
        -------
        list
            Keys of the created elements.

        """

        for key in sorted(list(network.nodes()), key=int):
            self.add_node(network.node_coordinates(key))

        ekeys = []

        for u, v in list(network.edges()):
            sp = self.check_node_exists(network.node_coordinates(u))
            ep = self.check_node_exists(network.node_coordinates(v))
            ekeys.append(self.add_element(nodes=[sp, ep], type=element_type, thermal=thermal, axes=axes))

        return ekeys


    def add_nodes_elements_from_volmesh(self, volmesh, element_type='SolidElement', thermal=False, elset=None, axes={}):

        """ Adds the nodes and cells of a VolMesh to the Structure object.

        Parameters
        ----------
        volmesh : obj
            VolMesh datastructure object.
        element_type : str
            Element type: 'SolidElement' or ....
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez' for all elements.

        Returns
        -------
        list
            Keys of the created elements.

        """

        for key in sorted(list(volmesh.vertices()), key=int):
            self.add_node(volmesh.vertex_coordinates(key))

        ekeys = []

        for ckey in volmesh.cell:
            cell_vertices = volmesh.cell_vertices(ckey)
            nkeys = [self.check_node_exists(volmesh.vertex_coordinates(nk)) for nk in cell_vertices]
            ekeys.append(self.add_element(nodes=nkeys, type=element_type, acoustic=acoustic, thermal=thermal,axes=axes))

        return ekeys


    # ==============================================================================
    # Modifiers
    # ==============================================================================

    def scale_displacements(self, displacements, factor):

        """ Scales displacements by a given factor.

        Parameters
        ----------
        displacements : dict
            Dictionary containing the displacements to scale.
        factor : float
            Factor to scale the displacements by.

        Returns
        -------
        dict
            The scaled displacements dictionary.

        """

        disp_dic = {}

        for key, disp in displacements.items():
            for dkey, dcomp in disp.components.items():
                if dcomp is not None:
                    disp.components[dkey] *= factor
            disp_dic[key] = disp

        return disp_dic


    def scale_loads(self, loads, factor):

        """ Scales loads by a given factor.

        Parameters
        ----------
        loads : dict
            Dictionary containing the loads to scale.
        factor : float
            Factor to scale the loads by.

        Returns
        -------
        dict
            The scaled loads dictionary.

        """

        loads_dic = {}

        for key, load in loads.items():
            for lkey, lcomp in load.components.items():
                if lcomp is not None:
                    load.components[lkey] *= factor
            loads_dic[key] = load

        return loads_dic

    # ==============================================================================
    # Steps
    # ==============================================================================

    def set_steps_order(self, order):

        """ Sets the order that the Steps will be analysed.

        Parameters
        ----------
        order : list
            An ordered list of the Step names.

        Returns
        -------
        None

        """

        self.steps_order = order


    # ==============================================================================
    # Results
    # ==============================================================================

    def get_nodal_results(self, step, field, nodes='all'):

        """ Extract nodal results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        nodes : str, list
            Extract 'all' or a node collection/list.

        Returns
        -------
        dict
            The nodal results for the requested field.

        """

        data  = {}
        rdict = self.results[step]['nodal']

        if nodes == 'all':
            keys = list(self.nodes.keys())

        # elif isinstance(nodes, str):              TODO: transfor to 'collection'
        #     keys = self.sets[nodes].selection

        else:
            keys = nodes

        for key in keys:
            data[key] = rdict[field][key]

        return data


    def get_element_results(self, step, field, elements='all'):

        """ Extract element results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        elements : str, list
            Extract 'all' or an element collection/list.

        Returns
        -------
        dict
            The element results for the requested field.

        """

        data  = {}
        rdict = self.results[step]['element']

        if elements == 'all':
            keys = list(self.elements.keys())

        # elif isinstance(elements, str):              TODO: transfor to 'collection'
        #     keys = self.sets[elements].selection

        else:
            keys = elements

        for key in keys:
            data[key] = rdict[field][key]

        return data


    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):

        """ Prints a summary of the Structure object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        print(self)


    # ==============================================================================
    # Save
    # ==============================================================================

    def save_to_cfea(self, output=True):

        """ Exports the Structure object to an .obj file through Pickle.

        Parameters
        ----------
        output : bool
            Print terminal output.

        Returns
        -------
        None

        """

        filename = os.path.join(self.path, self.name + '.cfea')

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        if output:
            print('***** Structure saved to: {0} *****\n'.format(filename))


    # ==============================================================================
    # Load
    # ==============================================================================

    @staticmethod
    def load_from_cfea(filename, output=True):

        """ Imports a Structure object from an .obj file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Structure .obj from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Structure object.

        """

        with open(filename, 'rb') as f:
            structure = pickle.load(f)

        if output:
            print('***** Structure loaded from: {0} *****'.format(filename))

        return structure
