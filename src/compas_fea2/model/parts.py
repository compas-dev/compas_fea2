from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from binascii import rlecode_hqx

# import importlib
# import numpy as np

from compas.geometry import normalize_vector
from compas.geometry import distance_point_point_sqrd

from compas_fea2 import config
from compas_fea2.base import FEAData

from .nodes import Node
from .elements import _Element, BeamElement, ShellElement, SolidElement
from .materials import _Material
from .sections import _Section, ShellSection, SolidSection
from .releases import _BeamEndRelease, BeamEndPinRelease
from .groups import NodesGroup, ElementsGroup


class Part(FEAData):
    """Base class for all parts.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    model : :class:`compas_fea2.model.Model`
        The parent model of the part.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    model : :class:`compas_fea2.model.Model`
        The parent model of the part.
    nodes : Set[:class:`compas_fea2.model.Node`]
        The nodes belonging to the part.
    materials : Set[:class:`compas_fea2.model.Material`]
        The materials belonging to the part.
    sections : Set[:class:`compas_fea2.model.Section`]
        The sections belonging to the part.
    elements : Set[:class:`compas_fea2.model.Element`]
        The elements belonging to the part.
    releases : Set[:class:`compas_fea2.model.Release`]
        The releases belonging to the part.
    groups : Set[:class:`compas_fea2.model.Group`]
        The groups belonging to the part.

    """

    def __init__(self, model=None, name=None, **kwargs):
        super(Part, self).__init__(name=name, **kwargs)
        self._model = model
        self._nodes = set()
        self._materials = set()
        self._sections = set()
        self._elements = set()
        self._releases = set()
        self._groups = set()
        self._gkey_node = {}

    @property
    def model(self):
        return self._model

    @property
    def nodes(self):
        return self._nodes

    @property
    def materials(self):
        return self._materials

    @property
    def sections(self):
        return self._sections

    @property
    def elements(self):
        return self._elements

    @property
    def releases(self):
        return self._releases

    @property
    def groups(self):
        return self._groups

    @property
    def gkey_node(self):
        return self._gkey_node

    def __str__(self):
        return """
{}
{}
name : {}

number of elements : {}
number of nodes    : {}
number of groups   : {}
""".format(self.__class__.__name__,
           len(self.__class__.__name__) * '-',
           self.name,
           len(self.elements),
           len(self.nodes),
           len(self.groups))

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    @classmethod
    def from_network(self, network):
        raise NotImplementedError()

    @classmethod
    def from_obj(self, obj):
        raise NotImplementedError()

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
    def frame_from_compas_mesh(cls, mesh, section, name=None, **kwargs):
        """Creates a Part object from a a :class:`compas.datastructures.Mesh`.
        To each edge of the mesh is assigned a :class:`compas_fea2.model.BeamElement`.
        Currently, the same section is applied to all the elements.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            Mesh to convert to a Part.
        section : :class:`compas_fea2.model.BeamSection`
            Section to assign to the frame elements.
        name : str, optional
            name of the new part.

        """
        part = cls(name=name, **kwargs)
        vertex_node = {vertex: part.add_node(Node(mesh.vertex_coordinates(vertex))) for vertex in mesh.vertices()}

        for edge in mesh.edges():
            nodes = [vertex_node[vertex] for vertex in edge]
            v = mesh.edge_direction(*edge)
            v.append(v.pop(0))
            part.add_element(BeamElement(nodes=[*nodes], section=section, frame=v))

        return part

    @ classmethod
    def shell_from_compas_mesh(cls, mesh, section, name=None, **kwargs):
        """Creates a Part object from a :class:`compas.datastructures.Mesh`.
        To each face of the mesh is assigned a :class:`compas_fea2.model.ShellElement`
        objects. Currently, the same section is applied to all the elements.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            Mesh to convert to a Part.
        section : :class:`compas_fea2.model.ShellElement`
            Shell section assigned to each face.
        name : str, optional
            name of the new part. If ``None``, a unique identifier is assigned
            automatically.

        """
        part = cls(name, **kwargs)

        vertex_node = {vertex: part.add_node(Node(mesh.vertex_coordinates(vertex))) for vertex in mesh.vertices()}

        for face in mesh.faces():
            nodes = [vertex_node[vertex] for vertex in mesh.face_vertices(face)]
            element = ShellElement(nodes=nodes, section=section)
            part.add_element(element)

        return part

    @ classmethod
    def from_gmsh(cls, gmshModel, section, split=False, verbose=False, check=False, name=None, **kwargs):
        """Create a Part object from a gmshModel object. According to the `section`
        type provided, SolidElement or ShellElement elements are cretated.
        The same section is applied to all the elements.

        Note
        ----
        The gmshModel must have the right dimension corresponding to the section
        provided.

        Parameters
        ----------
        name : str
            name of the new part.
        gmshModel : obj
            gmsh Model to convert. See [1]_
        section : obj
            `compas_fea2` :class:`SolidSection` or :class:`ShellSection` sub-class
            object to to apply to the elements.
        split : bool, optional
            if ``True`` create an additional node in the middle of the edges of the
            elements to implement more refined element types. Check for example [2]_.
        verbose : bool, optional
            if ``True`` print a log, by default False
        check : bool, optional
            if ``True`` performs sanity checks, by default False. This is a quite
            resource-intense operation! Set to ``False`` for large models (>10000
            nodes).

        Returns
        -------
        obj
            compas_fea2 `Part` object.

        References
        ----------
        .. [1] https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_9_1/api/gmsh.py
        .. [2] https://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node33.html

        Examples
        --------
        >>> gmshModel = gmsh.mode.generate(3)
        >>> mat = ElasticIsotropic(name='mat', E=29000, v=0.17, density=2.5e-9)
        >>> sec = SolidSection('mysec', mat)
        >>> part = Part.from_gmsh('part_gmsh', gmshModel, sec)

        """
        import numpy as np
        part = cls(name=name, **kwargs)
        # part.add_section(section)
        # add nodes
        gmsh_nodes = gmshModel.mesh.get_nodes()
        node_coords = gmsh_nodes[1].reshape((-1, 3), order='C')
        gmsh_elements = gmshModel.mesh.get_elements()
        fea2_nodes = [part.add_node(Node(coords.tolist())) for coords in node_coords]

        # for coords in node_coords:
        #     k = part.add_node(Node(coords.tolist()))
        #     if verbose:
        #         print(f'node {k} added')
        # add elements
        if isinstance(section, SolidSection):
            ntags_per_element = np.split(gmsh_elements[2][2]-1, len(gmsh_elements[1][2]))  # gmsh keys start from 1
            for ntags in ntags_per_element:
                # if split:
                # iteritools combinations
                # for comb in combs:
                # midpoint a b
                # k = add node
                k = part.add_element(SolidElement(nodes=[fea2_nodes[ntag] for ntag in ntags], section=section), check)
                if verbose:
                    print(f'element {k} added')
        if isinstance(section, ShellSection):
            ntags_per_element = np.split(gmsh_elements[2][1]-1, len(gmsh_elements[1][1]))  # gmsh keys start from 1
            for ntags in ntags_per_element:
                k = part.add_element(ShellElement(nodes=[fea2_nodes[ntag] for ntag in ntags], section=section))
                if verbose:
                    print(f'element {k} added')
        print('\ncompas_fea2 model generated!\n')
        return part

    # @classmethod
    # def from_compas_part(cls, name, part):
    #     raise NotImplementedError()

    # @classmethod
    # def from_volmesh(self, name, volmesh):
    #     raise NotImplementedError()

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def find_nodes_by_name(self, name):
        """Find all nodes with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        return [node for node in self.nodes if node.name == name]

    def find_nodes_by_location(self, point, distance):
        """Find all nodes within a distance of a given geometrical location.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            A geometrical location.
        distance : float
            Distance from the location.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        d2 = distance ** 2
        matched = []
        for node in self.nodes:
            if distance_point_point_sqrd(node.xyz, point) < d2:
                matched.append(node)
        return matched

    def contains_node(self, node):
        """Verify that the part contains a given node.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`

        Returns
        -------
        bool

        """
        return node in self.nodes

    def add_node(self, node):
        """Add a node to the part.

        Note
        ----
        By adding a Node to the part, this gets registered to this part.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node.

        Return
        ------
        :class:`compas_fea2.model.Node`
            The identifier of the node in the part.

        Raises
        ------
        TypeError
            If the node is not a node.

        Examples
        --------
        >>> part = Part()
        >>> node = Node(1.0, 2.0, 3.0)
        >>> part.add_node(node)

        """
        if not isinstance(node, Node):
            raise TypeError('{!r} is not a node.'.format(node))

        if self.contains_node(node):
            if config.VERBOSE:
                print('SKIPPED: Node {!r} already in part.'.format(node))
            return

        node._key = len(self._nodes)
        self._nodes.add(node)
        self._gkey_node[node.gkey] = node
        node._part = self
        if config.VERBOSE:
            print('Node {!r} registered to {!r}.'.format(node, self))
        return node

    def add_nodes(self, nodes):
        """Add multiple nodes to the part.

        Parameters
        ----------
        nodes : list[:class:`compas_fea2.model.Node`]
            The list of nodes.

        Return
        ------
        list[:class:`compas_fea2.model.Node`]
            The identifiers of the nodes in the part.

        Examples
        --------
        >>> part = Part()
        >>> node1 = Node([1.0, 2.0, 3.0])
        >>> node2 = Node([3.0, 4.0, 5.0])
        >>> node3 = Node([3.0, 4.0, 5.0])
        >>> nodes = part.add_nodes([node1, node2, node3])

        """
        return [self.add_node(node) for node in nodes]

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def find_materials_by_name(self, name):
        """Find all materials with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Material`]

        """
        return [material for material in self.materials if material.name == name]

    def contains_material(self, material):
        """Verify that the part contains a specific material.

        Parameters
        ----------
        material : :class:`compas_fea2.model.Material`

        Returns
        -------
        bool

        """
        return material in self.materials

    def add_material(self, material):
        """Add a material to the part so that it can be referenced in section and element definitions.

        Parameters
        ----------
        material : :class:`compas_fea2.model.Material`

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the material is not a material.

        """
        if not isinstance(material, _Material):
            raise TypeError('{!r} is not a material.'.format(material))

        if self.contains_material(material):
            if config.VERBOSE:
                print('SKIPPED: Material {!r} already in part.'.format(material))
            return

        self._materials.add(material)

    def add_materials(self, materials):
        """Add multiple materials to the part.

        Parameters
        ----------
        materials : list[:class:`compas_fea2.model.Material`]

        Returns
        -------
        None

        """
        for material in materials:
            self.add_material(material)

    # =========================================================================
    #                        Sections methods
    # =========================================================================

    def find_sections_by_name(self, name):
        """Find all sections with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Section`]

        """
        return [section for section in self.sections if section.name == name]

    def contains_section(self, section):
        """Verify that the part contains a specific section.

        Parameters
        ----------
        section : :class:`compas_fea2.model.Section`

        Returns
        -------
        bool

        """
        return section in self.sections

    def add_section(self, section):
        """Add a section to the part so that it can be referenced in element definitions.

        Parameters
        ----------
        section : :class:`compas_fea2.model.Section`

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the section is not a section.

        """
        if not isinstance(section, _Section):
            raise TypeError('{!r} is not a section.'.format(section))

        if self.contains_section(section):
            if config.VERBOSE:
                print("SKIPPED: Section {!r} already in part.".format(section))
            return

        self.add_material(section.material)
        self._sections.add(section)

    def add_sections(self, sections):
        """Add multiple sections to the part.

        Parameters
        ----------
        sections : list[:class:`compas_fea2.model.Section`]

        Returns
        -------
        None

        """
        for section in sections:
            self.add_section(section)

    # =========================================================================
    #                           Elements methods
    # =========================================================================

    def find_elements_by_name(self, name):
        """Find all elements with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Element`]

        """
        return [element for element in self.elements if element.name == name]

    def contains_element(self, element):
        """Verify that the part contains a specific element.

        Parameters
        ----------
        element : :class:`compas_fea2.model.Element`

        Returns
        -------
        bool

        """
        return element in self.elements

    def add_element(self, element):
        """Add an element to the part.

        Parameters
        ----------
        element : :class:`compas_fea2.model.Element`
            The element instance.

        Returns
        -------
        :class:`compas_fea2.model.Element`

        Raises
        ------
        TypeError
            If the element is not an element.

        """
        if not isinstance(element, _Element):
            raise TypeError('{!r} is not an element.'.format(element))

        if self.contains_element(element):
            if config.VERBOSE:
                print("SKIPPED: Element {!r} already in part.".format(element))
            return

        self.add_nodes(element.nodes)
        self.add_section(element.section)
        element._key = len(self.elements)
        self.elements.add(element)
        element._part = self
        if config.VERBOSE:
            print('Element {!r} registered to {!r}.'.format(element, self))
        return element

    def add_elements(self, elements):
        """Add multiple elements to the part.

        Parameters
        ----------
        elements : list[:class:`compas_fea2.model.Element`]

        Return
        ------
        list[:class:`compas_fea2.model.Element`]

        """
        return [self.add_element(element) for element in elements]

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    def add_beam_release(self, element, location, release):
        """Add a :class:`compas_fea2.model.BeamEndRelease` to an element in the
        part.

        Parameters
        ----------
        element : :class:`compas_fea2.model.BeamElement`
            The element to release.
        location : str
            'start' or 'end'.
        release : :class:`compas_fea2.model.BeamEndRelease`
            Release type to apply.
        """
        if not isinstance(release, _BeamEndRelease):
            raise TypeError('{!r} is not a beam release element.'.format(release))
        release.element = element
        release.location = location
        self._releases.add(release)
        return release

    # =========================================================================
    #                           Groups methods
    # =========================================================================

    def find_groups_by_name(self, name):
        """Find all groups with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Group`]

        """
        return [group for group in self.groups if group.name == name]

    def contains_group(self, group):
        """Verify that the part contains a specific group.

        Parameters
        ----------
        group : :class:`compas_fea2.model.Group`

        Returns
        -------
        bool

        """
        return group in self.groups

    def add_group(self, group):
        """Add a node or element group to the part.

        Parameters
        ----------
        group : :class:`compas_fea2.model.NodeGroup` | :class:`compas_fea2.model.ElementGroup`

        Return
        ------
        None

        Raises
        ------
        TypeError
            If the group is not a node or element group.

        """
        if not isinstance(group, (NodesGroup, ElementsGroup)):
            raise TypeError("{!r} is not a node or element group.".format(group))

        if isinstance(group, NodesGroup):
            self.add_nodes(group.nodes)
        elif isinstance(group, ElementsGroup):
            self.add_elements(group.elements)

        if self.contains_group(group):
            if config.VERBOSE:
                print("SKIPPED: Group {!r} already in part.".format(group))
            return

        self._groups.add(group)
        return group

    def add_groups(self, groups):
        """Add multiple groups to the part.

        Parameters
        ----------
        groups : list[:class:`compas_fea2.model.Group`]

        Return
        ------
        list[:class:`compas_fea2.model.Group`]

        """
        return [self.add_group(group) for group in groups]
