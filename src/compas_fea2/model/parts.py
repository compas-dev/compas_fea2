from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import sqrt
from compas.geometry import Point, Plane, Frame, Polygon
from compas.geometry import Transformation, Scale
from compas.geometry import normalize_vector
from compas.geometry import distance_point_point_sqrd
from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_on_plane
from compas.utilities import geometric_key
from compas.geometry import Vector
from compas.geometry import sum_vectors

from compas_fea2 import config
from compas_fea2.base import FEAData

from .nodes import Node
from .elements import _Element, _Element2D, _Element1D, _Element3D, BeamElement, HexahedronElement, ShellElement, TetrahedronElement, Face
from .materials import _Material
from .sections import _Section, ShellSection, SolidSection
from .releases import _BeamEndRelease, BeamEndPinRelease
from .groups import NodesGroup, ElementsGroup, FacesGroup
from .ics import InitialStressField

from compas_fea2.utilities._utils import timer

try:
    import compas_assembly
except:
    pass


class _Part(FEAData):
    """
    Note
    ----
    Parts are registered to a :class:`compas_fea2.model.Model`.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    model : :class:`compas_fea2.model.Model`
        The parent model of the part.
    nodes : Set[:class:`compas_fea2.model.Node`]
        The nodes belonging to the part.
    materials : Set[:class:`compas_fea2.model._Material`]
        The materials belonging to the part.
    sections : Set[:class:`compas_fea2.model._Section`]
        The sections belonging to the part.
    elements : Set[:class:`compas_fea2.model._Element`]
        The elements belonging to the part.
    releases : Set[:class:`compas_fea2.model._BeamEndRelease`]
        The releases belonging to the part.
    nodesgroups : Set[:class:`compas_fea2.model.NodesGroup`]
        The groups of nodes belonging to the part.
    elementsgroups : Set[:class:`compas_fea2.model.ElementsGroup`]
        The groups of elements belonging to the part.
    facesgroups : Set[:class:`compas_fea2.model.FacesGroup`]
        The groups of element faces belonging to the part.
    boundary_mesh : :class:`compas.datastructures.Mesh`
        The outer boundary mesh enveloping the DeformablePart.
    """

    def __init__(self, name=None, **kwargs):
        super(_Part, self).__init__(name=name, **kwargs)
        self._nodes = set()
        self._sections = set()
        self._materials = set()
        self._elements = set()
        self._nodesgroups = set()
        self._elementsgroups = set()
        self._facesgroups = set()
        self._gkey_node = {}
        self._boundary_mesh = None
        self._discretized_boundary_mesh = None
        self._results = {}

    @property
    def nodes(self):
        return self._nodes

    @property
    def elements(self):
        return self._elements

    @property
    def sections(self):
        return self._sections

    @property
    def materials(self):
        return self._materials

    @property
    def releases(self):
        return self._releases

    @property
    def nodesgroups(self):
        return self._nodesgroups

    @property
    def elementsgroups(self):
        return self._elementsgroups

    @property
    def facesgroups(self):
        return self._facesgroups

    @property
    def gkey_node(self):
        return self._gkey_node

    @property
    def boundary_mesh(self):
        return self._boundary_mesh

    @property
    def discretized_boundary_mesh(self):
        return self._discretized_boundary_mesh

    @property
    def volume(self):
        self._volume = 0.
        for element in self.elements:
            if element.volume:
                self._volume += element.volume
        return self._volume

    @property
    def model(self):
        return self._registration

    @property
    def results(self):
        return self._results

    @property
    def nodes_count(self):
        return len(self.nodes)-1

    @property
    def elements_count(self):
        return len(self.elements)-1

    @property
    def element_types(self):
        element_types = {}
        for element in self.elements:
            element_types.setdefault(type(element),[]).append(element)
        return element_types


    def __str__(self):
        return """
{}
{}
name : {}

number of elements : {}
number of nodes    : {}
""".format(self.__class__.__name__,
           len(self.__class__.__name__) * '-',
           self.name,
           self.elements_count,
           self.nodes_count)

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    @classmethod
    def from_compas_line(cls, line, element_model='BeamElement', section=None, name=None, **kwargs):
        """Generate a part from a class:`compas.geometry.Line`.

        Parameters
        ----------
        line : class:`compas.geometry.Line`
            The line
        element_model : str, optional
            Implementation model for the element, by default 'BeamElement'
        section : :class:`compas_fea2.model.BeamSection`, optional
            _description_, by default None
        name : str, optional
            The name of the part, by default None (one is automatically generated)

        Returns
        -------
        class:`compas_fea2.model.Part`
            The part.
        """
        import compas_fea2
        prt = cls(name=name)
        element = getattr(compas_fea2.model, element_model)(nodes=[Node(line.start), Node(line.end)], section=section)
        if not isinstance(element, _Element1D):
            raise ValueError("Provide a 1D element")
        prt.add_element(element)
        return prt

    @classmethod
    @timer(message='compas Mesh successfully imported in ')
    def shell_from_compas_mesh(cls, mesh, section, name=None, **kwargs):
        """Creates a DeformablePart object from a :class:`compas.datastructures.Mesh`.
        To each face of the mesh is assigned a :class:`compas_fea2.model.ShellElement`
        objects. Currently, the same section is applied to all the elements.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            Mesh to convert to a DeformablePart.
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

        part.boundary_mesh = mesh
        part.discretized_boundary_mesh = mesh

        return part

    @classmethod
    # @timer(message='part successfully imported from gmsh model in ')
    def from_gmsh(cls, gmshModel, name=None, **kwargs):
        """Create a Part object from a gmshModel object. According to the
        `section` type provided, :class:`compas_fea2.model._Element2D` or
        :class:`compas_fea2.model._Element3D` elements are cretated.
        The same section is applied to all the elements.

        Note
        ----
        The gmshModel must have the right dimension corresponding to the section
        provided.

        Warning
        -------
        the `split` option is currently not implemented

        Parameters
        ----------
        name : str
            Name of the new part.
        gmshModel : obj
            gmsh Model to convert. See [1]_
        section : obj
            `compas_fea2` :class:`SolidSection` or :class:`ShellSection` sub-class
            object to to apply to the elements.
        split : bool, optional
            If ``True`` create an additional node in the middle of the edges of the
            elements to implement more refined element types. Check for example [2]_.
        verbose : bool, optional
            If ``True`` print a log, by default False
        check : bool, optional
            If ``True`` performs sanity checks, by default False. This is a quite
            resource-intense operation! Set to ``False`` for large models (>10000
            nodes).

        Returns
        -------
        :class:`compas_fea2.model._Part`
            The part meshed.

        References
        ----------
        .. [1] https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_9_1/api/gmsh.py
        .. [2] https://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node33.html

        Examples
        --------
        >>> gmshModel = gmsh.mode.generate(3)
        >>> mat = ElasticIsotropic(name='mat', E=29000, v=0.17, density=2.5e-9)
        >>> sec = SolidSection('mysec', mat)
        >>> part = DeformablePart.from_gmsh('part_gmsh', gmshModel, sec)

        """
        import numpy as np

        part = cls(name=name)
        # add nodes
        gmsh_nodes = gmshModel.mesh.get_nodes()
        node_coords = gmsh_nodes[1].reshape((-1, 3), order='C')
        fea2_nodes = [part.add_node(Node(coords.tolist())) for coords in node_coords]
        # add elements
        gmsh_elements = gmshModel.mesh.get_elements()

        section = kwargs.get('section', None)
        split = kwargs.get('split', False)
        verbose = kwargs.get('verbose', False)
        rigid = kwargs.get('rigid', False)

        dimension = 2 if isinstance(section, SolidSection) else 1

        ntags_per_element = np.split(gmsh_elements[2][dimension]-1,
                                     len(gmsh_elements[1][dimension]))  # gmsh keys start from 1

        for ntags in ntags_per_element:
            if split:
                raise NotImplementedError('this feature is under development')
            element_nodes = [fea2_nodes[ntag] for ntag in ntags]
            if ntags.size == 3:
                k = part.add_element(ShellElement(nodes=element_nodes,
                                                  section=section,
                                                  rigid=rigid))
            elif ntags.size == 4:
                if isinstance(section, ShellSection):
                    k = part.add_element(ShellElement(nodes=element_nodes,
                                                      section=section,
                                                      rigid=rigid))
                else:
                    k = part.add_element(TetrahedronElement(nodes=element_nodes,
                                                            section=section))
            elif ntags.size == 8:
                k = part.add_element(HexahedronElement(nodes=element_nodes,
                                                       section=section))
            else:
                raise NotImplementedError('Element with {} nodes not supported'.format(ntags.size))
            if verbose:
                print('element {} added'.format(k))

        return part

    @classmethod
    def from_boundary_mesh(cls, boundary_mesh, name=None, **kwargs):
        """Create a Part object from a 3-dimensional :class:`compas.datastructures.Mesh`
        object reppresenting the boundary envelope of the Part. The Part is
        discretized uniformly in Thetrahedra of a given mesh size.
        The same section is applied to all the elements.

        Parameters
        ----------
        name : str, optional
            Name of the new Part.
        boundary_mesh : :class:`compas.datastructures.Mesh`
            Boundary envelope of the DeformablePart.

        Returns
        -------
        :class:`compas_fea2.model.Part`
            The part.

        """
        from compas_gmsh.models import MeshModel
        target_mesh_size = kwargs.get('target_mesh_size', 1)
        mesh_size_at_vertices = kwargs.get('mesh_size_at_vertices', None)
        target_point_mesh_size = kwargs.get('target_point_mesh_size', None)
        meshsize_max = kwargs.get('meshsize_max', None)
        meshsize_min = kwargs.get('meshsize_min', None)

        gmshModel = MeshModel.from_mesh(boundary_mesh, targetlength=target_mesh_size)

        if mesh_size_at_vertices:
            for vertex, target in mesh_size_at_vertices.items():
                gmshModel.mesh_targetlength_at_vertex(vertex, target)

        if target_point_mesh_size:
            gmshModel.heal()
            for point, target in target_point_mesh_size.items():
                tag = gmshModel.model.occ.addPoint(*point, target)
                gmshModel.model.occ.mesh.set_size([(0, tag)], target)

        if meshsize_max:
            gmshModel.options.mesh.meshsize_max = meshsize_max
        if meshsize_min:
            gmshModel.options.mesh.meshsize_min = meshsize_min

        gmshModel.heal()
        gmshModel.generate_mesh(3)

        part = cls.from_gmsh(gmshModel=gmshModel.model, name=name, **kwargs)
        part._boundary_mesh = boundary_mesh

        gmshModel.generate_mesh(2)
        part._discretized_boundary_mesh = gmshModel.mesh_to_compas()

        del(gmshModel)

        if kwargs.get('rigid', False):
            point = boundary_mesh.centroid()
            part.reference_point = Node(xyz=[point.x, point.y, point.z])

        centroid_face = {}
        for face in part._discretized_boundary_mesh.faces():
            centroid_face[geometric_key(part._discretized_boundary_mesh.face_centroid(face))] = face
        part._discretized_boundary_mesh.centroid_face = centroid_face

        return part

    # =========================================================================
    #                           Nodes methods
    # =========================================================================
    def find_node_by_key(self, key):
        # type: (int) -> Node
        """Retrieve a node in the model using its key.

        Parameters
        ----------
        key : int
            The node's key.

        Returns
        -------
        :class:`compas_fea2.model.Node`
            The corresponding node.
        """
        for node in self.nodes:
            if node.key == key:
                return node

    def find_nodes_by_name(self, name):
        # type: (str) -> list(Node)
        """Find all nodes with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        return [node for node in self.nodes if node.name == name]

    def find_nodes_by_location(self, point, distance, plane=None, report=False, **kwargs):
        # type: (Point, float, Plane, bool, bool) -> list(Node)
        """Find all nodes within a distance of a given geometrical location.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            A geometrical location.
        distance : float
            Distance from the location.
        plane : :class:`compas.geometry.Plane`, optional
            Limit the search to one plane.
        report : bool, optional
            If True, return a dictionary with the node and its distance to the
            point, otherwise, just the node. By default is False.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        d2 = distance ** 2
        nodes = self.find_nodes_on_plane(plane) if plane else self.nodes
        if report:
            return {node: sqrt(distance) for node in nodes if (distance := distance_point_point_sqrd(node.xyz, point)) < d2}
        else:
            return [node for node in nodes if (distance := distance_point_point_sqrd(node.xyz, point)) < d2]

    def find_closest_nodes_to_point(self, point, distance, number_of_nodes=1, plane=None):
        # type: (Point, float, int, Plane) -> list(Node)
        """Find the n closest nodes within a distance of a given geometrical location.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            A geometrical location.
        distance : float
            Distance from the location.
        numnber_of_nodes : int
            Number of nodes to return.
        plane : :class:`compas.geometry.Plane`, optional
            Limit the search to one plane.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        nodes = self.find_nodes_by_location(point, distance, plane, report=True)
        if number_of_nodes > len(nodes):
            number_of_nodes = len(nodes)
        return [k for k, v in sorted(nodes.items(), key=lambda item: item[1])][:number_of_nodes]

    def find_nodes_around_node(self, node, distance, plane=None):
        # type: (Node, float, Plane) -> list(Node)
        """Find all nodes around a given node (excluding the node itself).

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The given node.
        radius : float
            Search radious.
        plane : :class:`compas.geometry.Plane`, optional
            Limit the search to one plane.

        Returns
        -------
        [:class:`compas_fea2.model.Node]
            The nodes around the given node
        """
        nodes = self.find_nodes_by_location(node.xyz, distance, plane, report=True)
        if node in nodes:
            del nodes[node]
        return nodes

    def find_closest_nodes_to_node(self, node, distance, number_of_nodes=1, plane=None):
        # type: (Point, float, int, Plane) -> list(Node)
        """Find the n closest nodes around a given node (excluding the node itself).

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            A geometrical location.
        distance : float
            Distance from the location.
        numnber_of_nodes : int
            Number of nodes to return.
        plane : :class:`compas.geometry.Plane`, optional
            Limit the search to one plane.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        nodes = self.find_nodes_by_location(node.xyz, distance, plane, report=True)
        if number_of_nodes > len(nodes):
            number_of_nodes = len(nodes)
        return [k for k, v in sorted(nodes.items(), key=lambda item: item[1])][:number_of_nodes]

    def find_nodes_by_attribute(self, attr, value, tolerance=0.001):
        # type: (str, float, float) -> list(Node)
        """Find all nodes with a given value for a the given attribute.

        Note
        ----
        Only numeric attributes are supported.

        Parameters
        ----------
        attr : str
            Attribute name.
        value : any
            Appropriate value for the given attribute.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        return list(filter(lambda x: abs(getattr(x, attr) - value) <= tolerance, self.nodes))

    def find_nodes_on_plane(self, plane):
        # type: (Plane) -> list(Node)
        """Find all nodes on a given plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        return list(filter(lambda x: is_point_on_plane(Point(*x.xyz), plane), self.nodes))

    def find_nodes_in_polygon(self, polygon, tolerance=1.1):
        # type: (Polygon, float) -> list(Node)
        """Find the nodes of the part that are contained within a planar polygon

        Parameters
        ----------
        polygon : :class:`compas.geometry.Polygon`
            The polygon for the search.

        Returns
        -------
        [:class:`compas_fea2.model.Node]
            List with the nodes contained in the polygon.
        """
        # TODO quick fix...change!
        if not hasattr(polygon, 'plane'):
            try:
                polygon.plane = Frame.from_points(*polygon.points[:3])
            except:
                polygon.plane = Frame.from_points(*polygon.points[-3:])

        S = Scale.from_factors([tolerance]*3, polygon.plane)
        T = Transformation.from_frame_to_frame(polygon.plane, Frame.worldXY())
        nodes_on_plane = self.find_nodes_on_plane(Plane.from_frame(polygon.plane))
        polygon_xy = polygon.transformed(S)
        polygon_xy = polygon.transformed(T)
        return list(filter(lambda x: is_point_in_polygon_xy(Point(*x.xyz).transformed(T), polygon_xy), nodes_on_plane))


    # TODO quite slow...check how to make it faster
    def find_nodes_where(self, conditions):
        # type: (list(str)) -> list(Node)
        """Find the nodes where some conditions are met.

        Parameters
        ----------
        conditions : [str]
            List with the strings of the required conditions.

        Returns
        -------
        [Node]
            List with the nodes matching the criteria.
        """
        import re
        nodes = []
        for condition in conditions:
            # limit the serch to the already found nodes
            part_nodes = self.nodes if not nodes else list(set.intersection(*nodes))
            try:
                eval(condition)
            except NameError as ne:
                var_name = re.findall(r"'([^']*)'", str(ne))[0]
                nodes.append(set(filter(lambda n: eval(condition.replace(var_name, str(getattr(n, var_name)))), part_nodes)))
        return list(set.intersection(*nodes))

    def contains_node(self, node):
        # type: (Node) -> Node
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
        # type: (Node) -> Node
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
        >>> part = DeformablePart()
        >>> node = Node(1.0, 2.0, 3.0)
        >>> part.add_node(node)

        """
        if not isinstance(node, Node):
            raise TypeError('{!r} is not a node.'.format(node))

        if self.contains_node(node):
            if config.VERBOSE:
                print('NODE SKIPPED: Node {!r} already in part.'.format(node))
            return

        if not config.POINT_OVERLAP:
            if self.find_nodes_by_location(node.xyz, distance=config.GLOBAL_TOLERANCE):
                if config.VERBOSE:
                    print('NODE SKIPPED: Part {!r} has already a node at {}.'.format(self, node.xyz))
                return

        node._key = len(self._nodes)
        self._nodes.add(node)
        self._gkey_node[node.gkey] = node
        node._registration = self
        if config.VERBOSE:
            print('Node {!r} registered to {!r}.'.format(node, self))
        return node

    def add_nodes(self, nodes):
        # type: (list(Node)) -> list(Node)
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
        >>> part = DeformablePart()
        >>> node1 = Node([1.0, 2.0, 3.0])
        >>> node2 = Node([3.0, 4.0, 5.0])
        >>> node3 = Node([3.0, 4.0, 5.0])
        >>> nodes = part.add_nodes([node1, node2, node3])

        """
        return [self.add_node(node) for node in nodes]

    def is_node_on_boundary(self, node, precision=None):
        # type: (Node, str) -> bool
        """Check if a node is on the boundary mesh of the DeformablePart.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node to evaluate.
        precision : ??
            ???

        Note
        ----
        The `discretized_boundary_mesh` of the part must have been previously
        defined.

        Returns
        -------
        bool
            `True` if the node is on the boundary, `False` otherwise.
        """
        if not self.discretized_boundary_mesh:
            raise AttributeError("The discretized_boundary_mesh has not been defined")
        if not node.on_boundary:
            node._on_boundary = True if geometric_key(
                node.xyz, precision) in self.discretized_boundary_mesh.gkey_vertex() else False
        return node.on_boundary

    # =========================================================================
    #                           Elements methods
    # =========================================================================
    def find_element_by_key(self, key):
        # type: (int) -> _Element
        """Retrieve an element in the model using its key.

        Parameters
        ----------
        key : int
            The element's key.

        Returns
        -------
        :class:`compas_fea2.model._Element`
            The corresponding element.
        """
        for element in self.elements:
            if element.key == key:
                return element

    def find_elements_by_name(self, name):
        # type: (str) -> list(_Element)
        """Find all elements with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        list[:class:`compas_fea2.model._Element`]

        """
        return [element for element in self.elements if element.name == name]

    def contains_element(self, element):
        # type: (_Element) -> _Element
        """Verify that the part contains a specific element.

        Parameters
        ----------
        element : :class:`compas_fea2.model._Element`

        Returns
        -------
        bool

        """
        return element in self.elements

    def add_element(self, element):
        # type: (_Element) -> _Element
        """Add an element to the part.

        Parameters
        ----------
        element : :class:`compas_fea2.model._Element`
            The element instance.

        Returns
        -------
        :class:`compas_fea2.model._Element`

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
        if hasattr(element, 'section'):
            if element.section:
                self.add_section(element.section)

        if hasattr(element.section, 'material'):
            if element.section.material:
                self.add_material(element.section.material)

        element._key = len(self.elements)
        self.elements.add(element)
        element._registration = self
        if config.VERBOSE:
            print('Element {!r} registered to {!r}.'.format(element, self))
        return element

    def add_elements(self, elements):
        # type: (_Element) -> list(_Element)
        """Add multiple elements to the part.

        Parameters
        ----------
        elements : list[:class:`compas_fea2.model._Element`]

        Return
        ------
        list[:class:`compas_fea2.model._Element`]

        """
        return [self.add_element(element) for element in elements]

    def is_element_on_boundary(self, element):
        # type: (_Element) -> bool
        from compas.geometry import centroid_points
        from compas.utilities import geometric_key

        if element.on_boundary is None:
            if not self._discretized_boundary_mesh.centroid_face:
                centroid_face = {}
                for face in self._discretized_boundary_mesh.faces():
                    centroid_face[geometric_key(self._discretized_boundary_mesh.face_centroid(face))] = face
            if isinstance(element, _Element3D):
                if any(geometric_key(centroid_points([node.xyz for node in face.nodes])) in self._discretized_boundary_mesh.centroid_face for face in element.faces):
                    element.on_boundary = True
                else:
                    element.on_boundary = False
            elif isinstance(element, _Element2D):
                if geometric_key(centroid_points([node.xyz for node in element.nodes])) in self._discretized_boundary_mesh.centroid_face:
                    element.on_boundary = True
                else:
                    element.on_boundary = False
        return element.on_boundary

    # =========================================================================
    #                           Faces methods
    # =========================================================================

    def find_faces_on_plane(self, plane):
        # type: (Plane) -> list(Face)
        """Find the face of the elements that belongs to a given plane, if any.

        Note
        ----
        The search is limited to solid elements.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane where the faces should belong.

        Returns
        -------
        [:class:`compas_fea2.model.Face`]
            list with the faces belonging to the given plane.
        """
        faces = []
        for element in filter(lambda x: isinstance(x, (_Element2D, _Element3D)) and self.is_element_on_boundary(x), self._elements):
            for face in element.faces:
                if all([is_point_on_plane(node.xyz, plane) for node in face.nodes]):
                    faces.append(face)
        return faces

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
        if isinstance(group, NodesGroup):
            return group in self._nodesgroups
        elif isinstance(group, ElementsGroup):
            return group in self._elementsgroups
        elif isinstance(group, FacesGroup):
            return group in self._facesgroups
        else:
            raise TypeError('{!r} is not a valid Group'.format(group))

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

        if isinstance(group, NodesGroup):
            self.add_nodes(group.nodes)
        elif isinstance(group, ElementsGroup):
            self.add_elements(group.elements)

        if self.contains_group(group):
            if config.VERBOSE:
                print("SKIPPED: Group {!r} already in part.".format(group))
            return
        if isinstance(group, NodesGroup):
            self._nodesgroups.add(group)
        elif isinstance(group, ElementsGroup):
            self._elementsgroups.add(group)
        elif isinstance(group, FacesGroup):
            self._facesgroups.add(group)
        else:
            raise TypeError("{!r} is not a valid group.".format(group))
        group._registration = self  # BUG wrong because the memebers of the group might have a different registation
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

    # ==============================================================================
    # Results methods
    # ==============================================================================

    def sorted_nodes_by_displacement(self, problem, step=None, component='length'):
        """Return a list with the nodes sorted by their displacement

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            The problem
        step : :class:`compas_fea2.problem._Step`, optional
            The step, by default None. If not provided, the last step of the
            problem is used.
        component : str, optional
            one of ['x', 'y', 'z', 'length'], by default 'length'.

        Returns
        -------
        [:class:`compas_fea2.model.Node`]
            The node sorted by displacment (ascending).
        """
        step = step or problem._steps_order[-1]
        return sorted(self.nodes, key=lambda n: getattr(Vector(*n.results[problem][step].get('U', None)), component))

    def get_max_displacement(self, problem, step=None, component='length'):
        """Retrieve the node with the maximum displacement

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            The problem
        step : :class:`compas_fea2.problem._Step`, optional
            The step, by default None. If not provided, the last step of the
            problem is used.
        component : str, optional
            one of ['x', 'y', 'z', 'length'], by default 'length'.

        Returns
        -------
        :class:`compas_fea2.model.Node`, float
            The node and the displacement
        """
        step = step or problem._steps_order[-1]
        node = self.sorted_nodes_by_displacement(problem=problem, step=step, component=component)[-1]
        displacement = getattr(Vector(*node.results[problem][step].get('U', None)), component)
        return node, displacement

    def get_min_displacement(self, problem, step=None, component='length'):
        """Retrieve the node with the minimum displacement

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            The problem
        step : :class:`compas_fea2.problem._Step`, optional
            The step, by default None. If not provided, the last step of the
            problem is used.
        component : str, optional
            one of ['x', 'y', 'z', 'length'], by default 'length'.

        Returns
        -------
        :class:`compas_fea2.model.Node`, float
            The node and the displacement
        """
        step = step or problem._steps_order[-1]
        node = self.sorted_nodes_by_displacement(problem=problem, step=step, component=component)[0]
        displacement = getattr(Vector(*node.results[problem][step].get('U', None)), component)
        return node, displacement

    def get_average_displacement_at_point(self, problem, point, distance, step=None, component='length', project=False):
        """Compute the average displacement around a point

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            The problem
        step : :class:`compas_fea2.problem._Step`, optional
            The step, by default None. If not provided, the last step of the
            problem is used.
        component : str, optional
            one of ['x', 'y', 'z', 'length'], by default 'length'.

        Returns
        -------
        :class:`compas_fea2.model.Node`, float
            The node and the displacement
        """
        step = step or problem._steps_order[-1]
        nodes = self.find_nodes_by_location(point=point, distance=distance, report=True)
        if nodes:
            displacements = [getattr(Vector(*node.results[problem][step].get('U', None)), component) for node in nodes]
            return point, sum(displacements)/len(displacements)


class DeformablePart(_Part):
    """Deformable part.
    """
    __doc__ += _Part.__doc__
    __doc__ += """
    Additional Attributes
    ---------------------
    materials : Set[:class:`compas_fea2.model._Material`]
        The materials belonging to the part.
    sections : Set[:class:`compas_fea2.model._Section`]
        The sections belonging to the part.
    releases : Set[:class:`compas_fea2.model._BeamEndRelease`]
        The releases belonging to the part.
    """

    def __init__(self, name=None, **kwargs):
        super(DeformablePart, self).__init__(name=name, **kwargs)
        self._materials = set()
        self._sections = set()
        self._releases = set()

    @ property
    def materials(self):
        return self._materials

    @ property
    def sections(self):
        return self._sections

    @ property
    def releases(self):
        return self._releases

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    @ classmethod
    @ timer(message='compas Mesh successfully imported in ')
    def frame_from_compas_mesh(cls, mesh, section, name=None, **kwargs):
        """Creates a DeformablePart object from a a :class:`compas.datastructures.Mesh`.
        To each edge of the mesh is assigned a :class:`compas_fea2.model.BeamElement`.
        Currently, the same section is applied to all the elements.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            Mesh to convert to a DeformablePart.
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

        part._boundary_mesh = mesh
        part._discretized_boundary_mesh = mesh

        return part

    @ classmethod
    # @timer(message='part successfully imported from gmsh model in ')
    def from_gmsh(cls, gmshModel, section, name=None, **kwargs):
        """
        """
        return super().from_gmsh(gmshModel, name=name, section=section, **kwargs)

    @ classmethod
    def from_boundary_mesh(cls, boundary_mesh, section, name=None, **kwargs):
        """
        """
        return super().from_boundary_mesh(boundary_mesh, section=section, name=name, **kwargs)

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def find_materials_by_name(self, name):
        # type: (str) -> list(_Material)
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
        # type: (_Material) -> _Material
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
        # type: (_Material) -> _Material
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

        material._key = len(self._materials)
        self._materials.add(material)
        material._registration = self._registration
        return material

    def add_materials(self, materials):
        # type: (_Material) -> list(_Material)
        """Add multiple materials to the part.

        Parameters
        ----------
        materials : list[:class:`compas_fea2.model.Material`]

        Returns
        -------
        None

        """
        return [self.add_material(material) for material in materials]

    # =========================================================================
    #                        Sections methods
    # =========================================================================

    def find_sections_by_name(self, name):
        # type: (str) -> list(_Section)
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
        # type: (_Section) -> _Section
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
        # type: (_Section) -> _Section
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
        section._key = len(self.sections)
        self._sections.add(section)
        section._registration = self._registration
        return section

    def add_sections(self, sections):
        # type: (list(_Section)) -> _Section
        """Add multiple sections to the part.

        Parameters
        ----------
        sections : list[:class:`compas_fea2.model.Section`]

        Returns
        -------
        None

        """
        return [self.add_section(section) for section in sections]

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    def add_beam_release(self, element, location, release):
        """Add a :class:`compas_fea2.model._BeamEndRelease` to an element in the
        part.

        Parameters
        ----------
        element : :class:`compas_fea2.model.BeamElement`
            The element to release.
        location : str
            'start' or 'end'.
        release : :class:`compas_fea2.model._BeamEndRelease`
            Release type to apply.
        """
        if not isinstance(release, _BeamEndRelease):
            raise TypeError('{!r} is not a beam release element.'.format(release))
        release.element = element
        release.location = location
        self._releases.add(release)
        return release


class RigidPart(_Part):
    """Rigid part.
    """
    __doc__ += _Part.__doc__
    __doc__ += """
    Addtional Attributes
    --------------------
    reference_point : :class:`compas_fea2.model.Node`
        A node acting as a reference point for the part, by default `None`. This
        is required if the part is rigid as it controls its movement in space.
    """

    def __init__(self, reference_point=None, name=None, **kwargs):
        super(RigidPart, self).__init__(name=name, **kwargs)
        self._reference_point = reference_point

    @ property
    def reference_point(self):
        return self._reference_point

    @ reference_point.setter
    def reference_point(self, value):
        self._reference_point = self.add_node(value)
        value._is_reference = True

    @ classmethod
    # @timer(message='part successfully imported from gmsh model in ')
    def from_gmsh(cls, gmshModel, name=None, **kwargs):
        """
        """
        kwargs['rigid'] = True
        return super().from_gmsh(gmshModel, name=name, **kwargs)

    @ classmethod
    def from_boundary_mesh(cls, boundary_mesh, name=None, **kwargs):
        """
        """
        kwargs['rigid'] = True
        return super().from_boundary_mesh(boundary_mesh, name=name, **kwargs)
    # =========================================================================
    #                        Elements methods
    # =========================================================================
    # TODO this can be removed and the checks on the rigid part can be done in _part

    def add_element(self, element):
        # type: (_Element) -> _Element
        """Add an element to the part.

        Parameters
        ----------
        element : :class:`compas_fea2.model._Element`
            The element instance.

        Returns
        -------
        :class:`compas_fea2.model._Element`

        Raises
        ------
        TypeError
            If the element is not an element.

        """
        if not hasattr(element, 'rigid'):
            raise TypeError('The element type cannot be assigned to a RigidPart')
        if not getattr(element, 'rigid'):
            raise TypeError('Rigid parts can only have rigid elements')
        return super().add_element(element)
