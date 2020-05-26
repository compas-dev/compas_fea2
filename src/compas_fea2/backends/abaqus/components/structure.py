
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from compas_fea.utilities import combine_all_sets
from compas_fea2.utilities import group_keys_by_attribute
from compas_fea2.utilities import group_keys_by_attributes

from compas_fea2.backends._core import StructureBase

from compas_fea2.backends.abaqus.components.mixins import NodeMixins
from compas_fea2.backends.abaqus.components.mixins import ElementMixins
from compas_fea2.backends.abaqus.components.mixins import ObjectMixins

# from compas_fea2.backends._core.bcs import *
from compas_fea2.backends.abaqus.components import Set

from compas_fea2.backends.abaqus.job.send_job import input_generate
from compas_fea2.backends.abaqus.job.send_job import launch_process
from compas_fea2.backends.abaqus.job.read_results import extract_data

import pickle
import os


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
        'Structure',
        ]


class Structure(StructureBase, ObjectMixins, ElementMixins, NodeMixins):

    def __init__(self, path, name='abaqus-Structure'):
        super(Structure, self).__init__(path, name)
        self.sets = {}


    #TODO try to reduce duplicate code
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
        elset : str
            Name of element set to create.

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

        if elset:
            self.add_set(name=elset, type='element', selection=ekeys)

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
        elset : str
            Name of element set to create.
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

        if elset:
            self.add_set(name=elset, type='element', selection=ekeys)

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
        elset : str
            Name of element set to create.
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
            ekeys.append(self.add_element(nodes=nkeys, type=element_type, acoustic=acoustic, thermal=thermal, axes=axes))
        if elset:
            self.add_set(name=elset, type='element', selection=ekeys)

        return ekeys

    # ==============================================================================
    # Sets
    # ==============================================================================

    def add_set(self, name, type, selection):

        """ Adds a node, element or surface set to structure.sets.

        Parameters
        ----------
        name : str
            Name of the Set.
        type : str
            'node', 'element', 'surface_node', surface_element'.
        selection : list, dict
            The integer keys of the nodes, elements or the element numbers and sides.

        Returns
        -------
        None

        """

        if isinstance(selection, int):
            selection = [selection]

        self.sets[name] = Set(name=name, type=type, selection=selection, index=len(self.sets))


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
            Extract 'all' or a node set/list.

        Returns
        -------
        dict
            The nodal results for the requested field.

        """

        data  = {}
        rdict = self.results[step]['nodal']

        if nodes == 'all':
            keys = list(self.nodes.keys())

        elif isinstance(nodes, str):
            keys = self.sets[nodes].selection

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
            Extract 'all' or an element set/list.

        Returns
        -------
        dict
            The element results for the requested field.

        """

        data  = {}
        rdict = self.results[step]['element']

        if elements == 'all':
            keys = list(self.elements.keys())

        elif isinstance(elements, str):
            keys = self.sets[elements].selection

        else:
            keys = elements

        for key in keys:
            data[key] = rdict[field][key]

        return data

    def write_input_file(self, fields='u', output=True, save=False):

        """ Writes abaqus input file.

        Parameters
        ----------
        fields : list, str
            Data field requests.
        output : bool
            Print terminal output.
        save : bool
            Save structure to .obj before file writing.

        Returns
        -------
        None

        """

        if save:
            self.save_to_cfea()

        input_generate(self, fields=fields, output=output)


    def analyse(self, exe=None, cpus=4, license='research', delete=True, output=True, umat=False):

        """ Runs the analysis through abaqus.

        Parameters
        ----------

        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        license : str
            Software license type: 'research', 'student'.
        delete : bool
            -
        output : bool
            Print terminal output.

        Returns
        -------
        None

        """

        cpus = 1 if license == 'student' else cpus
        launch_process(self, exe=exe, cpus=cpus, output=output, umat=umat)


    def extract_data(self, fields='u', steps='all', exe=None, sets=None, license='research', output=True,
                     return_data=True, components=None):

        """ Extracts data from the analysis output files.

        Parameters
        ----------
        software : str
            Analysis software / library to use, 'abaqus', 'opensees' or 'ansys'.
        fields : list, str
            Data field requests.
        steps : list
            Loads steps to extract from.
        exe : str
            Full terminal command to bypass subprocess defaults.
        sets : list
            -
        license : str
            Software license type: 'research', 'student'.
        output : bool
            Print terminal output.
        return_data : bool
            Return data back into structure.results.
        components : list
            Specific components to extract from the fields data.

        Returns
        -------
        None

        """

        extract_data(self, fields=fields, exe=exe, output=output, return_data=return_data,
                            components=components)


    def analyse_and_extract(self, fields='u', exe=None, cpus=4, license='research', output=True, save=False,
                            return_data=True, components=None, umat=False):

        """ Runs the analysis through the chosen FEA software / library and extracts data.

        Parameters
        ----------
        software : str
            Analysis software / library to use, 'abaqus', 'opensees' or 'ansys'.
        fields : list, str
            Data field requests.
        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        license : str
            Software license type: 'research', 'student'.
        output : bool
            Print terminal output.
        save : bool
            Save the structure to .obj before writing.
        return_data : bool
            Return data back into structure.results.
        components : list
            Specific components to extract from the fields data.

        Returns
        -------
        None

        """

        self.write_input_file(fields=fields, output=output, save=save)

        self.analyse(exe=exe, cpus=cpus, license=license, output=output, umat=umat)

        self.extract_data(fields=fields, exe=exe, license=license, output=output,
                          return_data=return_data, components=components)

