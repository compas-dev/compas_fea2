from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# import importlib
# import numpy as np

# from compas.geometry import normalize_vector

from compas_fea2 import config
from compas_fea2.base import FEAData

from .nodes import Node
from .elements import Element
from .materials import Material
from .sections import Section
# from .sections import SolidSection
# from .sections import ShellSection
from .groups import NodesGroup
from .groups import ElementsGroup


class Part(FEAData):
    """Base class for all parts.

    Parameters
    ----------
    model : :class:`compas_fea2.model.Model`
        The parent model of the part.

    Attributes
    ----------
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
    groups : Set[:class:`compas_fea2.model.Group`]
        The groups belonging to the part.

    """

    def __init__(self, model=None, **kwargs):
        super(Part, self).__init__(**kwargs)
        self._model = model
        self._nodes = set()
        self._materials = set()
        self._sections = set()
        self._elements = set()
        self._groups = set()
        self.gkey_node = {}

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
    def groups(self):
        return self._groups

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

    # @classmethod
    # def frame_from_mesh(cls, name, mesh, beam_section):
    #     """Creates a ``Part`` object from a compas Mesh object [WIP]. The edges of
    #     the mesh become the BeamElements of the frame. Currently, the same section
    #     is applied to all the elements.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the new part.
    #     mesh : obj
    #         Mesh to convert to import as a Model.
    #     beam_section : obj
    #         compas_fea2 BeamSection object to to apply to the frame elements.

    #     """
    #     m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
    #     part = cls(name)
    #     part.add_section(beam_section)

    #     for v in mesh.vertices():
    #         part.add_node(m.Node(mesh.vertex_coordinates(v)))

    #     # Generate elements between nodes
    #     key_index = mesh.key_index()
    #     # vertices = list(mesh.vertices())
    #     edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]

    #     for e in edges:
    #         # get elements orientation
    #         v = normalize_vector(mesh.edge_vector(e[0], e[1]))
    #         v.append(v.pop(0))
    #         # add element to the model
    #         part.add_element(m.BeamElement(connectivity=[e[0], e[1]], section=beam_section, orientation=v))

    #     return part

    # @classmethod
    # def shell_from_mesh(cls, name, mesh, shell_section):
    #     """Creates a Part object from a compas Mesh object [WIP]. The faces of
    #     the mesh become ShellElement objects. Currently, the same section
    #     is applied to all the elements.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the new part.
    #     mesh : obj
    #         Mesh to convert to import as a Model.
    #     shell_section : obj
    #         compas_fea2 ShellSection object to to apply to the shell elements.

    #     """
    #     m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
    #     part = cls(name)
    #     part.add_section(shell_section)

    #     for v in mesh.vertices():
    #         part.add_node(m.Node(mesh.vertex_coordinates(v)), 'part-1')

    #     # Generate elements between nodes
    #     key_index = mesh.key_index()
    #     faces = [[key_index[key]
    #               for key in mesh.face_vertices(face)] for face in mesh.faces()]

    #     for face in faces:
    #         part.add_element(m.ShellElement(connectivity=face, section=shell_section))

    #     return part

    # @classmethod
    # def from_gmsh(cls, name, gmshModel, section, split=False, verbose=False, check=False):
    #     """Create a Part object from a gmshModel object. According to the `section`
    #     type provided, SolidElement or ShellElement elements are cretated.
    #     The same section is applied to all the elements.

    #     Note
    #     ----
    #     The gmshModel must have the right dimension corresponding to the section
    #     provided.

    #     Parameters
    #     ----------
    #     name : str
    #         name of the new part.
    #     gmshModel : obj
    #         gmsh Model to convert. See [1]_
    #     section : obj
    #         `compas_fea2` :class:`SolidSection` or :class:`ShellSection` sub-class
    #         object to to apply to the elements.
    #     split : bool, optional
    #         if ``True`` create an additional node in the middle of the edges of the
    #         elements to implement more refined element types. Check for example [2]_.
    #     verbose : bool, optional
    #         if ``True`` print a log, by default False
    #     check : bool, optional
    #         if ``True`` performs sanity checks, by default False. This is a quite
    #         resource-intense operation! Set to ``False`` for large models (>10000
    #         nodes).

    #     Returns
    #     -------
    #     obj
    #         compas_fea2 `Part` object.

    #     References
    #     ----------
    #     .. [1] https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_9_1/api/gmsh.py
    #     .. [2] https://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node33.html

    #     Examples
    #     --------
    #     >>> gmshModel = gmsh.mode.generate(3)
    #     >>> mat = ElasticIsotropic(name='mat', E=29000, v=0.17, p=2.5e-9)
    #     >>> sec = SolidSection('mysec', mat)
    #     >>> part = Part.from_gmsh('part_gmsh', gmshModel, sec)

    #     """
    #     part = cls(name)
    #     m = importlib.import_module('.'.join(part.__module__.split('.')[:-1]))
    #     part.add_section(section)
    #     # add nodes
    #     nodes = gmshModel.mesh.get_nodes()
    #     node_coords = nodes[1].reshape((-1, 3), order='C')
    #     for coords in node_coords:
    #         k = part.add_node(m.Node(coords.tolist()), check)
    #         if verbose:
    #             print(f'node {k} added')
    #     # add elements
    #     elements = gmshModel.mesh.get_elements()
    #     if isinstance(section, SolidSection):
    #         ntags_per_element = np.split(elements[2][2]-1, len(elements[1][2]))  # gmsh keys start from 1
    #         for ntags in ntags_per_element:
    #             # if split:
    #             # iteritools combinations
    #             # for comb in combs:
    #             # midpoint a b
    #             # k = add node
    #             k = part.add_element(m.SolidElement(ntags, section), check)
    #             if verbose:
    #                 print(f'element {k} added')
    #     if isinstance(section, ShellSection):
    #         ntags_per_element = np.split(elements[2][1]-1, len(elements[1][1]))  # gmsh keys start from 1
    #         for ntags in ntags_per_element:
    #             k = part.add_element(m.ShellElement(ntags, section), check)
    #             if verbose:
    #                 print(f'element {k} added')
    #     print('\ncompas_fea2 model generated!\n')
    #     return part

    # @classmethod
    # def from_compas_part(cls, name, part):
    #     raise NotImplementedError()

    # @classmethod
    # def from_volmesh(self, name, volmesh):
    #     raise NotImplementedError()

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    # def find_node_in_part(self, node):
    #     """Checks if a node already exists in the Part in the same location.

    #     Parameters
    #     ----------
    #     node : :class:`compas_fea2.model.Node`
    #         compas_fea2 Node object.

    #     Returns
    #     -------
    #     :class:`compas_fea2.model.Node` | None
    #         The existing node in the same location.

    #     """
    #     gkey = node.gkey
    #     if gkey in self.gkey_node:
    #         return self.gkey_node[gkey]
    #     return None

    # def find_nodes_at_location(self, xyz, tol):
    #     """Finds (if any) the nodes in the model at specified coordinates.

    #     Parameters
    #     ----------
    #     xyz : list[float]
    #         List with the [x, y, z] coordinates.
    #     tol : int
    #         multiple to which round the coordinates.

    #     Returns
    #     -------
    #     list
    #         list with the keys of the maching nodes.
    #         key =  Part name
    #         value = Node object with the specified coordinates.
    #     """
    #     matches = []
    #     a = [tol * round(i/tol) for i in xyz]
    #     for node in self.nodes:
    #         b = [tol * round(i/tol) for i in node.xyz]
    #         if a == b:
    #             matches.append(node.key)
    #     return matches

    def add_node(self, node):
        """Add a node to the part.

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

        if node in self.nodes:
            if config.VERBOSE:
                print('SKIPPED: Node {!r} already in part.'.format(node))
            return

        node._key = len(self._nodes)
        if node not in self._nodes:
            self._nodes.add(node)
        self.gkey_node[node.gkey] = node
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

    # def remove_node(self, node):
    #     """Remove the node from the Part. If there are duplicate nodes, it
    #     removes also all the duplicates.

    #     Parameters
    #     ----------
    #     node : :class:`compas_fea2.model.Node`
    #         The node.

    #     Returns
    #     -------
    #     None
    #     """
    #     raise NotImplementedError()

    # def remove_nodes(self, nodes):
    #     """Remove the nodes from the Part.

    #     If there are duplicate nodes, it removes also all the duplicates.

    #     Parameters
    #     ----------
    #     nodes : list[:class:`compas_fea2.model.Node`]
    #         List of nodes.

    #     Returns
    #     -------
    #     None
    #     """
    #     raise NotImplementedError()

    # =========================================================================
    #                           Materials methods
    # =========================================================================

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
        if not isinstance(material, Material):
            raise TypeError('{!r} is not a material.'.format(material))

        if material in self.materials:
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
        if not isinstance(section, Section):
            raise TypeError('{!r} is not a section.'.format(section))

        if section in self._sections:
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

    # def _check_element_in_part(self, element):
    #     """Check if the element is already in the model and in case add it.
    #     If `element` is of type `str`, check if the element is already defined.
    #     If `element` is of type `Element`, add the element to the Part if not
    #     already defined.

    #     Warning
    #     -------
    #     the function does not check the elements connectivity. This could generate
    #     duplicate elements.

    #     Parameters
    #     ----------
    #     element : str or obj
    #         Name of the Part or Part object to check.

    #     Returns
    #     -------
    #     obj
    #         Part object

    #     Raises
    #     ------
    #     ValueError
    #         if `element` is a string and the element is not defined in the Part
    #     TypeError
    #         `element` must be either an instance of a `compas_fea2` Part class or the
    #         name of a Part already defined in the Problem.
    #     """
    #     if isinstance(element, str):
    #         if element not in self.elements:
    #             raise ValueError(f'{element} not found in the Part')
    #         element_name = element
    #     elif isinstance(element, Part):
    #         if element.name not in self.elements:
    #             self.add_element(element)
    #             print(f'{element.__repr__()} added to the Part')
    #         element_name = element.name
    #     else:
    #         raise TypeError(
    #             f'{element} is either not an instance of a `compas_fea2` Element class or not found in the Model')

    #     return self.elements[element_name]

    # def _reorder_elements(self):
    #     """Reorders the elements to have consecutive keys.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     None
    #     """

    #     k = 0
    #     for element in self._elements:
    #         element.key = k
    #         k += 1

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
        if not isinstance(element, Element):
            raise TypeError('{!r} is not an element.'.format(element))

        if element in self._elements:
            if config.VERBOSE:
                print("SKIPPED: Element {!r} already in part.".format(element))
            return

        self.add_nodes(element.nodes)
        self.add_section(element.section)
        element._key = len(self.elements)
        self.elements.add(element)
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

    # def remove_element(self, element_key):
    #     """Removes the element from the Part.

    #     Parameters
    #     ----------
    #     element_key : int
    #         Key number of the element to be removed.

    #     Returns
    #     -------
    #     None

    #     """
    #     raise NotImplementedError()
    #     # # TODO check if element key exists
    #     # del self.elements[element_key]
    #     # self._reorder_elements()

    # def remove_elements(self, elements):
    #     """Removes the elements from the Part.

    #     Parameters
    #     ----------
    #     elements : list
    #         List with the key numbers of the element to be removed.

    #     Returns
    #     -------
    #     None
    #     """
    #     raise NotImplementedError()

    #     # for element in elements:
    #     #     self.remove_element(element)

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    # # TODO: check the release definition
    # def add_release(self, release):
    #     self.releases.append(release)

    # def add_releases(self, releases):
    #     for release in releases:
    #         self.add_release(release)

    # =========================================================================
    #                           Groups methods
    # =========================================================================

    def add_group(self, group):
        """Add a node or element group to the part.

        Parameters
        ----------
        group : :class:`compas_fea2.model.NodeGroup` | :class:`compas_fea2.model.ElementGroup`

        Returns
        -------
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

        if group in self.groups:
            if config.VERBOSE:
                print("SKIPPED: Group {!r} already in part.".format(group))
            return

        self._groups.add(group)

    def add_groups(self, groups):
        """Add multiple groups to the part.

        Parameters
        ----------
        groups : list[:class:`compas_fea2.model.Group`]

        Returns
        -------
        None

        """
        for group in groups:
            self.add_group(group)
