from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

import pickle
import os
import importlib

from compas_fea2.backends._base.base import FEABase
from compas_fea2.backends._base.model.parts import PartBase
from compas_fea2.backends._base.model.materials import MaterialBase
from compas_fea2.backends._base.model.sections import SectionBase
from compas_fea2.backends._base.model.bcs import GeneralBCBase
from compas_fea2.backends._base.model.groups import NodesGroupBase
from compas_fea2.backends._base.model.groups import ElementsGroupBase

__all__ = [
    'ModelBase',
]


class ModelBase(FEABase):
    """Initialise the Model object.

    Parameters
    ----------
    name : str
        Name of the Model.
    description : str
        Some description of the Model. This will be added to the input file and
        can be useful for future reference.
    """

    def __init__(self, name, description, author):
        self.__name__ = 'Model'
        self._name = name
        self._description = description
        self._author = author
        self._parts = {}
        self._nodes = []
        self._materials = {}
        self._sections = {}
        self._elements = {}
        self._constraints = {}
        self._releases = {}
        self._interactions = {}
        self._surfaces = {}
        self._bcs = {}
        self._problems = {}

    @property
    def name(self):
        """str : Name of the Model."""
        return self._name

    @property
    def description(self):
        """str : Some description of the Model. This will be added to the input file and
        can be useful for future reference."""
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def parts(self):
        """dict: A dictionary with the `Part` objects referenced in the Model."""
        return self._parts

    @property
    def nodes(self):
        """The nodes property."""
        return self._nodes

    @property
    def surfaces(self):
        """list : A list with the `Surface` objects belonging to the Model."""
        return self._surfaces

    @property
    def constraints(self):
        """list : A list with the `Constraint` objects belonging to the Model."""
        return self._constraints

    @property
    def releases(self):
        """list : A list with the `Release` objects belonging to the Model."""
        return self._releases

    @property
    def interactions(self):
        """list : A list with the `Interaction` objects belonging to the Model."""
        return self._interactions

    @property
    def materials(self):
        """dict : A dictionary of all the materials defined in the Model."""
        return self._materials

    @property
    def sections(self):
        """dict :  A dictionary of all the sections defined in the Model."""
        return self._sections

    @property
    def elements(self):
        """The elements property."""
        return self._elements

    @property
    def parts_groups(self):
        """dict : A dictionary of all the groups defined in the Model."""
        return self._parts_groups

    @property
    def bcs(self):
        """The bcs property."""
        return self._bcs

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    def _get_materials(self):
        materials = []
        for i in self.instances:
            for mat in i.part.elements_by_material.keys():
                materials.append(mat)
        return list(set(materials))

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    def from_network(self, network):
        raise NotImplementedError()

    def from_obj(self, obj):
        raise NotImplementedError()

    def frame_from_mesh(self, mesh, beam_section):
        """Creates a Model object from a compas Mesh object [WIP]. The edges of
        the mesh become the elements of the frame. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        mesh : obj
            Mesh to convert to import as a Model.
        beam_section : obj
            compas_fea2 BeamSection object to to apply to the frame elements.
        """
        from compas.geometry import normalize_vector
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))

        self.add_part(m.Part(name='part-1'))
        self.add_section(beam_section)

        for v in mesh.vertices():
            self.add_node(m.Node(mesh.vertex_coordinates(v)), 'part-1')

        # Generate elements between nodes
        key_index = mesh.key_index()
        vertices = list(mesh.vertices())
        edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]

        for e in edges:
            # get elements orientation
            v = normalize_vector(mesh.edge_vector(e[0], e[1]))
            v.append(v.pop(0))
            # add element to the model
            self.add_element(m.BeamElement(connectivity=[
                             e[0], e[1]], section=beam_section.name, orientation=v), part='part-1')

    def shell_from_mesh(self, mesh, shell_section):
        """Creates a Model object from a compas Mesh object [WIP]. The faces of
        the mesh become the elements of the shell. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        mesh : obj
            Mesh to convert to import as a Model.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))

        self.add_part(m.Part(name='part-1'))
        self.add_section(shell_section)

        for v in mesh.vertices():
            self.add_node(m.Node(mesh.vertex_coordinates(v)), 'part-1')

        # Generate elements between nodes
        key_index = mesh.key_index()
        faces = [[key_index[key]
                  for key in mesh.face_vertices(face)] for face in mesh.faces()]

        for f in faces:
            self.add_element(m.ShellElement(connectivity=f, section=shell_section.name), part='part-1')

    def shell_from_gmesh(self, gmshModel, shell_section):
        """Creates a Model object from a gmsh Model object [WIP]. The faces of
        the mesh become the elements of the shell. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        gmshModel : obj
            gmsh Model to convert.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.
        """

        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))

        self.add_part(m.Part(name='part-1'))
        self.add_section(shell_section)

        nodes = gmshModel.mesh.getNodes()
        node_tags = nodes[0]
        node_coords = nodes[1].reshape((-1, 3), order='C')
        for _, coords in zip(node_tags, node_coords):
            self.add_node(m.Node(coords.tolist()), 'part-1', check=False)
        elements = gmshModel.mesh.getElements()
        for eltype, etags, ntags in zip(*elements):
            if eltype == 2:
                for i, _ in enumerate(etags):
                    n = gmshModel.mesh.getElementProperties(eltype)[3]
                    triangle = ntags[i * n: i * n + n]  # NOTE: seems pretty much useless
                    triangle = [x-1 for x in triangle]
                    self.add_element(m.ShellElement(connectivity=triangle, section=shell_section.name), part='part-1')

    def from_volmesh(self, volmesh):
        raise NotImplementedError()

    def from_solid(self, solid):
        raise NotImplementedError()

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def _check_part_in_model(self, part, add=True):
        if not part in self._parts and not isinstance(part, PartBase):
            raise ValueError('** ERROR! **: part {} not found in the Model or instance of a Part!'.format(part))
        if isinstance(part, PartBase) and add:
            self.add_part(part)

    def add_part(self, part):
        """Adds a Part to the Model.

        Parameters
        ----------
        part : obj
            Part object from which the Instance is created.

        Returns
        -------
        None

        Examples
        --------
        >>> model = Assembly('mymodel')
        >>> part = Part('mypart')
        """
        if part.name in self.parts:
            print(f"WARNING: {part.__repr__()} already in the Model. skipped!")
        else:
            self.parts[part.name] = part

        # Add part's properties to the model
        self._nodes.append(part.nodes)  # TODO check

        for attr in ['elements', 'materials', 'sections']:
            for k, v in getattr(part, attr).items():
                if not k in getattr(self, attr):
                    getattr(self, attr)[k] = v
                else:
                    print('{} already in Model, skipped!'.format(v.__repr__()))

    def add_parts(self, parts):
        for part in parts:
            self.add_part(part)

    def remove_part(self, part):
        """ Removes the part from the Model and all the referenced instances
        of that part.

        Parameters
        ----------
        part : str
            Name of the Part to remove.

        Returns
        -------
        None
        """

        raise NotImplementedError()
        # # TODO remove nodes, elements and sections

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def _renumber_model_nodes():
        pass

    def _update_part_nodes_to_model(self, part, check=True):
        self._nodes.append(part._nodes)

    def _check_node_in_model(self, node, add=True):
        pass

    def add_node(self, node, part='hidden_part', check=True):
        """Add a compas_fea2 `Node` object to a `Part` in the `Model`.
        If the `Node` object has no label, one is automatically assigned.
        Duplicate nodes are automatically excluded.

        Warning
        -------
        For the backends that do not have the concept of a `Part`, a hidden_part
        is automatically created to keep things consistent. The user can ignore it.


        Parameters
        ----------
        node : obj
            compas_fea2 Node object.
        part : str, optional
            Name of the part where the node will be added.

        Returns
        -------
        None
        """
        if check:
            self._check_part_in_model(part)
        self._parts[part].add_node(node, check)
        self._update_part_nodes_to_model(self.parts[part])

    def add_nodes(self, nodes, part, check=True):
        """Add multiple compas_fea2 Node objects a Part in the Model.
        If the Node object has no label, one is automatically assigned. Duplicate
        nodes are automatically excluded.
        The part must have been previously added to the Model.

        Parameters
        ----------
        nodes : list
            List of compas_fea2 Node objects.
        part : str
            Name of the part where the node will be added.

        Returns
        -------
        None
        """
        if check:
            self._check_part_in_model(part)
        for node in nodes:
            self._parts[part].add_node(node, check)
        self._update_part_nodes_to_model(self.parts[part])

    def remove_node(self, node_key, part):
        '''Remove the node from a Part in the Model. If there are duplicate nodes,
        it removes also all the duplicates.

        Parameters
        ----------
        node_key : int
            Key number of the node to be removed.
        part : str
            Name of the part where the node will be removed from.

        Returns
        -------
        None
        '''

        if part in self.parts:
            self.parts[part].remove_node(node_key)
            self._update_part_nodes_to_model(part)  # TODO this happens at every iteration...
        else:
            raise ValueError(
                '** ERROR! **: part {} not found in the Model!'.format(part))

    def remove_nodes(self, nodes, part):
        '''Remove the nodes from a Part in the Model. If there are duplicate nodes,
        it removes also all the duplicates.

        Parameters
        ----------
        node : list
            List with the key numbers of the nodes to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        for node in nodes:
            self.remove_node(node, part)

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def _check_material_in_model(self, material, add=True):
        if not material in self._materials and not isinstance(material, MaterialBase):
            raise ValueError('** ERROR! **: section {} not found in the Model or instance of a Section!'.format(material))
        elif isinstance(material, MaterialBase) and add:
            self.add_material(material)

    def add_material(self, material):
        '''Adds a Material object to the Model so that it can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : obj
            compas_fea2 material object.

        Returns
        -------
        None
        '''
        if material._name not in self._materials:
            self._materials[material._name] = material
        else:
            print('WARNING: {} already added to the model. skipped!'.format(material))

    def add_materials(self, materials):
        '''Adds multiple Material objects to the Model so that they can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : list
            List of compas_fea2 material objects.

        Returns
        -------
        None
        '''
        for material in materials:
            self.add_material(material)

    def assign_material_to_element(self, material, part, element):
        raise NotImplementedError()

    # =========================================================================
    #                           Sections methods
    # =========================================================================

    def _check_section_in_model(self, section, add=True):
        if not section in self._sections and not isinstance(section, SectionBase):
            raise ValueError('** ERROR! **: section {} not found in the Model or instance of a Section!'.format(section))
        elif isinstance(section, SectionBase) and add:
            self.add_section(section)

    def add_section(self, section):
        """Adds a compas_fea2 Section object to the Model.

        Parameters
        ----------
        element : obj
            compas_fea2 Element object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        if isinstance(section.material, str):
            if section.material not in self.materials:
                raise ValueError(f'** ERROR! **: section {section.material} not found in the Model!')
            else:
                section._material = self.materials[section.material]

        if isinstance(section, SectionBase):
            if section._name not in self._sections:
                self._sections[section._name] = section
            else:
                print('WARNING: {} already added to the model. skipped!'.format(section))
        else:
            raise ValueError('Provide a valid Section object')

    def add_sections(self, sections):
        """Add multiple compas_fea2 Section objects to the Model.

        Parameters
        ----------
        sections : list
            list of compas_fea2 Section objects.

        Returns
        -------
        None
        """
        for section in sections:
            self.add_section(section)

    def assign_section_to_element(self, material, part, element):
        raise NotImplementedError()

    # =========================================================================
    #                           Elements methods
    # =========================================================================

    def _update_part_elements_to_model(self, part, check=True):
        self._elements[part._name] = part._elements

    def _check_element_in_model(self, element, add=True):
        self._check_material_in_model(element)

    def add_element(self, element, part, check=True):
        """Add a compas_fea2 `Element` object to a `Part` in the `Model`.

        Parameters
        ----------
        element : obj
            compas_fea2 `Element` object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """
        if check:
            self._check_part_in_model(part)
        # self._check_section_in_model(element.section)
        if isinstance(element.section, str):
            if element.section not in self.sections:
                if element.section in self.parts[part].sections:
                    self.sections[element.section] = self.parts[part].sections[element.section]
                else:
                    raise ValueError('ERROR: section {} not found in the Model!'.format(element.section.__repr__()))
            else:
                element._section = self.sections[element.section]
        self.parts[part].add_element(element)
        self._update_part_elements_to_model(self.parts[part])  # TODO this happens at every iteration...change!

    def add_elements(self, elements, part, check=True):
        """Adds multiple compas_fea2 Element objects to a Part in the Model.

        Parameters
        ----------
        elements : list
            List of compas_fea2 Element objects.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """

        for element in elements:
            self.add_element(element, part, check)

    def remove_element(self, element_key, part):
        '''Removes the element from a Part in the Model.

        Parameters
        ----------
        element_key : int
            Key number of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        if part in self.parts:
            self.parts[part].remove_element(element_key)
        else:
            raise ValueError('ERROR: part {} not found in the Model!'.format(part))

    def remove_elements(self, elements, part):
        '''Removes the elements from a Part in the Model.

        Parameters
        ----------
        elements : list
            List with the key numbers of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        for element in elements:
            self.remove_node(element, part)

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    def add_release(self, release, part):
        '''Add an Element End Release to the Model.

        Parameters
        ----------
        release : obj
            `EndRelase` object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''

        self._check_part_in_model(part)

        self.parts[part].add_release(release)
        self.releases.append(release)

    def add_releases(self, releases, part):
        '''Add multiple Element End Release to the Model.

        Parameters
        ----------
        release : list
            list of `EndRelase` object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        '''
        for release in releases:
            self.add_release(release, part)

    # =========================================================================
    #                           Groups methods
    # =========================================================================
    def add_group(self, group, part=None):
        '''Add a Group object to a part in the Model at the instance level. Can
        be either a NodesGroup or an ElementsGroup.

        Parameters
        ----------
        group : obj
            group object.

        Returns
        -------
        None
        '''
        if not part and isinstance(group, PartsGroupBase):
            self._check_part_in_model(part)
            self.parts[part].add_group(group)
        elif isinstance(group, PartsGroupBase):
            self._groups[group.name] = group
        else:
            TypeError

    def add_groups(self, groups, part=None):
        '''Add multiple Group objects to a part in the Model. Can be
        a list of NodesGroup or ElementsGroup objects, also mixed.

        Parameters
        ----------
        group : obj
            group object.
        part : str
            Name of the part the group belongs to.

        Returns
        -------
        None
        '''
        for group in groups:
            self.add_group(group, part)

    def add_nodes_group(self, name, part, nodes):
        self._check_part_in_model(part)
        self.parts[part].add_nodes_group(name, nodes)

    def add_elements_group(self, name, part, elements):
        self._check_part_in_model(part)
        self.parts[part].add_elements_group(name, elements)

    def add_parts_group(self, name, parts):
        raise NotImplementedError()
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        group = m.PartsGroup(name, parts)
        self._groups[group.name] = group

    def remove_group(self, group):
        raise NotImplementedError()

    # =========================================================================
    #                        Surfaces methods
    # =========================================================================

    def add_surface(self, surface):
        self.surfaces.append(surface)

    # =========================================================================
    #                       Constraints methods
    # =========================================================================

    def add_constraint(self, constraint):
        self._constraints[constraint.name] = constraint

    def add_constraints(self, constraints):
        for constraint in constraints:
            self.add_constraint(constraint)

    # =========================================================================
    #                        Interaction methods
    # =========================================================================

    def add_interactions(self, interactions):
        raise NotImplementedError()

    # =========================================================================
    #                           BCs methods
    # =========================================================================
    # TODO missing axes
    def add_bc(self, bc, nodes, part):
        """Adds a boundary condition to the Problem object.

        Parameters
        ----------
        bc : obj
            `compas_fea2` BoundaryCondtion object.
        part : str
            part in the model where the BoundaryCondtion is applied.

        Returns
        -------
        None
        """
        if not isinstance(bc, GeneralBCBase):
            raise TypeError(f'{bc} not instance of a BC class')
        if part not in self.bcs:
            self._bcs[part] = {node: bc for node in nodes}
        else:
            for node in nodes:
                if node in self.bcs[part]:
                    raise ValueError(f"overconstrained node: {self.parts[part].nodes[node]}")
                else:
                    self._bcs[part][node] = bc

    def add_bc_type(self, name, bc_type, part, nodes, axes='global'):
        types = {'fix': 'FixedBC', 'fixXX': 'FixedBCXX', 'fixYY': 'FixedBCYY',
                 'fixZZ': 'FixedBCZZ', 'pin': 'PinnedBC', 'rollerX': 'RollerBCX',
                 'rollerY': 'RollerBCY', 'rollerZ': 'RollerBCZ', 'rollerXY': 'RollerBCXY',
                 'rollerYZ': 'RollerBCYZ', 'rollerXZ': 'RollerBCXZ',
                 }
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        bc = getattr(m, types[bc_type])(name, axes)
        self._bcs.setdefault(part, {})[bc] = nodes

    def add_fix_bc(self, name, part, nodes, axes='global'):
        self.add_bc_type(name, 'fix', part, nodes)

    def add_fixXX_bc(self, name, part, nodes, axes='global'):
        self.add_bc_type(name, 'fixXX', part, nodes)

    def add_fixYY_bc(self, name, part, nodes, axes='global'):
        self.add_bc_type(name, 'fixYY', part, nodes)

    def add_fixZZ_bc(self, name, part, nodes, axes='global'):
        self.add_bc_type(name, 'fixZZ', part, nodes)

    def add_pin_bc(self, name, part, nodes):
        self.add_bc_type(name, 'pin', part, nodes)

    def add_rollerX_bc(self, name, part, nodes):
        self.add_bc_type(name, 'rollerX', part, nodes)

    def add_rollerY_bc(self, name, part, nodes):
        self.add_bc_type(name, 'rollerY', part, nodes)

    def add_rollerZ_bc(self, name, part, nodes):
        self.add_bc_type(name, 'rollerZ', part, nodes)

    def add_rollerXY_bc(self, name, part, nodes):
        self.add_bc_type(name, 'rollerXY', part, nodes)

    def add_rollerXZ_bc(self, name, part, nodes):
        self.add_bc_type(name, 'rollerXZ', part, nodes)

    def add_rollerYZ_bc(self, name, part, nodes):
        self.add_bc_type(name, 'rollerYZ', part, nodes)

    def add_bcs(self, bcs):
        """Adds multiple boundary conditions to the Problem object.

        Parameters
        ----------
        bcs : list
            List of `compas_fea2` BoundaryCondtion objects.

        Returns
        -------
        None
        """
        for bc in bcs:
            self.add_bc(bc)

    def remove_bc(self, bc_name):
        """Removes a boundary condition from the Problem object.

        Parameters
        ----------
        bc_name : str
            Name of thedisplacement to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_bcs(self, bc_names):
        """Removes multiple boundary conditions from the Problem object.

        Parameters
        ----------
        bc_names : list
            List of names of the boundary conditions to remove.

        Returns
        -------
        None
        """
        raise NotImplementedError

    def remove_all_bcs(self):
        """Removes all the boundary conditions from the Problem object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.bcs = {}

    # =========================================================================
    #                          Helper methods
    # =========================================================================

    def _check_part_in_model(self, part_name):
        if part_name not in self.parts:
            raise ValueError(f'ERROR: part {part_name} not found in the Model!')

    # TODO change to check through the instance

    def get_node_from_coordinates(self, xyz, tol):
        """Finds (if any) the Node object in the model with the specified coordinates.
        A tollerance factor can be specified.

        Parameters
        ----------
        xyz : list
            List with the [x, y, z] coordinates of the Node.
        tol : int
            multiple to which round the coordinates.

        Returns
        -------
        node : dict
            Dictionary with the Node object for each Instance.
            key =  Instance
            value = Node object with the specified coordinates.
        """

        node_dict = {}
        for part in self.parts.values():
            for node in part.nodes:
                a = [tol * round(i/tol) for i in node.xyz]
                b = [tol * round(i/tol) for i in xyz]
                # if math.isclose(node.xyz, xyz, tol):
                if a == b:
                    node_dict[part.name] = node.key
        if not node_dict:
            print("WARNING: Node at {} not found!".format(b))

        return node_dict

    # ==============================================================================
    # Summary
    # ==============================================================================
    # TODO continue the summary # FIXME
    def summary(self):
        """Prints a summary of the Model object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        data = """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Model: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Parts
-----
{}
    # of nodes:     {}
    # of elements:  {}

Materials
---------
{}

Sections
--------
{}

Interactions
------------
{}

Constraints
-----------
{}

Boundary Conditions
-------------------
{}

""".format(self.name,
           '\n'.join([e for e in self.parts]),
           '\n'.join([str(len(e)) for e in [p.nodes for p in self.parts.values()]]),
           '\n'.join([str(len(e)) for e in [p.elements for p in self.parts.values()]]),
           '\n'.join([e for e in self.materials]),
           '\n'.join([e for e in self.sections]),
           '\n'.join([e for e in self.interactions]),
           '\n'.join([e for e in self.constraints]),
           '\n'.join([f'{part}: {node}' for part, node in self.bcs.items()]),
           )
        print(data)
        return data

    # ==============================================================================
    # Viewer
    # ==============================================================================

    def show(self, width=800, height=500, scale_factor=.001):
        from compas_fea2.interfaces.viewer import ModelViewer

        v = ModelViewer(self, width, height, scale_factor)
        v.show()

    # ==============================================================================
    # Save model file
    # ==============================================================================

    def save_to_cfm(self, path, output=True):
        """Exports the Model object to an .cfm file through Pickle.

        Parameters
        ----------
        path : path
            Path to the folder where save the file to.
        output : bool
            Print terminal output.

        Returns
        -------
        None
        """

        if not os.path.exists(path):
            os.makedirs(path)

        filename = '{0}/{1}.cfm'.format(path, self.name)

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        if output:
            print('***** Model saved to: {0} *****\n'.format(filename))

    # ==============================================================================
    # Load model file
    # ==============================================================================

    @ staticmethod
    def load_from_cfm(filename, output=True):
        """Imports a Model object from an .cfm file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Model .cfm from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Model object.
        """
        with open(filename, 'rb') as f:
            mdl = pickle.load(f)

        if output:
            print('***** Model loaded from: {0} *****'.format(filename))

        return mdl
