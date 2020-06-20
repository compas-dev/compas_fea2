from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

# from compas_fea.utilities import combine_all_sets
from compas_fea2.utilities import group_keys_by_attribute
from compas_fea2.utilities import group_keys_by_attributes

from compas_fea2.backends._core import StructureBase

from compas_fea2.backends.abaqus.components import Set
from compas_fea2.backends.abaqus.components.elements import *
from compas_fea2.backends.abaqus.job.send_job import launch_process
from compas_fea2.backends.abaqus.job.read_results import extract_data

from compas_fea2.backends.abaqus.writer import Writer

# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'Structure',
]


ETYPES = {
    'BeamElement':        BeamElement,
    'SpringElement':      SpringElement,
    'TrussElement':       TrussElement,
    'StrutElement':       StrutElement,
    'TieElement':         TieElement,
    'ShellElement':       ShellElement,
    'MembraneElement':    MembraneElement,
    'FaceElement':        FaceElement,
    'SolidElement':       SolidElement,
    'TetrahedronElement': TetrahedronElement,
    'PentahedronElement': PentahedronElement,
    'HexahedronElement':  HexahedronElement,
    'MassElement':        MassElement
}


class Structure(StructureBase):

    def __init__(self, name, parts, assembly, interactions, steps):
        super(Structure, self).__init__(name)
        self.parts = parts
        self.assembly = assembly


    # # ==============================================================================
    # # Elements
    # # ==============================================================================

    # def add_nodal_element(self, node, type, virtual_node=False):
    #     """Adds a nodal element to structure.elements with the possibility of
    #     adding a coincident virtual node. Virtual nodes are added to a node
    #     set called 'virtual_nodes'.

    #     Parameters
    #     ----------
    #     node : int
    #         Node number the element is connected to.
    #     type : str
    #         Element type: 'SpringElement'.
    #     virtual_node : bool
    #         Create a virtual node or not.

    #     Returns
    #     -------
    #     int
    #         Key of the added element.

    #     Notes
    #     -----
    #     - Elements are numbered sequentially starting from 0.

    #     """
    #     if virtual_node:
    #         xyz = self.node_xyz(node)
    #         key = self.virtual_nodes.setdefault(node, self.node_count())
    #         self.nodes[key] = {'x': xyz[0], 'y': xyz[1], 'z': xyz[2],
    #                            'ex': [1, 0, 0], 'ey': [0, 1, 0], 'ez': [0, 0, 1], 'virtual': True}
    #         if 'virtual_nodes' in self.sets:
    #             self.sets['virtual_nodes']['selection'].append(key)
    #         else:
    #             self.sets['virtual_nodes'] = {'type': 'node', 'selection': [key], 'explode': False}
    #         nodes = [node, key]
    #     else:
    #         nodes = [node]

    #     func_dict = {
    #         'SpringElement': SpringElement,
    #     }

    #     ekey = self.element_count()
    #     element = func_dict[type]()
    #     element.nodes = nodes
    #     element.number = ekey
    #     self.elements[ekey] = element
    #     return ekey

    # def add_virtual_element(self, nodes, type, thermal=False, axes={}):
    #     """Adds a virtual element to structure.elements and to element set 'virtual_elements'.

    #     Parameters
    #     ----------
    #     nodes : list
    #         Nodes the element is connected to.
    #     type : str
    #         Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez'.

    #     Returns
    #     -------
    #     int
    #         Key of the added virtual element.

    #     Notes
    #     -----
    #     - Virtual elements are numbered sequentially starting from 0.

    #     """
    #     ekey = self.check_element_exists(nodes, virtual=True)

    #     if ekey is None:
    #         ekey            = self.element_count()
    #         element         = func_dict[type]()
    #         element.axes    = axes
    #         element.nodes   = nodes
    #         element.number  = ekey
    #         element.thermal = thermal

    #         self.virtual_elements[ekey] = element
    #         self.add_element_to_element_index(ekey, nodes, virtual=True)

    #         if 'virtual_elements' in self.sets:
    #             self.sets['virtual_elements']['selection'].append(ekey)
    #         else:
    #             self.sets['virtual_elements'] = {'type': 'virtual_element', 'selection': [ekey],
    #                                              'index': len(self.sets)}
    #     return ekey

    # def assign_element_property(self, element_property):
    #     """Assign the ElementProperties object name to associated Elements.

    #     Parameters
    #     ----------
    #     element_property : obj
    #         ElementProperties object.

    #     Returns
    #     -------
    #     None

    #     """
    #     if element_property.elset:
    #         elements = self.sets[element_property.elset].selection
    #     else:
    #         elements = element_property.elements

    #     for element in elements:
    #         self.elements[element].element_property = element_property.name

    # # ==============================================================================
    # # Nodes and Elements
    # # ==============================================================================

    # def add_nodes_elements_from_mesh(self, mesh, element_type, thermal=False, elset=None):
    #     """Adds the nodes and faces of a Mesh to the Structure object.

    #     Parameters
    #     ----------
    #     mesh : obj
    #         Mesh datastructure object.
    #     element_type : str
    #         Element type: 'ShellElement', 'MembraneElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     elset : str
    #         Name of element set to create.

    #     Returns
    #     -------
    #     list
    #         Keys of the created elements.
    #     """
    #     ekeys = super(Structure, self).add_nodes_elements_from_mesh(mesh, element_type, thermal)
    #     if elset:
    #         self.add_set(name=elset, type='element', selection=ekeys)
    #     return ekeys

    # def add_nodes_elements_from_network(self, network, element_type, thermal=False, axes={}, elset=None):
    #     """Adds the nodes and edges of a Network to the Structure object.

    #     Parameters
    #     ----------
    #     network : obj
    #         Network datastructure object.
    #     element_type : str
    #         Element type: 'BeamElement', 'TrussElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez' for all elements.
    #     elset : str
    #         Name of element set to create.

    #     Returns
    #     -------
    #     list
    #         Keys of the created elements.

    #     """
    #     ekeys = super(Structure, self).add_nodes_elements_from_network(network, element_type, thermal, axes)
    #     if elset:
    #         self.add_set(name=elset, type='element', selection=ekeys)
    #     return ekeys

    # def add_nodes_elements_from_volmesh(self, volmesh, element_type='SolidElement', thermal=False, axes={}, elset=None):
    #     """Adds the nodes and cells of a VolMesh to the Structure object.

    #     Parameters
    #     ----------
    #     volmesh : obj
    #         VolMesh datastructure object.
    #     element_type : str
    #         Element type: 'SolidElement' or ....
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez' for all elements.
    #     elset : str
    #         Name of element set to create.

    #     Returns
    #     -------
    #     list
    #         Keys of the created elements.

    #     """
    #     ekeys = super(Structure, self).add_nodes_elements_from_volmesh(volmesh, element_type, thermal, axes)
    #     if elset:
    #         self.add_set(name=elset, type='element', selection=ekeys)
    #     return ekeys

    # # ==============================================================================
    # # Sets
    # # ==============================================================================

    # def add_set(self, name, type, selection):
    #     """Adds a node, element or surface set to structure.sets.

    #     Parameters
    #     ----------
    #     name : str
    #         Name of the Set.
    #     type : str
    #         'node', 'element', 'surface_node', surface_element'.
    #     selection : list, dict
    #         The integer keys of the nodes, elements or the element numbers and sides.

    #     Returns
    #     -------
    #     None

    #     """
    #     if isinstance(selection, int):
    #         selection = [selection]
    #     self.sets[name] = Set(name=name, type=type, selection=selection, index=len(self.sets))
    def write_heading(self, job_name, f):

        line="""** {}
*Heading
** Job name: {}
** Generated by: compas_fea2
*Preprint, echo=NO, history=NO, contact=NO
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.67e-8
**
** PARTS
**\n""".format(self.name, job_name)
        f.write(line)

    def write_input_file(self, fields='u', output=True, save=False, path='C:/'):
        """Writes abaqus input file.

        Parameters
        ----------
        fields : list, str
            Data field requests.
        output : bool
            Print terminal output.
        save : bool
            Save structure to .cfea before file writing.

        Returns
        -------
        None

        """
        directory='{0}{1}'.format(self.path, self.name)
        filename = '{0}{1}/{2}.inp'.format(self.path, self.name, self.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if save:
            self.save_to_cfea()

        if isinstance(fields, str):
            fields = [fields]

        if 'u' not in fields:
            fields.append('u')




        # Open input file
        f=open(self.path,'w')

        # write heading
        self.write_heading(self.name, self.job_name, f)
        # Write parts
        for part in self.parts:
            part.write_keyword_start(f)
            part.write_data(f)
            part.write_keyword_end(f)

        # Write Assembly
        self.assembly.write_keyword_start(f)
        # Write instances
        for instance in self.assembly.instances:
            instance.write_data_line(f)
        # Write assembly node sets
        for nset in self.assembly.nsets:
            nset.write_data_line(f)
        # Write assembly element sets
        for elset in self.assembly.elsets:
            elset.write_data_line(f)
        # Write assembly surfaces
        for surface in self.assembly.surfaces:
            surface.write_data_line(f)
        for constraint in self.assembly.constraints:
            constraint.write_data_line(f)
        self.assembly.write_keyword_end(f)

        # Write materials
        Writer.write_keyword('materials')
        for material in self.materials:
            material.write_data_line(f)

        # Write interaction properties
        Writer.write_keyword('interaction properties')
        for interaction_property in self.interaction_properties:
            interaction_property.write_data_line(f)

        # Write interactions
        Writer.write_keyword('interactions')
        for interaction in self.interactions:
            interaction.write_data_line(f)

        # Write boundary conditions
        Writer.write_keyword('bc')
        for bc in self.bcs:
            bc.write_data_line(f)

        # Write steps
        for step in self.steps:
            step.write_header(f)
            # Write loads
            Writer.write_keyword_start('loads')
            for load in self.loads[step]:
                load.write_data_line(f)
            # Write Output Reequests
            Writer.write_headers('outputs')
            for output in self.outputs[step]:
                output.write_data_line(f)
            step.write_keyword_end(f)

        # Close input file
        f.close()

        if output:
            print('***** Abaqus input file generated: {0} *****\n'.format(filename))

    # this should be an abstract method of the base class
    def analyse(self, fields='u', exe=None, cpus=4, license='research', delete=True, output=True, overwrite=True, user_mat=False, save=False):
        """Runs the analysis through abaqus.

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
        self.write_input_file(fields=fields, output=output, save=save)

        cpus = 1 if license == 'student' else cpus
        launch_process(self, exe=exe, cpus=cpus, output=output, overwrite=overwrite, user_mat=user_mat)

    # this should be an abstract method of the base class
    def extract(self, fields='u', steps='all', exe=None, sets=None, license='research', output=True,
                     return_data=True, components=None):
        """Extracts data from the analysis output files.

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

    # this should be an abstract method of the base class
    def analyse_and_extract(self, fields='u', exe=None, cpus=4, license='research', output=True, save=False,
                            return_data=True, components=None, user_mat=False, overwrite=True):
        """Runs the analysis through the chosen FEA software / library and extracts data.

        Parameters
        ----------
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
        user_sub : bool
            Specify the user subroutine if needed.

        Returns
        -------
        None

        """

        self.analyse(exe=exe, fields=fields, cpus=cpus, license=license, output=output, user_mat=user_mat, overwrite=overwrite, save=save)

        self.extract(fields=fields, exe=exe, license=license, output=output,
                          return_data=return_data, components=components)


    # ==============================================================================
    # Results
    # ==============================================================================

    # this should be stored in a more generic way
    def get_nodal_results(self, step, field, nodes='all'):
        """Extract nodal results from self.results.

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
        """Extract element results from self.results.

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
