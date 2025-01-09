from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import sqrt
from math import pi
from typing import Iterable

from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Transformation
from compas.geometry import Vector
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from compas.geometry import distance_point_point_sqrd
from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_on_plane
from compas.tolerance import TOL

import compas_fea2
from compas_fea2.base import FEAData

from .elements import BeamElement
from .elements import HexahedronElement
from .elements import ShellElement
from .elements import TetrahedronElement
from .elements import _Element
from .elements import _Element1D
from .elements import _Element2D
from .elements import _Element3D
from .groups import ElementsGroup
from .groups import FacesGroup
from .groups import NodesGroup
from .materials.material import _Material
from .nodes import Node
from .releases import _BeamEndRelease
from .sections import ShellSection
from .sections import SolidSection
from .sections import _Section


class _Part(FEAData):
    """Base class for Parts.

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
    nodes_count : int
        Number of nodes in the part.
    gkey_node : {gkey : :class:`compas_fea2.model.Node`}
        Dictionary that associates each node and its geometric key}
    materials : Set[:class:`compas_fea2.model._Material`]
        The materials belonging to the part.
    sections : Set[:class:`compas_fea2.model._Section`]
        The sections belonging to the part.
    elements : Set[:class:`compas_fea2.model._Element`]
        The elements belonging to the part.
    element_types : {:class:`compas_fea2.model._Element` : [:class:`compas_fea2.model._Element`]]
        Dictionary with the elements of the part for each element type.
    element_count : int
        Number of elements in the part
    nodesgroups : Set[:class:`compas_fea2.model.NodesGroup`]
        The groups of nodes belonging to the part.
    elementsgroups : Set[:class:`compas_fea2.model.ElementsGroup`]
        The groups of elements belonging to the part.
    facesgroups : Set[:class:`compas_fea2.model.FacesGroup`]
        The groups of element faces belonging to the part.
    boundary_mesh : :class:`compas.datastructures.Mesh`
        The outer boundary mesh enveloping the Part.
    discretized_boundary_mesh : :class:`compas.datastructures.Mesh`
        The discretized outer boundary mesh enveloping the Part.

    Notes
    -----
    Parts are registered to a :class:`compas_fea2.model.Model`.

    """

    def __init__(self, **kwargs):
        super(_Part, self).__init__(**kwargs)
        self._nodes = set()
        self._gkey_node = {}
        self._sections = set()
        self._materials = set()
        self._elements = set()
        self._releases = set()

        self._nodesgroups = set()
        self._elementsgroups = set()
        self._facesgroups = set()

        self._boundary_mesh = None
        self._discretized_boundary_mesh = None
        self._bounding_box = None

        self._volume = None
        self._weight = None

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
    def bounding_box(self):
        try:
            return Box.from_bounding_box(bounding_box([n.xyz for n in self.nodes]))
        except Exception:
            print("WARNING: BoundingBox not generated")
            return None

    @property
    def center(self):
        return centroid_points(self.bounding_box.points)

    @property
    def bottom_plane(self):
        return Plane.from_three_points(*[self.bounding_box.points[i] for i in self.bounding_box.bottom[:3]])

    @property
    def top_plane(self):
        return Plane.from_three_points(*[self.bounding_box.points[i] for i in self.bounding_box.top[:3]])

    @property
    def volume(self):
        self._volume = 0.0
        for element in self.elements:
            if element.volume:
                self._volume += element.volume
        return self._volume

    @property
    def weight(self):
        self._weight = 0.0
        for element in self.elements:
            if element.weight:
                self._weight += element.weight
        return self._weight

    @property
    def model(self):
        return self._registration

    @property
    def results(self):
        return self._results

    @property
    def nodes_count(self):
        return len(self.nodes) - 1

    @property
    def elements_count(self):
        return len(self.elements) - 1

    @property
    def element_types(self):
        element_types = {}
        for element in self.elements:
            element_types.setdefault(type(element), []).append(element)
        return element_types

    def elements_by_dimension(self, dimension=1):
        if dimension == 1:
            return filter(lambda x: isinstance(x, _Element1D), self.elements)
        elif dimension == 2:
            return filter(lambda x: isinstance(x, _Element2D), self.elements)
        elif dimension == 3:
            return filter(lambda x: isinstance(x, _Element3D), self.elements)
        else:
            raise ValueError("dimension not supported")

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    @classmethod
    def from_compas_lines(cls, lines, element_model="BeamElement", xaxis=[0, 1, 0], section=None, name=None, **kwargs):
        """Generate a part from a list of :class:`compas.geometry.Line`.

        Parameters
        ----------
        lines : list[:class:`compas.geometry.Line`]
            The lines to be converted.
        element_model : str, optional
            Implementation model for the element, by default 'BeamElement'.
        xaxis : list[float], optional
            The x-axis direction, by default [0,1,0].
        section : :class:`compas_fea2.model.BeamSection`, optional
            The section to be assigned to the elements, by default None.
        name : str, optional
            The name of the part, by default None (one is automatically generated).

        Returns
        -------
        :class:`compas_fea2.model.Part`
            The part.

        """
        import compas_fea2

        prt = cls(name=name)
        # nodes = [Node(n) for n in set([list(p) for l in lines for p in list(l)])]
        mass = kwargs.get("mass", None)
        for line in lines:
            frame = Frame(line[0], xaxis, line.vector)
            # FIXME change tolerance
            nodes = [prt.find_nodes_around_point(list(p), 1, single=True) or Node(list(p), mass=mass) for p in list(line)]
            prt.add_nodes(nodes)
            element = getattr(compas_fea2.model, element_model)(nodes=nodes, section=section, frame=frame)
            if not isinstance(element, _Element1D):
                raise ValueError("Provide a 1D element")
            prt.add_element(element)
        return prt

    @classmethod
    def shell_from_compas_mesh(cls, mesh, section, name=None, **kwargs):
        """Creates a DeformablePart object from a :class:`compas.datastructures.Mesh`.

        To each face of the mesh is assigned a :class:`compas_fea2.model.ShellElement`
        object. Currently, the same section is applied to all the elements.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            Mesh to convert to a DeformablePart.
        section : :class:`compas_fea2.model.ShellSection`
            Shell section assigned to each face.
        name : str, optional
            Name of the new part. If ``None``, a unique identifier is assigned
            automatically.

        Returns
        -------
        :class:`compas_fea2.model.Part`
            The part.

        """
        implementation = kwargs.get("implementation", None)
        ndm = kwargs.get("ndm", None)
        part = cls(name=name, ndm=ndm) if ndm else cls(name=name)
        vertex_node = {vertex: part.add_node(Node(mesh.vertex_coordinates(vertex))) for vertex in mesh.vertices()}

        for face in mesh.faces():
            nodes = [vertex_node[vertex] for vertex in mesh.face_vertices(face)]
            element = ShellElement(nodes=nodes, section=section, implementation=implementation)
            part.add_element(element)

        part._boundary_mesh = mesh
        part._discretized_boundary_mesh = mesh

        return part

    @classmethod
    def from_gmsh(cls, gmshModel, section=None, name=None, **kwargs):
        """Create a Part object from a gmshModel object.

        According to the `section` type provided, :class:`compas_fea2.model._Element2D` or
        :class:`compas_fea2.model._Element3D` elements are created.
        The same section is applied to all the elements.

        Parameters
        ----------
        gmshModel : obj
            gmsh Model to convert. See [1]_.
        section : obj
            `compas_fea2` :class:`SolidSection` or :class:`ShellSection` sub-class
            object to apply to the elements.
        name : str, optional
            Name of the new part.
        split : bool, optional
            If ``True`` create an additional node in the middle of the edges of the
            elements to implement more refined element types. Check for example [2]_.
        verbose : bool, optional
            If ``True`` print a log, by default False.
        check : bool, optional
            If ``True`` performs sanity checks, by default False. This is a quite
            resource-intense operation! Set to ``False`` for large models (>10000
            nodes).

        Returns
        -------
        :class:`compas_fea2.model.Part`
            The part meshed.

        Notes
        -----
        The gmshModel must have the right dimension corresponding to the section provided.

        References
        ----------
        .. [1] https://gitlab.onelab.info/gmsh/gmsh/blob/gmsh_4_9_1/api/gmsh.py
        .. [2] https://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node33.html

        Examples
        --------
        >>> mat = ElasticIsotropic(name="mat", E=29000, v=0.17, density=2.5e-9)
        >>> sec = SolidSection("mysec", mat)
        >>> part = DeformablePart.from_gmsh("part_gmsh", gmshModel, sec)

        """
        import numpy as np

        part = cls(name=name)

        gmshModel.heal()
        gmshModel.generate_mesh(3)
        model = gmshModel.model

        # add nodes
        node_coords = model.mesh.get_nodes()[1].reshape((-1, 3), order="C")
        fea2_nodes = np.array([part.add_node(Node(coords)) for coords in node_coords])

        # add elements
        gmsh_elements = model.mesh.get_elements()
        dimension = 2 if isinstance(section, SolidSection) else 1
        ntags_per_element = np.split(gmsh_elements[2][dimension] - 1, len(gmsh_elements[1][dimension]))  # gmsh keys start from 1

        verbose = kwargs.get("verbose", False)
        rigid = kwargs.get("rigid", False)
        implementation = kwargs.get("implementation", None)

        for ntags in ntags_per_element:
            if kwargs.get("split", False):
                raise NotImplementedError("this feature is under development")
            # element_nodes = [fea2_nodes[ntag] for ntag in ntags]
            element_nodes = fea2_nodes[ntags]

            if ntags.size == 3:
                k = part.add_element(ShellElement(nodes=element_nodes, section=section, rigid=rigid, implementation=implementation))
            elif ntags.size == 4:
                if isinstance(section, ShellSection):
                    k = part.add_element(ShellElement(nodes=element_nodes, section=section, rigid=rigid, implementation=implementation))
                else:
                    k = part.add_element(TetrahedronElement(nodes=element_nodes, section=section))
                    part.ndf = 3  # FIXME try to move outside the loop
            elif ntags.size == 8:
                k = part.add_element(HexahedronElement(nodes=element_nodes, section=section))
            else:
                raise NotImplementedError("Element with {} nodes not supported".format(ntags.size))
            if verbose:
                print("element {} added".format(k))

        if not part._boundary_mesh:
            gmshModel.generate_mesh(2)  # FIXME Get the volumes without the mesh
            part._boundary_mesh = gmshModel.mesh_to_compas()

        if not part._discretized_boundary_mesh:
            # gmshModel.generate_mesh(2)
            part._discretized_boundary_mesh = part._boundary_mesh

        if rigid:
            point = part._discretized_boundary_mesh.centroid()
            part.reference_point = Node(xyz=[point.x, point.y, point.z])

        # FIXME get the planes on each face of the part and compute the centroid -> move to Part
        # centroid_face = {}
        # for face in part._discretized_boundary_mesh.faces():
        #     centroid_face[geometric_key(part._discretized_boundary_mesh.face_centroid(face))] = face
        # part._discretized_boundary_mesh.centroid_face = centroid_face

        return part

    @classmethod
    def from_boundary_mesh(cls, boundary_mesh, name=None, **kwargs):
        """Create a Part object from a 3-dimensional :class:`compas.datastructures.Mesh`
        object representing the boundary envelope of the Part. The Part is
        discretized uniformly in Tetrahedra of a given mesh size.
        The same section is applied to all the elements.

        Parameters
        ----------
        boundary_mesh : :class:`compas.datastructures.Mesh`
            Boundary envelope of the DeformablePart.
        name : str, optional
            Name of the new Part.
        target_mesh_size : float, optional
            Target mesh size for the discretization, by default 1.
        mesh_size_at_vertices : dict, optional
            Dictionary of vertex keys and target mesh sizes, by default None.
        target_point_mesh_size : dict, optional
            Dictionary of point coordinates and target mesh sizes, by default None.
        meshsize_max : float, optional
            Maximum mesh size, by default None.
        meshsize_min : float, optional
            Minimum mesh size, by default None.

        Returns
        -------
        :class:`compas_fea2.model.Part`
            The part.

        """
        from compas_gmsh.models import MeshModel

        target_mesh_size = kwargs.get("target_mesh_size", 1)
        mesh_size_at_vertices = kwargs.get("mesh_size_at_vertices", None)
        target_point_mesh_size = kwargs.get("target_point_mesh_size", None)
        meshsize_max = kwargs.get("meshsize_max", None)
        meshsize_min = kwargs.get("meshsize_min", None)

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

        part = cls.from_gmsh(gmshModel=gmshModel, name=name, **kwargs)

        del gmshModel

        return part

    @classmethod
    def from_step_file(cls, step_file, name=None, **kwargs):
        """Create a Part object from a STEP file.

        Parameters
        ----------
        step_file : str
            Path to the STEP file.
        name : str, optional
            Name of the new Part.
        mesh_size_at_vertices : dict, optional
            Dictionary of vertex keys and target mesh sizes, by default None.
        target_point_mesh_size : dict, optional
            Dictionary of point coordinates and target mesh sizes, by default None.
        meshsize_max : float, optional
            Maximum mesh size, by default None.
        meshsize_min : float, optional
            Minimum mesh size, by default None.

        Returns
        -------
        :class:`compas_fea2.model.Part`
            The part.

        """
        from compas_gmsh.models import MeshModel

        mesh_size_at_vertices = kwargs.get("mesh_size_at_vertices", None)
        target_point_mesh_size = kwargs.get("target_point_mesh_size", None)
        meshsize_max = kwargs.get("meshsize_max", None)
        meshsize_min = kwargs.get("meshsize_min", None)

        print("Creating the part from the step file...")
        gmshModel = MeshModel.from_step(step_file)

        if mesh_size_at_vertices:
            for vertex, target in mesh_size_at_vertices.items():
                gmshModel.mesh_targetlength_at_vertex(vertex, target)

        if target_point_mesh_size:
            gmshModel.heal()
            for point, target in target_point_mesh_size.items():
                tag = gmshModel.model.occ.addPoint(*point, target)
                gmshModel.model.occ.mesh.set_size([(0, tag)], target)

        if meshsize_max:
            gmshModel.heal()
            gmshModel.options.mesh.meshsize_max = meshsize_max
        if meshsize_min:
            gmshModel.heal()
            gmshModel.options.mesh.meshsize_min = meshsize_min

        part = cls.from_gmsh(gmshModel=gmshModel, name=name, **kwargs)

        del gmshModel

        return part

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    def find_node_by_key(self, key):
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

    def find_node_by_inputkey(self, input_key):
        """Retrieve a node in the model using its key.

        Parameters
        ----------
        input_key : int
            The node's inputkey.

        Returns
        -------
        :class:`compas_fea2.model.Node`
            The corresponding node.

        """
        for node in self.nodes:
            if node.input_key == input_key:
                return node

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

    def find_nodes_around_point(self, point, distance, plane=None, report=False, single=False, **kwargs):
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
        single : bool, optional
            If True, return only the closest node, by default False.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        d2 = distance**2
        nodes = self.find_nodes_on_plane(plane) if plane else self.nodes
        if report:
            return {node: sqrt(distance) for node in nodes if distance_point_point_sqrd(node.xyz, point) < d2}
        nodes = [node for node in nodes if distance_point_point_sqrd(node.xyz, point) < d2]
        if len(nodes) == 0:
            if compas_fea2.VERBOSE:
                print(f"No nodes found at {point}")
            return
        if single:
            return nodes[0]
        else:
            return nodes

    # def find_closest_nodes_to_point(self, point, distance, number_of_nodes=1, plane=None):
    #     """Find the n closest nodes within a distance of a given geometrical location.

    #     Parameters
    #     ----------
    #     point : :class:`compas.geometry.Point`
    #         A geometrical location.
    #     distance : float
    #         Distance from the location.
    #     number_of_nodes : int
    #         Number of nodes to return.
    #     plane : :class:`compas.geometry.Plane`, optional
    #         Limit the search to one plane.

    #     Returns
    #     -------
    #     list[:class:`compas_fea2.model.Node`]

    #     """
    #     nodes = self.find_nodes_around_point(point, distance, plane, report=True)
    #     if number_of_nodes > len(nodes):
    #         number_of_nodes = len(nodes)
    #     return [k for k, v in sorted(nodes.items(), key=lambda item: item[1])][:number_of_nodes]

    def find_nodes_around_node(self, node, distance, plane=None, report=False, single=False):
        """Find all nodes around a given node (excluding the node itself).

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The given node.
        distance : float
            Search radius.
        plane : :class:`compas.geometry.Plane`, optional
            Limit the search to one plane.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        nodes = self.find_nodes_around_point(node.xyz, distance, plane, report=report, single=single)
        if nodes and isinstance(nodes, Iterable):
            if node in nodes:
                del nodes[node]
        return nodes

    def find_closest_nodes_to_node(self, node, distance, number_of_nodes=1, plane=None):
        """Find the n closest nodes around a given node (excluding the node itself).

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The given node.
        distance : float
            Distance from the location.
        number_of_nodes : int
            Number of nodes to return.
        plane : :class:`compas.geometry.Plane`, optional
            Limit the search to one plane.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        nodes = self.find_nodes_around_point(node.xyz, distance, plane, report=True)
        if number_of_nodes > len(nodes):
            number_of_nodes = len(nodes)
        return [k for k, v in sorted(nodes.items(), key=lambda item: item[1])][:number_of_nodes]

    def find_nodes_by_attribute(self, attr, value, tolerance=0.001):
        """Find all nodes with a given value for the given attribute.

        Parameters
        ----------
        attr : str
            Attribute name.
        value : any
            Appropriate value for the given attribute.
        tolerance : float, optional
            Tolerance for numeric attributes, by default 0.001.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        Notes
        -----
        Only numeric attributes are supported.

        """
        return list(filter(lambda x: abs(getattr(x, attr) - value) <= tolerance, self.nodes))

    def find_nodes_on_plane(self, plane, tolerance=1):
        """Find all nodes on a given plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane.
        tolerance : float, optional
            Tolerance for the search, by default 1.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        return list(filter(lambda x: is_point_on_plane(Point(*x.xyz), plane, tolerance), self.nodes))

    def find_nodes_in_polygon(self, polygon, tolerance=1.1):
        """Find the nodes of the part that are contained within a planar polygon.

        Parameters
        ----------
        polygon : :class:`compas.geometry.Polygon`
            The polygon for the search.
        tolerance : float, optional
            Tolerance for the search, by default 1.1.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        """
        # TODO quick fix...change!
        if not hasattr(polygon, "plane"):
            try:
                polygon.plane = Frame.from_points(*polygon.points[:3])
            except Exception:
                polygon.plane = Frame.from_points(*polygon.points[-3:])

        S = Scale.from_factors([tolerance] * 3, polygon.frame)
        T = Transformation.from_frame_to_frame(Frame.from_plane(polygon.plane), Frame.worldXY())
        nodes_on_plane = self.find_nodes_on_plane(Plane.from_frame(polygon.plane))
        polygon_xy = polygon.transformed(S)
        polygon_xy = polygon.transformed(T)
        return list(filter(lambda x: is_point_in_polygon_xy(Point(*x.xyz).transformed(T), polygon_xy), nodes_on_plane))

    # TODO quite slow...check how to make it faster
    def find_nodes_where(self, conditions):
        """Find the nodes where some conditions are met.

        Parameters
        ----------
        conditions : list[str]
            List with the strings of the required conditions.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

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
        """Verify that the part contains a given node.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node to check.

        Returns
        -------
        bool

        """
        return node in self.nodes

    def add_node(self, node):
        """Add a node to the part.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node.

        Returns
        -------
        :class:`compas_fea2.model.Node`
            The identifier of the node in the part.

        Raises
        ------
        TypeError
            If the node is not a node.

        Notes
        -----
        By adding a Node to the part, it gets registered to the part.

        Examples
        --------
        >>> part = DeformablePart()
        >>> node = Node(xyz=(1.0, 2.0, 3.0))
        >>> part.add_node(node)

        """
        if not isinstance(node, Node):
            raise TypeError("{!r} is not a node.".format(node))

        if self.contains_node(node):
            if compas_fea2.VERBOSE:
                print("NODE SKIPPED: Node {!r} already in part.".format(node))
            return

        if not compas_fea2.POINT_OVERLAP:
            existing_node = self.find_nodes_around_point(node.xyz, distance=compas_fea2.GLOBAL_TOLERANCE)
            if existing_node:
                if compas_fea2.VERBOSE:
                    print("NODE SKIPPED: Part {!r} has already a node at {}.".format(self, node.xyz))
                return existing_node[0]

        node._key = len(self._nodes)
        self._nodes.add(node)
        self._gkey_node[node.gkey] = node
        node._registration = self
        if compas_fea2.VERBOSE:
            print("Node {!r} registered to {!r}.".format(node, self))
        return node

    def add_nodes(self, nodes):
        """Add multiple nodes to the part.

        Parameters
        ----------
        nodes : list[:class:`compas_fea2.model.Node`]
            The list of nodes.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]

        Examples
        --------
        >>> part = DeformablePart()
        >>> node1 = Node([1.0, 2.0, 3.0])
        >>> node2 = Node([3.0, 4.0, 5.0])
        >>> node3 = Node([3.0, 4.0, 5.0])
        >>> nodes = part.add_nodes([node1, node2, node3])

        """
        return [self.add_node(node) for node in nodes]

    def remove_node(self, node):
        """Remove a :class:`compas_fea2.model.Node` from the part.

        Warnings
        --------
        Removing nodes can cause inconsistencies.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node to remove.

        """
        # type: (Node) -> None
        if self.contains_node(node):
            self.nodes.remove(node)
            self._gkey_node.pop(node.gkey)
            node._registration = None
            if compas_fea2.VERBOSE:
                print("Node {!r} removed from {!r}.".format(node, self))

    def remove_nodes(self, nodes):
        """Remove multiple :class:`compas_fea2.model.Node` from the part.

        Warnings
        --------
        Removing nodes can cause inconsistencies.

        Parameters
        ----------
        nodes : list[:class:`compas_fea2.model.Node`]
            List with the nodes to remove.

        """
        for node in nodes:
            self.remove_node(node)

    def is_node_on_boundary(self, node, precision=None):
        """Check if a node is on the boundary mesh of the DeformablePart.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node to evaluate.
        precision : float, optional
            Precision for the geometric key comparison, by default None.

        Returns
        -------
        bool
            `True` if the node is on the boundary, `False` otherwise.

        Notes
        -----
        The `discretized_boundary_mesh` of the part must have been previously defined.

        """
        if not self.discretized_boundary_mesh:
            raise AttributeError("The discretized_boundary_mesh has not been defined")
        if not node.on_boundary:
            node._on_boundary = True if TOL.geometric_key(node.xyz, precision) in self.discretized_boundary_mesh.gkey_vertex() else False
        return node.on_boundary

    # =========================================================================
    #                           Elements methods
    # =========================================================================
    def find_element_by_key(self, key):
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
            raise TypeError("{!r} is not an element.".format(element))

        if self.contains_element(element):
            if compas_fea2.VERBOSE:
                print("SKIPPED: Element {!r} already in part.".format(element))
            return

        self.add_nodes(element.nodes)

        for node in element.nodes:
            if element not in node.connected_elements:
                node.connected_elements.append(element)

        if hasattr(element, "section"):
            if element.section:
                self.add_section(element.section)

        if hasattr(element.section, "material"):
            if element.section.material:
                self.add_material(element.section.material)

        element._key = len(self.elements)
        self.elements.add(element)
        element._registration = self
        if compas_fea2.VERBOSE:
            print("Element {!r} registered to {!r}.".format(element, self))
        return element

    def add_elements(self, elements):
        """Add multiple elements to the part.

        Parameters
        ----------
        elements : list[:class:`compas_fea2.model._Element`]

        Returns
        -------
        list[:class:`compas_fea2.model._Element`]

        """
        return [self.add_element(element) for element in elements]

    def remove_element(self, element):
        """Remove a :class:`compas_fea2.model._Element` from the part.

        Parameters
        ----------
        element : :class:`compas_fea2.model._Element`
            The element to remove.

        Warnings
        --------
        Removing elements can cause inconsistencies.

        """
        # type: (_Element) -> None
        if self.contains_element(element):
            self.elements.remove(element)
            element._registration = None
            for node in element.nodes:
                node.connected_elements.remove(element)
            if compas_fea2.VERBOSE:
                print("Element {!r} removed from {!r}.".format(element, self))

    def remove_elements(self, elements):
        """Remove multiple :class:`compas_fea2.model.Element` from the part.

        Parameters
        ----------
        elements : list[:class:`compas_fea2.model._Element`]
            List with the elements to remove.

        Warnings
        --------
        Removing elements can cause inconsistencies.

        """
        for element in elements:
            self.remove_element(element)

    def is_element_on_boundary(self, element):
        """Check if the element belongs to the boundary mesh of the part.

        Parameters
        ----------
        element : :class:`compas_fea2.model._Element`
            The element to check.

        Returns
        -------
        bool
            ``True`` if the element is on the boundary.

        """
        # type: (_Element) -> bool
        from compas.geometry import centroid_points

        if element.on_boundary is None:
            if not self._discretized_boundary_mesh.centroid_face:
                centroid_face = {}
                for face in self._discretized_boundary_mesh.faces():
                    centroid_face[TOL.geometric_key(self._discretized_boundary_mesh.face_centroid(face))] = face
            if isinstance(element, _Element3D):
                if any(TOL.geometric_key(centroid_points([node.xyz for node in face.nodes])) in self._discretized_boundary_mesh.centroid_face for face in element.faces):
                    element.on_boundary = True
                else:
                    element.on_boundary = False
            elif isinstance(element, _Element2D):
                if TOL.geometric_key(centroid_points([node.xyz for node in element.nodes])) in self._discretized_boundary_mesh.centroid_face:
                    element.on_boundary = True
                else:
                    element.on_boundary = False
        return element.on_boundary

    # =========================================================================
    #                           Faces methods
    # =========================================================================

    def find_faces_on_plane(self, plane):
        """Find the face of the elements that belongs to a given plane, if any.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane where the faces should belong.

        Returns
        -------
        list[:class:`compas_fea2.model.Face`]
            List with the faces belonging to the given plane.

        Notes
        -----
        The search is limited to solid elements.

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
            raise TypeError("{!r} is not a valid Group".format(group))

    def add_group(self, group):
        """Add a node or element group to the part.

        Parameters
        ----------
        group : :class:`compas_fea2.model.NodeGroup` | :class:`compas_fea2.model.ElementGroup`

        Returns
        -------
        :class:`compas_fea2.model.Group`

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
            if compas_fea2.VERBOSE:
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

        Returns
        -------
        list[:class:`compas_fea2.model.Group`]

        """
        return [self.add_group(group) for group in groups]

    # ==============================================================================
    # Results methods
    # ==============================================================================

    def sorted_nodes_by_displacement(self, step, component="length"):
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
        list[:class:`compas_fea2.model.Node`]
            The node sorted by displacment (ascending).

        """
        return sorted(self.nodes, key=lambda n: getattr(Vector(*n.results[step.problem][step].get("U", None)), component))

    def get_max_displacement(self, problem, step=None, component="length"):
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
        displacement = getattr(Vector(*node.results[problem][step].get("U", None)), component)
        return node, displacement

    def get_min_displacement(self, problem, step=None, component="length"):
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
        displacement = getattr(Vector(*node.results[problem][step].get("U", None)), component)
        return node, displacement

    def get_average_displacement_at_point(self, problem, point, distance, step=None, component="length", project=False):
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
        nodes = self.find_nodes_around_point(point=point, distance=distance, report=True)
        if nodes:
            displacements = [getattr(Vector(*node.results[problem][step].get("U", None)), component) for node in nodes]
            return point, sum(displacements) / len(displacements)

    # ==============================================================================
    # Viewer
    # ==============================================================================

    def show(self, scale_factor=1, draw_nodes=False, node_labels=False, solid=False):
        """Draw the parts.

        Parameters
        ----------
        parts : :class:`compas_fea2.model.DeformablePart` | [:class:`compas_fea2.model.DeformablePart`]
            The part or parts to draw.
        draw_nodes : bool, optional
            if `True` draw the nodes of the part, by default False
        node_labels : bool, optional
            if `True` add the node lables, by default False
        draw_envelope : bool, optional
            if `True` draw the outer boundary of the part, by default False
        solid : bool, optional
            if `True` draw all the elements (also the internal ones) of the part
            otherwise just show the boundary faces, by default True
        """

        from compas_fea2.UI.viewer import FEA2Viewer

        v = FEA2Viewer(self, scale_factor=scale_factor)

        if solid:
            v.draw_solid_elements(filter(lambda x: isinstance(x, _Element3D), self.elements), show_vertices=draw_nodes)
        else:
            if self.discretized_boundary_mesh:
                v.app.add(self.discretized_boundary_mesh, use_vertex_color=True)
        v.draw_shell_elements(
            filter(lambda x: isinstance(x, ShellElement), self.elements),
            show_vertices=draw_nodes,
        )
        v.draw_beam_elements(filter(lambda x: isinstance(x, BeamElement), self.elements), show_vertices=draw_nodes)
        # if draw_nodes:
        #     v.draw_nodes(self.nodes, node_labels)
        v.show()


class DeformablePart(_Part):
    """Deformable part."""

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

    def __init__(self, **kwargs):
        super(DeformablePart, self).__init__(**kwargs)
        self._materials = set()
        self._sections = set()
        self._releases = set()

    @property
    def materials(self):
        return self._materials

    @property
    def sections(self):
        return self._sections

    @property
    def releases(self):
        return self._releases

    # =========================================================================
    #                       Constructor methods
    # =========================================================================
    @classmethod
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
            faces = mesh.edge_faces(edge)
            n = [mesh.face_normal(f) for f in faces if f is not None]
            if len(n) == 1:
                n = n[0]
            else:
                n = n[0] + n[1]
            v = list(mesh.edge_direction(edge))
            frame = n
            frame.rotate(pi / 2, v, nodes[0].xyz)
            part.add_element(BeamElement(nodes=[*nodes], section=section, frame=frame))

        return part

    @classmethod
    # @timer(message='part successfully imported from gmsh model in ')
    def from_gmsh(cls, gmshModel, section, name=None, **kwargs):
        """ """
        return super().from_gmsh(gmshModel, name=name, section=section, **kwargs)

    @classmethod
    def from_boundary_mesh(cls, boundary_mesh, section, name=None, **kwargs):
        """ """
        return super().from_boundary_mesh(boundary_mesh, section=section, name=name, **kwargs)

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def find_materials_by_name(self, name):
        # type: (str) -> list
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
            raise TypeError("{!r} is not a material.".format(material))

        if self.contains_material(material):
            if compas_fea2.VERBOSE:
                print("SKIPPED: Material {!r} already in part.".format(material))
            return

        material._key = len(self._materials)
        self._materials.add(material)
        material._registration = self._registration
        return material

    def add_materials(self, materials):
        # type: (_Material) -> list
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
        # type: (str) -> list
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
            raise TypeError("{!r} is not a section.".format(section))

        if self.contains_section(section):
            if compas_fea2.VERBOSE:
                print("SKIPPED: Section {!r} already in part.".format(section))
            return

        self.add_material(section.material)
        section._key = len(self.sections)
        self._sections.add(section)
        section._registration = self._registration
        return section

    def add_sections(self, sections):
        # type: (list) -> _Section
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
            raise TypeError("{!r} is not a beam release element.".format(release))
        release.element = element
        release.location = location
        self._releases.add(release)
        return release


class RigidPart(_Part):
    """Rigid part."""

    __doc__ += _Part.__doc__
    __doc__ += """
    Addtional Attributes
    --------------------
    reference_point : :class:`compas_fea2.model.Node`
        A node acting as a reference point for the part, by default `None`. This
        is required if the part is rigid as it controls its movement in space.

    """

    def __init__(self, reference_point=None, **kwargs):
        super(RigidPart, self).__init__(**kwargs)
        self._reference_point = reference_point

    @property
    def reference_point(self):
        return self._reference_point

    @reference_point.setter
    def reference_point(self, value):
        self._reference_point = self.add_node(value)
        value._is_reference = True

    @classmethod
    # @timer(message='part successfully imported from gmsh model in ')
    def from_gmsh(cls, gmshModel, name=None, **kwargs):
        """ """
        kwargs["rigid"] = True
        return super().from_gmsh(gmshModel, name=name, **kwargs)

    @classmethod
    def from_boundary_mesh(cls, boundary_mesh, name=None, **kwargs):
        """ """
        kwargs["rigid"] = True
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
        if not hasattr(element, "rigid"):
            raise TypeError("The element type cannot be assigned to a RigidPart")
        if not getattr(element, "rigid"):
            raise TypeError("Rigid parts can only have rigid elements")
        return super().add_element(element)
