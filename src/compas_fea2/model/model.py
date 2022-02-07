from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle
import os
import importlib

from compas_fea2.base import FEABase
from compas_fea2.model.parts import PartBase
from compas_fea2.model.materials import MaterialBase
from compas_fea2.model.sections import SectionBase
from compas_fea2.model.bcs import GeneralBCBase
# from compas_fea2.model.groups import NodesGroupBase
# from compas_fea2.model.groups import ElementsGroupBase


class ModelBase(FEABase):
    """Initialise the Model object.

    Note
    ----
    For the backends that do not have the concept of a `Part`, a model with only
    one part should be created.

    Parameters
    ----------
    name : str
        Name of the Model.
    description : str
        Some description of the Model. This will be added to the input file and
        can be useful for future reference.
    author : str
        The name of the author of the Model. This will be added to the input file and
        can be useful for future reference.
    """

    def __init__(self, name, description, author):
        self.__name__ = 'Model'
        self._name = name
        self._description = description
        self._author = author
        self._parts = {}
        self._materials = {}
        self._sections = {}
        self._bcs = {}
        self._constraints = {}
        self._interactions = {}
        self._contacts = {}
        self._parts_groups = {}
        self._surfaces = {}

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
    def author(self):
        """str : The author of the Model. This will be added to the input file and
        can be useful for future reference."""
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def parts(self):
        """dict: A dictionary with the `Part` objects referenced in the Model."""
        return self._parts

    @property
    def materials(self):
        """dict : A dictionary of all the materials defined in the Model."""
        return self._materials

    @property
    def sections(self):
        """dict :  A dictionary with all the sections defined in the Model."""
        return self._sections

    @property
    def parts_groups(self):
        """dict : A dictionary of the groups of parts."""
        return self._parts_groups

    @property
    def bcs(self):
        """dict : A dictionary with the boundary conditions assigned to the parts in the Model."""
        return self._bcs

    @property
    def contacts(self):
        """dict : A dictionary with the boundary conditions assigned to the parts in the Model."""
        return self._contacts

    @property
    def constraints(self):
        """dict : A dictionary with the `Constraint` objects between the parts of the model."""
        return self._constraints

    @property
    def interactions(self):
        """dict : A dictionary with the `Interaction` properties  defined in the model."""
        return self._interactions

    @property
    def surfaces(self):
        """dict : A dictionary with the surface definitions in the Model."""
        return self._surfaces

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    def from_network(self, network):
        raise NotImplementedError()

    def from_obj(self, obj):
        raise NotImplementedError()

    @classmethod
    def frame_from_mesh(cls, name, part_name, mesh, beam_section, author=None, description=None):
        """Creates a Model object from a compas Mesh object [WIP]. The edges of
        the mesh become the BeamElements of the frame. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        name : str
            name of the new Model.
        part_name : str
            name of the new part.
        mesh : obj
            Mesh to convert to import as a Model.
        beam_section : obj
            compas_fea2 BeamSection object to to apply to the frame elements.
        """
        m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
        model = cls(name)
        part = m.Part.frame_from_mesh(part_name, mesh, beam_section)
        model.add_part(part)
        return model

    @classmethod
    def shell_from_mesh(cls, name, part_name, mesh, shell_section):
        """Create a Model object from a compas Mesh object [WIP]. The faces of
        the mesh become ShellElement objects. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        name : str
            name of the new Model.
        part_name : str
            name of the new part.
        mesh : obj
            Mesh to convert to import as a Model.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.
        """
        m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
        model = cls(name)
        part = m.Part.shell_from_mesh(part_name, mesh, shell_section)
        model.add_part(part)
        return model

    @classmethod
    def shell_from_gmesh(cls, name, part_name, gmshModel, shell_section):
        """Creates a Model object from a gmsh Model object [WIP]. The faces of
        the mesh become the elements of the shell. Currently, the same section
        is applied to all the elements.

        Parameters
        ----------
        name : str
            name of the new Model.
        part_name : str
            name of the new Part.
        gmshModel : obj
            gmsh Model to convert.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.
        """
        m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
        model = cls(name)
        part = m.Part.shell_from_gmesh(part_name, gmshModel, shell_section)
        model.add_part(part)
        return model

    @classmethod
    def from_volmesh(cls, name, part_name, volmesh):
        raise NotImplementedError()

    @classmethod
    def from_solid(cls, name, part_name, solid):
        raise NotImplementedError()

    @classmethod
    def from_compas_part(cls, name, part_name, part):
        raise NotImplementedError()

    @classmethod
    def from_compas_assembly(cls, name, part_name, assembly):
        raise NotImplementedError()

    # =========================================================================
    #                             Parts methods
    # =========================================================================
    def _check_part_in_model(self, part):
        """Check if the part is already in the model and in case add it.
        If `part` is of type :class:`str`, check if the part is already defined.
        If `part` is of type :class:`PartBase`, add the part to the Model if not
        already defined.

        Parameters
        ----------
        part : str or obj
            Name of the Part or Part object to check.

        Returns
        -------
        obj
            type :class:`PartBase` object

        Raises
        ------
        ValueError
            if `part` is a string and the part is not defined in the model
        TypeError
            `part` must be either an instance of a `compas_fea2` :class:`PartBase`
            or the name of a :class:`PartBase` already defined in the Model.
        """
        if isinstance(part, str):
            if part not in self.parts:
                raise ValueError(f'{part} not found in the Model')
            part_name = part
        elif isinstance(part, PartBase):
            if part.name not in self.parts:
                self.add_part(part)
                print(f'{part.__repr__()} added to the Model')
            part_name = part.name
        else:
            raise TypeError(
                f'{part} is either not an instance of a compas_fea2 Part class or not found in the Model')

        return self.parts[part_name]

    def add_part(self, part):
        """Adds a Part to the Model.

        Parameters
        ----------
        part : obj
            type :class:`PartBase` object.

        Returns
        -------
        None
        """
        if part.name in self.parts:
            print(f"WARNING: {part.__repr__()} already in the Model. skipped!")
        else:
            self.parts[part.name] = part

        for attr in ['materials', 'sections']:
            for k, v in getattr(part, attr).items():
                if k not in getattr(self, attr):
                    getattr(self, attr)[k] = v
                else:
                    print(f'{v.__repr__()} already in Model, skipped!')

    def add_parts(self, parts):
        """Add multiple Part objects to the Model.

        Parameters
        ----------
        parts : list
            List of the :class:`PartBase` objects to add.
        """
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

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def add_node(self, node, part, check=False):
        """Add a :class:`NodeBase` object to a part in the Model.
        If the node object has no label, one is automatically assigned.

        Parameters
        ----------
        node : obj
            :class:`NodeBase` object.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.
        check : bool, optional
            If ``True``, checks if the node is already present. This is a quite
            resource-intense operation! Set to ``False`` for large parts (>10000
            nodes). By default ``False``

        Return
        ------
        int
            node key

        Examples
        --------
        >>> model = Model('mymodel')
        >>> model.add_part(Part('mypart'))
        >>> node = Node(1.0, 2.0, 3.0)
        >>> model.add_node(node, 'mypart', check=True)
        0
        """
        part = self._check_part_in_model(part)
        return part.add_node(node, check)

    def add_nodes(self, nodes, part, check=False):
        """Add multiple :class:`NodeBase` objects a part in the Model.
        If the Node object has no label, one is automatically assigned.
        Duplicate nodes are automatically excluded.

        Parameters
        ----------
        nodes : list
            List of :class:`NodeBase` objects.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.
        check : bool, optional
            If ``True``, checks if the node is already present. This is a quite
            resource-intense operation! Set to ``False`` for large parts (>10000
            nodes). By default ``False``

        Return
        ------
        list of int
            list with the keys of the added nodes.

        Examples
        --------
        >>> model = Model('mymodel')
        >>> model.add_part(Part('mypart'))
        >>> node1 = Node([1.0, 2.0, 3.0])
        >>> node2 = Node([3.0, 4.0, 5.0])
        >>> node3 = Node([3.0, 4.0, 5.0]) # Duplicate node
        >>> model.add_nodes([node1, node2, node3], 'mypart', check=True)
        [0, 1, None]
        """
        return [self.add_node(node, part, check) for node in nodes]

    def remove_node(self, node_key, part):
        """Remove the node from a Part in the Model.

        Parameters
        ----------
        node_key : int
            Key number of the node to be removed.
        part : str
            Name of the part where the node will be removed from.

        Returns
        -------
        None
        """
        raise NotImplementedError()

    def remove_nodes(self, nodes, part):
        """Remove the `nodes` from a part in the Model. If there are duplicate
        nodes, remove also all the duplicates.

        Parameters
        ----------
        nodes : list
            List with the key (:class:`int`) of the nodes to be removed.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            removed.

        Returns
        -------
        None
        """
        raise NotImplementedError()

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
        dict
            Dictionary with the keys of the maching nodes for each Part.
            key =  Part name
            value = list of keys of the maching the specified coordinates.
        """
        return {part.name: part.get_node_from_coordinates(xyz, tol) for part in self.parts.values()}

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material):
        """Add a :class:`MaterialBase` subclass object to the Model so that it can be
        later refernced and used in the section and element definitions.

        Parameters
        ----------
        material : obj
            :class:`MaterialBase` object to be added.

        Returns
        -------
        None
        """
        if material.name not in self.materials:
            self._materials[material._name] = material
        else:
            print('NOTE: {} already added to the model. skipped!'.format(material))

    def add_materials(self, materials):
        """Add multiple :class:`MaterialBase` subclass objects to the Model so
        that they can be later refernced and used in section and element definitions.

        Parameters
        ----------
        material : list
            List of :class:`MaterialBase` objects.

        Returns
        -------
        None
        """
        for material in materials:
            self.add_material(material)

    # =========================================================================
    #                           Sections methods
    # =========================================================================

    def add_section(self, section):
        """Add a :class:`SectionBase` subclass object to the Model o that it can be later
        refernced and used in an element definition.

        Parameters
        ----------
        section : obj
            :class:`SectionBase` subclass object to be added.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            if the material associated to the section is a string and it has not
            been defined previously in the model
        """

        if isinstance(section.material, str):
            if section.material not in self.materials:
                raise ValueError(f'** ERROR! **: section {section.material.__repr__()} not found in the Model!')
            else:
                section._material = self.materials[section.material]
        elif isinstance(section.material, MaterialBase):
            if section.material.name not in self.materials:
                self._materials[section.material.name] = section.material
        else:
            raise TypeError(
                "The material for the the section must be either the name of a previously added Material or an instance of a Material object")

        if isinstance(section, SectionBase):
            if section._name not in self._sections:
                self._sections[section._name] = section
            else:
                print('WARNING: {} already added to the model. skipped!'.format(section))
        else:
            raise TypeError('Provide a valid SectionBase subclass object')

    def add_sections(self, sections):
        """Add multiple :class:`SectionBase`subclass  objects to the Model.

        Parameters
        ----------
        sections : list
            list of :class:`SectionBase` subclass objects.

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

    def add_element(self, element, part, check=False):
        """Add a :class:`ElementBase` subclass object to a part in the Model.

        Note
        ----
        Elements are defined at the part level. The element added is stored in
        the specified part. However, the section and material associaceted are
        added to tthe model, if not already present.

        Parameters
        ----------
        element : obj
            :class:`ElementBase` subclass object to be added.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.
        check : bool, optional
            If ``True``, checks if the node connected by the element are present.
            This is a quite resource-intense operation! Set to ``False`` for large
            parts (>10000 nodes). By default ``False``

        Returns
        -------
        int
            element key
        """
        part = self._check_part_in_model(part)
        if isinstance(element.section, str):
            if element.section not in self.sections:
                if element.section in part.sections:
                    self.sections[element.section] = part.sections[element.section]
                else:
                    raise ValueError(f'ERROR: section {element.section.__repr__()} not found in the Model!')
            else:
                element._section = self.sections[element.section]
        return part.add_element(element, check)

    def add_elements(self, elements, part, check=False):
        """Adds multiple :class:`ElementBase` subclass objects to a part in the Model.

        Parameters
        ----------
        elements : list
            List of compas_fea2 Element subclass objects.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.
        check : bool
            If True, checks if the element keys are in the model. This is a quite
            resource-intense operation! Set to `False` for large models (>10000
            nodes)

        Return
        ------
        list of int
            list with the keys of the added nodes.
        """
        return [self.add_element(element, part, check) for element in elements]

    def remove_element(self, element_key, part):
        """Removes the element from a Part in the Model.

        Parameters
        ----------
        element_key : int
            Key number of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """
        raise NotImplementedError()
        part = self._check_part_in_model(part)
        part.remove_element(element_key)

    def remove_elements(self, elements, part):
        """Removes several elements from a Part in the Model.

        Parameters
        ----------
        elements : list
            List with the key numbers of the element to be removed.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """
        raise NotImplementedError()
        for element in elements:
            self.remove_node(element, part)

    # =========================================================================
    #                           Releases methods
    # =========================================================================
    # TODO: check the release definition

    def add_release(self, release, part):
        """Add an Element EndRelease object to the Model.

        Parameters
        ----------
        release : obj
            `EndRelase` object.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.

        Returns
        -------
        None
        """
        part = self._check_part_in_model(part)
        part.add_release(release)

    def add_releases(self, releases, part):
        """Add multiple Element EndRelease objects to the Model.

        Parameters
        ----------
        releases : list
            list of `EndRelase` object.
        part : str
            Name of the part where the nodes will be removed from.

        Returns
        -------
        None
        """
        for release in releases:
            self.add_release(release, part)

    # =========================================================================
    #                           Groups methods
    # =========================================================================
    def group_parts(self, name, parts):
        """Group parts together.

        Parameters
        ----------
        name : str
            name of the group
        parts : list of str
            list containing the parts names to group

        Returns
        -------
        None
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        group = m.PartsGroup(name=name, parts=parts)
        self._parts_groups[group.name] = group

    # NOTE: Nodes and Elements groups should not be added but defined (simlartly to what happens for Parts)
    def add_group(self, group, part):
        """Add a Group object to a part in the Model. it can be either a
        :class:`NodesGroupBase` or an :class:`ElementsGroupBase`.

        Parameters
        ----------
        group : obj
            :class:`NodesGroupBase` or :class:`ElementsGroupBase` object to add.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.

        Returns
        -------
        None
        """
        part = self._check_part_in_model(part)
        part.add_group(group)

    def add_groups(self, groups, part):
        """Add multiple Group objects to a part in the Model. Can be
        a list of NodesGroup or ElementsGroup objects, also mixed.

        Parameters
        ----------
        group : obj
            group object.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.

        Returns
        -------
        None
        """
        for group in groups:
            self.add_group(group, part)

    def add_nodes_group(self, name, part, nodes):
        """Add a :class:`NodeGroupBase` object to the the part in the model.

        Parameters
        ----------
        name : str
            name of the group.
        part : str
            name of the part
        nodes : list
            list of nodes keys to group

        Returns
        -------
        None
        """
        part = self._check_part_in_model(part)
        part.add_nodes_group(name, nodes)

    def add_elements_group(self, name, part, elements):
        """Add a :class:`ElementGroupBase` object to a part in the model.

        Parameters
        ----------
        name : str
            name of the group.
        part : str
            name of the part
        elements : list
            list of elements keys to group

        Returns
        -------
        None
        """
        part = self._check_part_in_model(part)
        part.add_elements_group(name, elements)

    def remove_group(self, group):
        raise NotImplementedError()

    # =========================================================================
    #                        Surfaces methods
    # =========================================================================

    def add_surface(self, surface):
        """Add a :class:`SurfaceBase` object to the model.

        Parameters
        ----------
        surface : obj
            type :class:`SurfaceBase` object to be added

        Returns
        -------
        None
        """
        self._surfaces[surface.name] = surface

    def add_surfaces(self, surfaces):
        """Add multiple :class:`SurfaceBase` objects to the Model.

        Parameters
        ----------
        surfaces : list
            list with the type :class:`SurfaceBase` objects to be added

        Returns
        -------
        None
        """
        for surface in surfaces:
            self.add_surface(surface)

    # =========================================================================
    #                       Constraints methods
    # =========================================================================

    def add_constraint(self, constraint):
        """Add a :class:`ConstraintBase` object to the Model.

        Parameters
        ----------
        constraint : obj
            :class:`ConstraintBase` object to add.

        Returns
        -------
        None
        """
        self._constraints[constraint.name] = constraint

    def add_constraints(self, constraints):
        """Add multiple :class:`ConstraintBase` objects to the Model.

        Parameters
        ----------
        constraints : list
            list of :class:`ConstraintBase` objects to add.

        Returns
        -------
        None
        """
        for constraint in constraints:
            self.add_constraint(constraint)

    # =========================================================================
    #                        ContactPair methods
    # =========================================================================
    def add_contact(self, contact):
        """Add a :class:`ContactPairBase` object to the model.

        Parameters
        ----------
        surface : obj
            type :class:`ContactPairBase` object to be added

        Returns
        -------
        None
        """
        self._contacts[contact.name] = contact

        if isinstance(contact.master, str):
            if contact.master in self._surfaces:
                contact._master = self._surfaces[contact.master]
            else:
                raise ValueError(f'{contact.master} not found in {self.__repr__()}')
        if contact.master.name not in self._surfaces:
            self._surfaces[contact.master.name] = contact.master

        if isinstance(contact.slave, str):
            if contact.slave in self._surfaces:
                contact._slave = self._surfaces[contact.slave]
            else:
                raise ValueError(f'{contact.slave} not found in {self.__repr__()}')
        if contact.slave.name not in self._surfaces:
            self._surfaces[contact.slave.name] = contact.slave

        if isinstance(contact.interaction, str):
            if contact.interaction in self._interaction:
                contact._interactions = self._interactions[contact.interaction]
            else:
                raise ValueError(f'{contact.interaction} not found in {self.__repr__()}')
        if contact.interaction.name not in self._interactions:
            self._interactions[contact.interaction.name] = contact.interaction

    def add_contacts(self, contacts):
        """Add multiple :class:`ContactPairBase` objects to the Model.

        Parameters
        ----------
        surfaces : list
            list with the type :class:`ContactPairBase` objects to be added

        Returns
        -------
        None
        """
        for contact in contacts:
            self.add_contact(contact)

    # =========================================================================
    #                        Interaction methods
    # =========================================================================
    # FIXME choose between Contact and Interaction for the name
    def add_interaction(self, interaction):
        """Add a :class:`ContactBase` object to the model.

        Parameters
        ----------
        surface : obj
            type :class:`ContactBase` object to be added

        Returns
        -------
        None
        """
        self._interactions[interaction.name] = interaction

    def add_interactions(self, interactions):
        """Add multiple :class:`ContactBase` objects to the Model.

        Parameters
        ----------
        surfaces : list
            list with the type :class:`ContactBase` objects to be added

        Returns
        -------
        None
        """
        for interaction in interactions:
            self.add_interaction(interaction)

    # =========================================================================
    #                           BCs methods
    # =========================================================================
    # FIXME missing axes
    def add_bc(self, bc, nodes, part):
        """Adds a :class:`GeneralBCBase` to the Problem object.

        Parameters
        ----------
        bc : obj
            :class:`GeneralBCBase` object.
        nodes : list
            list with the node keys where to assign the boundary condition.
        part : str, obj
            Name of the part or :class:`PartBase` object where the node will be
            added.

        Returns
        -------
        None
        """
        part = self._check_part_in_model(part)
        if not isinstance(nodes, (list, tuple)):
            nodes = [nodes]
        if not isinstance(bc, GeneralBCBase):
            raise TypeError(f'{bc} not instance of a BC class')
        if part not in self.bcs:
            self._bcs[part] = {node: bc for node in nodes}
        else:
            for node in nodes:
                if node in self.bcs[part]:
                    raise ValueError(f"overconstrained node: {self.parts[part].nodes[node].__repr__()}")
                else:
                    self._bcs[part][node] = bc

    def add_bc_type(self, name, bc_type, part, nodes, axes='global'):
        """Add a :class:`GeneralBCBase` subclass to nodes in a part by type.

        Note
        ----
        The bc_type must be one of the following:
        +------------------------+-------------------------+
        | bc_type                | BC                      |
        +========================+=========================+
        | fix                    | :class:`FixedBCBase`    |
        +------------------------+-------------------------+
        | body row 2             | ...                     |
        +------------------------+-------------------------+
        'fix': 'FixedBC', 'fixXX': 'FixedBCXX', 'fixYY': 'FixedBCYY',
        'fixZZ': 'FixedBCZZ', 'pin': 'PinnedBC', 'rollerX': 'RollerBCX',
        'rollerY': 'RollerBCY', 'rollerZ': 'RollerBCZ', 'rollerXY': 'RollerBCXY',
        'rollerYZ': 'RollerBCYZ', 'rollerXZ': 'RollerBCXZ',

        Parameters
        ----------
        name : str
            name of the boundary condition
        bc_type : str
            one of the boundary condition types specified above
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        types = {'fix': 'FixedBC', 'fixXX': 'FixedBCXX', 'fixYY': 'FixedBCYY',
                 'fixZZ': 'FixedBCZZ', 'pin': 'PinnedBC', 'rollerX': 'RollerBCX',
                 'rollerY': 'RollerBCY', 'rollerZ': 'RollerBCZ', 'rollerXY': 'RollerBCXY',
                 'rollerYZ': 'RollerBCYZ', 'rollerXZ': 'RollerBCXZ',
                 }
        self._check_part_in_model(part)
        # self._check_nodes_in_model(nodes) #TODO implement method
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        bc = getattr(m, types[bc_type])(name, axes)
        self._bcs.setdefault(part, {})[bc] = nodes

    def add_fix_bc(self, name, part, nodes, axes='global'):
        """Add a :class:`FixedBCBase` to the nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes keys where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fix', part, nodes)

    def add_fixXX_bc(self, name, part, nodes, axes='global'):
        """Add a fixed boundary condition type free about XX to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fixXX', part, nodes)

    def add_fixYY_bc(self, name, part, nodes, axes='global'):
        """Add a fixed boundary condition free about YY type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fixYY', part, nodes)

    def add_fixZZ_bc(self, name, part, nodes, axes='global'):
        """Add a fixed boundary condition free about ZZ type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fixZZ', part, nodes)

    def add_pin_bc(self, name, part, nodes):
        """Add a pinned boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'pin', part, nodes)

    def add_rollerX_bc(self, name, part, nodes):
        """Add a roller free on X boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerX', part, nodes)

    def add_rollerY_bc(self, name, part, nodes):
        """Add a roller free on Y boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerY', part, nodes)

    def add_rollerZ_bc(self, name, part, nodes):
        """Add a roller free on Z boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerZ', part, nodes)

    def add_rollerXY_bc(self, name, part, nodes):
        """Add a roller free on XY boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerXY', part, nodes)

    def add_rollerXZ_bc(self, name, part, nodes):
        """Add a roller free on XZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerXZ', part, nodes)

    def add_rollerYZ_bc(self, name, part, nodes):
        """Add a roller free on YZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        nodes : list
            list of nodes where to apply the boundary condition
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
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
        """Removes a boundary condition from the Model.

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
        """Removes multiple boundary conditions from the Model.

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
        """Removes all the boundary conditions from the Model.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        raise NotImplementedError()

    # ==============================================================================
    # Summary
    # ==============================================================================
    def summary(self):
        """Prints a summary of the Model object.

        Parameters
        ----------
        None

        Returns
        -------
        str
            Model summary
        """
        parts_info = ['\n'.join([f'{part.name}',
                                 f'    # of nodes: {len(part.nodes)}',
                                 f'    # of elements: {len(part.elements)}']) for part in self.parts.values()]
        materials_info = '\n'.join([e.__repr__() for e in self.materials.values()])
        sections_info = '\n'.join([e.__repr__() for e in self.sections.values()])
        interactions_info = '\n'.join([e.__repr__() for e in self.interactions.values()])
        constraints_info = '\n'.join([e.__repr__() for e in self.constraints.values()])
        bc_info = '\n'.join([f'{part}: {node}' for part, node in self.bcs.items()])
        data = f"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Model: {self.name}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

description: {self.description or 'N/A'}
author: {self.author or 'N/A'}

Parts
-----
{''.join(parts_info)}

Materials
---------
{materials_info}

Sections
--------
{sections_info}

Interactions
------------
{interactions_info}

Constraints
-----------
{constraints_info}

Boundary Conditions
-------------------
{bc_info}
"""
        print(data)
        return data

    # ==============================================================================
    # Viewer
    # ==============================================================================

    def show(self, width=800, height=500, scale_factor=1, node_labels=None):
        from compas_fea2.interfaces.viewer import ModelViewer
        v = ModelViewer(self, width, height, scale_factor, node_labels)
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
