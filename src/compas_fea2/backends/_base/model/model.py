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
            name of the new part.
        gmshModel : obj
            gmsh Model to convert.
        shell_section : obj
            compas_fea2 ShellSection object to to apply to the shell elements.
        """
        m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
        model = cls(name)
        part = m.Part.shell_from_gmesh(part_name, mesh, shell_section)
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

    # =========================================================================
    #                             Parts methods
    # =========================================================================
    def _check_part_in_model(self, part):
        """Check if the part is already in the model and in case add it.
        If `part` is of type `str`, check if the part is already defined.
        If `part` is of type `PartBase`, add the part to the Model if not
        already defined.

        Parameters
        ----------
        part : str or obj
            Name of the Part or Part object to check.

        Returns
        -------
        obj
            Part object

        Raises
        ------
        ValueError
            if `part` is a string and the part is not defined in the model
        TypeError
            `part` must be either an instance of a `compas_fea2` Part class or the
            name of a Part already defined in the Model.
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
                f'{part} is either not an instance of a `compas_fea2` Part class or not found in the Model')

        return self.parts[part_name]

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

        for attr in ['materials', 'sections']:
            for k, v in getattr(part, attr).items():
                if not k in getattr(self, attr):
                    getattr(self, attr)[k] = v
                else:
                    print('{} already in Model, skipped!'.format(v.__repr__()))

    def add_parts(self, parts):
        """Add multiple parts to the Model.

        Parameters
        ----------
        parts : list
            List of the Part objects to add.
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

    def add_node(self, node, part):
        """Add a compas_fea2 `Node` object to a `Part` in the `Model`.
        If the `Node` object has no label, one is automatically assigned.
        Duplicate nodes are automatically excluded.

        Parameters
        ----------
        node : obj
            compas_fea2 Node object.
        part : str, obj
            Name of the part or Part object where the node will be added.

        Returns
        -------
        None
        """
        part = self._check_part_in_model(part)
        part.add_node(node)

    def add_nodes(self, nodes, part):
        """Add multiple compas_fea2 Node objects a Part in the Model.
        If the Node object has no label, one is automatically assigned. Duplicate
        nodes are automatically excluded.

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
        for node in nodes:
            self.add_node(node, part)

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
        """Remove the nodes from a Part in the Model. If there are duplicate nodes,
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
        """
        raise NotImplementedError()

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material):
        """Add a Material object to the Model so that it can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : obj
            compas_fea2 material object.

        Returns
        -------
        None
        """
        if material.name not in self.materials:
            self._materials[material._name] = material
        else:
            print('WARNING: {} already added to the model. skipped!'.format(material))

    def add_materials(self, materials):
        """Add multiple Material objects to the Model so that they can be later refernced
        and used in the Section and Element definitions.

        Parameters
        ----------
        material : list
            List of compas_fea2 material objects.

        Returns
        -------
        None
        """
        for material in materials:
            self.add_material(material)

    def assign_material_to_element(self, material, part, element):
        raise NotImplementedError()

    # =========================================================================
    #                           Sections methods
    # =========================================================================

    def add_section(self, section):
        """Add a compas_fea2 Section object to the Model o that it can be later
        refernced and used in an Element definitions

        Parameters
        ----------
        section : obj
            compas_fea2 Section object.

        Returns
        -------
        None
        """

        if isinstance(section.material, str):
            if section.material not in self.materials:
                raise ValueError(f'** ERROR! **: section {section.material} not found in the Model!')
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

    def add_element(self, element, part):
        """Add a compas_fea2 Element object to a Part in the Model.

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
        part = self._check_part_in_model(part)
        if isinstance(element.section, str):
            if element.section not in self.sections:
                if element.section in part.sections:
                    self.sections[element.section] = part.sections[element.section]
                else:
                    raise ValueError('ERROR: section {} not found in the Model!'.format(element.section.__repr__()))
            else:
                element._section = self.sections[element.section]
        part.add_element(element)

    def add_elements(self, elements, part):
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
            self.add_element(element, part)

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
        for element in elements:
            self.remove_node(element, part)

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    def add_release(self, release, part):
        """Add an Element EndRelease object to the Model.

        Parameters
        ----------
        release : obj
            `EndRelase` object.
        part : str
            Name of the part where the nodes will be removed from.

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
        """Group parts together

        Parameters
        ----------
        name : str
            name of the group
        parts : list
            list containing the parts names to group
        """
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        group = m.PartsGroup(name=name, parts=parts)
        self._parts_groups[group.name] = group

    def add_group(self, group, part):
        """Add a Group object to a part in the Model at the instance level. Can
        be either a NodesGroup or an ElementsGroup.

        Parameters
        ----------
        group : obj
            group object.
        part : str, obj
            Part name or Part object.

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
        part : str
            Name of the part the group belongs to.

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
        """Add a Constraint object to the Model.

        Parameters
        ----------
        constraint : obj
            compas_fea2 Contraint object

        Returns
        -------
        None
        """
        self._constraints[constraint.name] = constraint

    def add_constraints(self, constraints):
        """Add multiple Constraint objects to the Model.

        Parameters
        ----------
        constraints : list
            list of Constraint objects to add.

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
                    raise ValueError(f"overconstrained node: {self.parts[part].nodes[node]}")
                else:
                    self._bcs[part][node] = bc

    def add_bc_type(self, name, bc_type, part, nodes, axes='global'):
        """Add a BoundaryCondition to nodes in a part by type.

        Note
        ----
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
        """Add a fixed boundary condition type to some nodes in a part.

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
        raise NotImplementedError()

    # =========================================================================
    #                          Helper methods
    # =========================================================================

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
            Dictionary with the Node object for each Part.
            key =  Part name
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
            print(f"WARNING: Node at {xyz} not found!")

        return node_dict

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
        None
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
