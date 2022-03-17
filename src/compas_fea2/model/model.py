from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# import pickle
# import os
import importlib

# import compas_fea2
from compas_fea2 import config

from compas_fea2.base import FEAData
from compas_fea2.model.parts import Part
from compas_fea2.model.materials import Material
from compas_fea2.model.sections import Section
from compas_fea2.model.bcs import BoundaryCondition
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import ElementsGroup


class Model(FEAData):
    """Class representing an FEA model.

    Parameters
    ----------
    description : str
        Some description of the model.
        This will be added to the input file and can be useful for future reference.
    author : str
        The name of the author of the model.
        This will be added to the input file and can be useful for future reference.

    Attributes
    ----------
    description : str
        Some description of the model.
        This will be added to the input file and can be useful for future reference.
    author : str
        The name of the author of the model.
        This will be added to the input file and can be useful for future reference.
    parts : Set[:class:`compas_fea2.model.Part`]
        The parts of the model.
    materials : Set[:class:`compas_fea2.model.Material`]
        The materials of the model.
    materials : Set[:class:`compas_fea2.model.Material`]
        The materials used in the model.
    sections : Set[:class:`compas_fea2.model.Section`]
        The sections used in the model.
    bcs : Set[:class:`compas_fea2.model.BoundaryCondition`]
        The boundary conditions of the model.
    constraints : Set[:class:`compas_fea2.model.Constraint`]
        The constraints of the model.
    interactions : Set[:class:`compas_fea2.model.Interaction`]
        The interactions between parts of the model.
    contacts : Set[:class:`compas_fea2.model.Contact`]
        The contacts between parts of the model.
    partgroups : Set[:class:`compas_fea2.model.PartGroup`]
        The part groups of the model.
    surfaces : Set[:class:`compas_fea2.model.surface`]
        The surfaces of the model.

    """

    def __init__(self, *, description, author, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.description = description
        self.author = author
        self._parts = set()
        self._materials = set()
        self._sections = set()
        self._bcs = set()
        self._constraints = set()
        self._interactions = set()
        self._contacts = set()
        self._partgroups = set()
        self._surfaces = set()

    @property
    def parts(self):
        return self._parts

    @property
    def materials(self):
        return self._materials

    @property
    def sections(self):
        return self._sections

    @property
    def partgroups(self):
        return self._partgroups

    @property
    def bcs(self):
        return self._bcs

    @property
    def contacts(self):
        return self._contacts

    @property
    def constraints(self):
        return self._constraints

    @property
    def interactions(self):
        return self._interactions

    @property
    def surfaces(self):
        return self._surfaces

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    def from_network(self, network):
        raise NotImplementedError

    def from_assembly(self, assembly):
        raise NotImplementedError

    # @classmethod
    # def frame_from_mesh(cls, name, part_name, mesh, beam_section, author=None, description=None):
    #     """Creates a Model object from a compas Mesh object [WIP]. The edges of
    #     the mesh become the BeamElements of the frame. Currently, the same section
    #     is applied to all the elements.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the new Model.
    #     part_name : str
    #         name of the new part.
    #     mesh : obj
    #         Mesh to convert to import as a Model.
    #     beam_section : obj
    #         compas_fea2 BeamSection object to to apply to the frame elements.
    #     """
    #     m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
    #     model = cls(name)
    #     part = m.Part.frame_from_mesh(part_name, mesh, beam_section)
    #     model.add_part(part)
    #     return model

    # @classmethod
    # def shell_from_mesh(cls, name, part_name, mesh, shell_section):
    #     """Create a Model object from a compas Mesh object [WIP]. The faces of
    #     the mesh become ShellElement objects. Currently, the same section
    #     is applied to all the elements.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the new Model.
    #     part_name : str
    #         name of the new part.
    #     mesh : obj
    #         Mesh to convert to import as a Model.
    #     shell_section : obj
    #         compas_fea2 ShellSection object to to apply to the shell elements.
    #     """
    #     m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
    #     model = cls(name)
    #     part = m.Part.shell_from_mesh(part_name, mesh, shell_section)
    #     model.add_part(part)
    #     return model

    # @classmethod
    # def shell_from_gmesh(cls, name, part_name, gmshModel, shell_section):
    #     """Creates a Model object from a gmsh Model object [WIP]. The faces of
    #     the mesh become the elements of the shell. Currently, the same section
    #     is applied to all the elements.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the new Model.
    #     part_name : str
    #         name of the new Part.
    #     gmshModel : obj
    #         gmsh Model to convert.
    #     shell_section : obj
    #         compas_fea2 ShellSection object to to apply to the shell elements.
    #     """
    #     m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
    #     model = cls(name)
    #     part = m.Part.shell_from_gmesh(part_name, gmshModel, shell_section)
    #     model.add_part(part)
    #     return model

    # @classmethod
    # def from_volmesh(cls, name, part_name, volmesh):
    #     raise NotImplementedError()

    # @classmethod
    # def from_solid(cls, name, part_name, solid):
    #     raise NotImplementedError()

    # @classmethod
    # def from_compas_part(cls, name, part_name, part):
    #     raise NotImplementedError()

    # @classmethod
    # def from_compas_assembly(cls, name, part_name, assembly):
    #     raise NotImplementedError()

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    # def _check_part_in_model(self, part):
    #     """Check if the part is already in the model and in case add it.
    #     If `part` is of type :class:`str`, check if the part is already defined.
    #     If `part` is of type :class:`Part`, add the part to the Model if not
    #     already defined.

    #     Parameters
    #     ----------
    #     part : str or obj
    #         Name of the Part or Part object to check.

    #     Returns
    #     -------
    #     obj
    #         type :class:`Part` object

    #     Raises
    #     ------
    #     ValueError
    #         if `part` is a string and the part is not defined in the model
    #     TypeError
    #         `part` must be either an instance of a `compas_fea2` :class:`Part`
    #         or the name of a :class:`Part` already defined in the Model.
    #     """
    #     if isinstance(part, str):
    #         if part not in self.parts:
    #             raise ValueError(f'{part} not found in the Model')
    #         part_name = part
    #     elif isinstance(part, Part):
    #         if part.name not in self.parts:
    #             self.add_part(part)
    #             print(f'{part.__repr__()} added to the Model')
    #         part_name = part.name
    #     else:
    #         raise TypeError(
    #             f'{part} is either not an instance of a compas_fea2 Part class or not found in the Model')

    #     return self.parts[part_name]

    def find_parts_by_name(self, name):
        """Find all the parts with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Part`]

        """
        return [part for part in self.parts if part.name == name]

    def contains_part(self, part):
        """Verify that the model contains a specific part.

        Parameters
        ----------
        part : :class:`compas_fea2.model.Part`

        Returns
        -------
        bool

        """
        return part in self.parts

    def add_part(self, part):
        """Adds a Part to the Model.

        Parameters
        ----------
        part : :class:`compas_fea2.model.Part`

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the part is not a part.

        """
        if not isinstance(part, Part):
            raise TypeError("{!r} is not a part.".format(part))

        if self.contains_part(part):
            if config.VERBOSE:
                print("SKIPPED: Part {!r} is already in the model.".format(part))
            return

        part.model = self

        self.add_materials(part.materials)
        self.add_sections(part.sections)
        self._parts.add(part)

    def add_parts(self, parts):
        """Add multiple parts to the model.

        Parameters
        ----------
        parts : list[:class:`compas_fea2.model.Part`]

        Returns
        -------
        None

        """
        for part in parts:
            self.add_part(part)

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
        """Add a :class:`Material` subclass object to the Model so that it can be
        later refernced and used in the section and element definitions.

        Parameters
        ----------
        material : obj
            :class:`Material` object to be added.

        Returns
        -------
        None
        """
        if material.name not in self.materials:
            self._materials[material._name] = material
        else:
            print('NOTE: {} already added to the model. skipped!'.format(material))

    def add_materials(self, materials):
        """Add multiple :class:`Material` subclass objects to the Model so
        that they can be later refernced and used in section and element definitions.

        Parameters
        ----------
        material : list
            List of :class:`Material` objects.

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
        """Add a :class:`Section` subclass object to the Model o that it can be later
        refernced and used in an element definition.

        Parameters
        ----------
        section : obj
            :class:`Section` subclass object to be added.

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
        elif isinstance(section.material, Material):
            if section.material.name not in self.materials:
                self._materials[section.material.name] = section.material
        else:
            raise TypeError(
                "The material for the the section must be either the name of a previously added Material or an instance of a Material object")

        if isinstance(section, Section):
            if section._name not in self._sections:
                self._sections[section._name] = section
            else:
                print('WARNING: {} already added to the model. skipped!'.format(section))
        else:
            raise TypeError('Provide a valid Section subclass object')

    def add_sections(self, sections):
        """Add multiple :class:`Section`subclass  objects to the Model.

        Parameters
        ----------
        sections : list
            list of :class:`Section` subclass objects.

        Returns
        -------
        None
        """
        for section in sections:
            self.add_section(section)

    # =========================================================================
    #                           Elements methods
    # =========================================================================

    # def add_element(self, element, part, check=False):
    #     """Add a :class:`ElementBase` subclass object to a part in the Model.

    #     Note
    #     ----
    #     Elements are defined at the part level. The element added is stored in
    #     the specified part. However, the section and material associaceted are
    #     added to tthe model, if not already present.

    #     Parameters
    #     ----------
    #     element : obj
    #         :class:`ElementBase` subclass object to be added.
    #     part : str, obj
    #         Name of the part or :class:`Part` object where the node will be
    #         added.
    #     check : bool, optional
    #         If ``True``, checks if the node connected by the element are present.
    #         This is a quite resource-intense operation! Set to ``False`` for large
    #         parts (>10000 nodes). By default ``False``

    #     Returns
    #     -------
    #     int
    #         element key
    #     """
    #     part = self._check_part_in_model(part)
    #     if isinstance(element.section, str):
    #         if element.section not in self.sections:
    #             if element.section in part.sections:
    #                 self.sections[element.section] = part.sections[element.section]
    #             else:
    #                 raise ValueError(f'ERROR: section {element.section.__repr__()} not found in the Model!')
    #         else:
    #             element._section = self.sections[element.section]
    #     return part.add_element(element, check)

    # def add_elements(self, elements, part, check=False):
    #     """Adds multiple :class:`ElementBase` subclass objects to a part in the Model.

    #     Parameters
    #     ----------
    #     elements : list
    #         List of compas_fea2 Element subclass objects.
    #     part : str, obj
    #         Name of the part or :class:`Part` object where the node will be
    #         added.
    #     check : bool
    #         If True, checks if the element keys are in the model. This is a quite
    #         resource-intense operation! Set to `False` for large models (>10000
    #         nodes)

    #     Return
    #     ------
    #     list of int
    #         list with the keys of the added nodes.
    #     """
    #     return [self.add_element(element, part, check) for element in elements]

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    # def add_release(self, release, part):
    #     """Add an Element EndRelease object to the Model.

    #     Parameters
    #     ----------
    #     release : obj
    #         `EndRelase` object.
    #     part : str, obj
    #         Name of the part or :class:`Part` object where the node will be
    #         added.

    #     Returns
    #     -------
    #     None
    #     """
    #     part = self._check_part_in_model(part)
    #     part.add_release(release)

    # def add_releases(self, releases, part):
    #     """Add multiple Element EndRelease objects to the Model.

    #     Parameters
    #     ----------
    #     releases : list
    #         list of `EndRelase` object.
    #     part : str
    #         Name of the part where the nodes will be removed from.

    #     Returns
    #     -------
    #     None
    #     """
    #     for release in releases:
    #         self.add_release(release, part)

    # =========================================================================
    #                           Groups methods
    # =========================================================================

    # def group_parts(self, name, parts):
    #     """Group parts together.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the group
    #     parts : list of str
    #         list containing the parts names to group

    #     Returns
    #     -------
    #     None
    #     """
    #     m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
    #     group = m.PartsGroup(name=name, parts=parts)
    #     self._parts_partgroups[group.name] = group

    # # NOTE: Nodes and Elements groups should not be added but defined (similarly to what happens for Parts)
    # def add_group(self, group, part):
    #     """Add a Group object to a part in the Model. it can be either a
    #     :class:`NodesGroupBase` or an :class:`ElementsGroupBase`.

    #     Parameters
    #     ----------
    #     group : obj
    #         :class:`NodesGroupBase` or :class:`ElementsGroupBase` object to add.
    #     part : str, obj
    #         Name of the part or :class:`Part` object where the node will be
    #         added.

    #     Returns
    #     -------
    #     None
    #     """
    #     part = self._check_part_in_model(part)
    #     part.add_group(group)

    # def add_partgroups(self, groups, part):
    #     """Add multiple Group objects to a part in the Model. Can be
    #     a list of NodesGroup or ElementsGroup objects, also mixed.

    #     Parameters
    #     ----------
    #     group : obj
    #         group object.
    #     part : str, obj
    #         Name of the part or :class:`Part` object where the node will be
    #         added.

    #     Returns
    #     -------
    #     None
    #     """
    #     for group in groups:
    #         self.add_group(group, part)

    # def add_nodes_group(self, name, part, nodes):
    #     """Add a :class:`NodeGroupBase` object to the the part in the model.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the group.
    #     part : str
    #         name of the part
    #     nodes : list
    #         list of nodes keys to group

    #     Returns
    #     -------
    #     None
    #     """
    #     part = self._check_part_in_model(part)
    #     part.add_nodes_group(name, nodes)

    # def add_elements_group(self, name, part, elements):
    #     """Add a :class:`ElementGroupBase` object to a part in the model.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the group.
    #     part : str
    #         name of the part
    #     elements : list
    #         list of elements keys to group

    #     Returns
    #     -------
    #     None
    #     """
    #     part = self._check_part_in_model(part)
    #     part.add_elements_group(name, elements)

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
    def add_bc(self, bc, where, part):
        """Adds a :class:`compas_fea2.model.GeneralBC` to the Problem object.

        Parameters
        ----------
        bc : obj
            :class:`BoundaryCondition` object.
        nodes : list
            list with the node keys where to assign the boundary condition.
        part : str, obj
            Name of the part or :class:`Part` object where the node will be
            added.

        Returns
        -------
        None
        """
        part = self._check_part_in_model(part)

        if isinstance(where, int):
            nodes = [where]
        elif isinstance(where, (list, tuple)):
            nodes = where
        elif isinstance(where, NodesGroup):
            nodes = where.keys
        else:
            raise TypeError('You must provide either a key or a list of keys, or a NodesGroupBase subclass instance')
        # self._check_nodes_in_model(nodes) #TODO implement method

        if not isinstance(bc, BoundaryCondition):
            raise TypeError(f'{bc} not instance of a BC class')

        self._bcs.setdefault(part.name, {})[bc] = nodes

    def add_bc_type(self, name, bc_type, part, where, axes='global'):
        """Add a :class:`GeneralBCBase` subclass to some nodes in a part by type.

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
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        types = {'fix': 'FixedBC', 'fixXX': 'FixedBCXX', 'fixYY': 'FixedBCYY',
                 'fixZZ': 'FixedBCZZ', 'pin': 'PinnedBC', 'rollerX': 'RollerBCX',
                 'rollerY': 'RollerBCY', 'rollerZ': 'RollerBCZ', 'rollerXY': 'RollerBCXY',
                 'rollerYZ': 'RollerBCYZ', 'rollerXZ': 'RollerBCXZ',
                 }
        m = importlib.import_module('.'.join(self.__module__.split('.')[:-1]))
        bc = getattr(m, types[bc_type])(name, axes)
        self.add_bc(bc, where, part)

    def add_fix_bc(self, name, part, where, axes='global'):
        """Add a :class:`FixedBCBase` to the nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fix', part, where)

    def add_fixXX_bc(self, name, part, where, axes='global'):
        """Add a fixed boundary condition type free about XX to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fixXX', part, where)

    def add_fixYY_bc(self, name, part, where, axes='global'):
        """Add a fixed boundary condition free about YY type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fixYY', part, where)

    def add_fixZZ_bc(self, name, part, where, axes='global'):
        """Add a fixed boundary condition free about ZZ type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'fixZZ', part, where)

    def add_pin_bc(self, name, part, where):
        """Add a pinned boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'pin', part, where)

    def add_rollerX_bc(self, name, part, where):
        """Add a roller free on X boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerX', part, where)

    def add_rollerY_bc(self, name, part, where):
        """Add a roller free on Y boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerY', part, where)

    def add_rollerZ_bc(self, name, part, where):
        """Add a roller free on Z boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerZ', part, where)

    def add_rollerXY_bc(self, name, part, where):
        """Add a roller free on XY boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerXY', part, where)

    def add_rollerXZ_bc(self, name, part, where):
        """Add a roller free on XZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerXZ', part, where)

    def add_rollerYZ_bc(self, name, part, where):
        """Add a roller free on YZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        part : str
            name of the part where the boundary condition is applied
        where : int or list(int), obj
            It can be either a key or a list of keys, or a :class:`NodesGroupBase` subclass instance
            of the nodes where the boundary condition is applied.
        axes : str, optional
            [axes of the boundary condition, by default 'global'
        """
        self.add_bc_type(name, 'rollerYZ', part, where)

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
    # Save model file
    # ==============================================================================

    def check(self, type='quick'):
        """Check for possible problems in the model

            Warning
            -------
            WIP! It is better if you check yourself...

            Parameters
            ----------
            type : str, optional
                *quick* or *deep* check, by default 'quick'

            Returns
            -------
            str
                report
            """

        def _check_units(self):
            """Check if the units are consistent.
            """
            raise NotImplementedError()

        def _check_bcs(self):
            """Check if the units are consistent.
            """
            raise NotImplementedError()

        raise NotImplementedError()

    # ==============================================================================
    # Viewer
    # ==============================================================================

    # def save_to_cfm(self, path, output=True):
    #     """Exports the Model object to an .cfm file through Pickle.

    #     Parameters
    #     ----------
    #     path : path
    #         Path to the folder where save the file to.
    #     output : bool
    #         Print terminal output.

    #     Returns
    #     -------
    #     None
    #     """

    #     if not os.path.exists(path):
    #         os.makedirs(path)

    #     filename = '{0}/{1}.cfm'.format(path, self.name)

    #     with open(filename, 'wb') as f:
    #         pickle.dump(self, f)

    #     if output:
    #         print('***** Model saved to: {0} *****\n'.format(filename))

    # # ==============================================================================
    # # Load model file
    # # ==============================================================================

    # @ staticmethod
    # def load_from_cfm(filename, output=True):
    #     """Imports a Model object from an .cfm file through Pickle.

    #     Parameters
    #     ----------
    #     filename : str
    #         Path to load the Model .cfm from.
    #     output : bool
    #         Print terminal output.

    #     Returns
    #     -------
    #     obj
    #         Imported Model object.
    #     """
    #     with open(filename, 'rb') as f:
    #         mdl = pickle.load(f)

    #     if output:
    #         print('***** Model loaded from: {0} *****'.format(filename))

    #     return mdl
