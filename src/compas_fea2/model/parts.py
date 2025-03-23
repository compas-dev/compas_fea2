from math import pi
from math import sqrt
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from compas.topology import connected_components
from collections import defaultdict
from itertools import groupby
import h5py
import json

import compas
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Transformation
from compas.geometry import Vector
from compas.geometry import bounding_box
from compas.geometry import centroid_points, centroid_points_weighted
from compas.geometry import distance_point_point_sqrd
from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_on_plane
from compas.datastructures import Mesh
from compas.tolerance import TOL
from scipy.spatial import KDTree

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
from .groups import ElementsGroup, FacesGroup, NodesGroup, MaterialsGroup, SectionsGroup, _Group

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
        Unique identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Unique identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    model : :class:`compas_fea2.model.Model`
        The parent model of the part.
    nodes : Set[:class:`compas_fea2.model.Node`]
        The nodes belonging to the part.
    nodes_count : int
        Number of nodes in the part.
    gkey_node : Dict[str, :class:`compas_fea2.model.Node`]
        Dictionary that associates each node and its geometric key.
    materials : Set[:class:`compas_fea2.model._Material`]
        The materials belonging to the part.
    sections : Set[:class:`compas_fea2.model._Section`]
        The sections belonging to the part.
    elements : Set[:class:`compas_fea2.model._Element`]
        The elements belonging to the part.
    element_types : Dict[:class:`compas_fea2.model._Element`, List[:class:`compas_fea2.model._Element`]]
        Dictionary with the elements of the part for each element type.
    element_count : int
        Number of elements in the part.
    boundary_mesh : :class:`compas.datastructures.Mesh`
        The outer boundary mesh enveloping the Part.
    discretized_boundary_mesh : :class:`compas.datastructures.Mesh`
        The discretized outer boundary mesh enveloping the Part.

    Notes
    -----
    Parts are registered to a :class:`compas_fea2.model.Model`.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ndm = None
        self._ndf = None
        self._graph = nx.DiGraph()
        self._nodes: Set[Node] = set()
        self._gkey_node: Dict[str, Node] = {}
        self._sections: Set[_Section] = set()
        self._materials: Set[_Material] = set()
        self._elements: Set[_Element] = set()
        self._releases: Set[_BeamEndRelease] = set()

        self._groups: Set[_Group] = set()

        self._boundary_mesh = None
        self._discretized_boundary_mesh = None

        self._reference_point = None

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__,
            "ndm": self._ndm or None,
            "ndf": self._ndf or None,
            "nodes": [node.__data__ for node in self.nodes],
            "gkey_node": {key: node.__data__ for key, node in self.gkey_node.items()},
            "materials": [material.__data__ for material in self.materials],
            "sections": [section.__data__ for section in self.sections],
            "elements": [element.__data__ for element in self.elements],
            "releases": [release.__data__ for release in self.releases],
        }

    def to_hdf5_data(self, hdf5_file, mode="a"):
        group = hdf5_file.require_group(f"model/{"parts"}/{self.uid}")  # Create a group for this object
        group.attrs["class"] = str(self.__data__["class"])

    @classmethod
    def __from_data__(cls, data):
        """Create a part instance from a data dictionary.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        _Part
            The part instance.
        """
        part = cls()
        part._ndm = data.get("ndm")
        part._ndf = data.get("ndf")

        # Deserialize nodes
        uid_node = {node_data["uid"]: Node.__from_data__(node_data) for node_data in data.get("nodes", [])}

        # Deserialize materials
        for material_data in data.get("materials", []):
            material_cls = material_data.pop("class", None)
            if not material_cls:
                raise ValueError("Missing class information for material.")

            mat = part.add_material(material_cls.__from_data__(material_data))
            mat.uid = material_data["uid"]

        # Deserialize sections
        for section_data in data.get("sections", []):
            material_data = section_data.pop("material", None)
            if not material_data or "uid" not in material_data:
                raise ValueError("Material UID is missing in section data.")

            material = part.find_material_by_uid(material_data["uid"])
            if not material:
                raise ValueError(f"Material with UID {material_data['uid']} not found.")

            section_cls = section_data.pop("class", None)
            if not section_cls:
                raise ValueError("Missing class information for section.")

            section = part.add_section(section_cls(material=material, **section_data))
            section.uid = section_data["uid"]

        # Deserialize elements
        for element_data in data.get("elements", []):
            section_data = element_data.pop("section", None)
            if not section_data or "uid" not in section_data:
                raise ValueError("Section UID is missing in element data.")

            section = part.find_section_by_uid(section_data["uid"])
            if not section:
                raise ValueError(f"Section with UID {section_data['uid']} not found.")

            element_cls = element_data.pop("class", None)
            if not element_cls:
                raise ValueError("Missing class information for element.")

            nodes = [uid_node[node_data["uid"]] for node_data in element_data.pop("nodes", [])]
            for node in nodes:
                node._registration = part
            element = element_cls(nodes=nodes, section=section, **element_data)
            part.add_element(element, checks=False)

        part._boundary_mesh = Mesh.__from_data__(data.get("boundary_mesh")) if data.get("boundary_mesh") else None
        part._discretized_boundary_mesh = Mesh.__from_data__(data.get("discretized_boundary_mesh")) if data.get("discretized_boundary_mesh") else None
        return part

    @property
    def reference_point(self) -> Optional[Node]:
        return self._reference_point

    @reference_point.setter
    def reference_point(self, value: Node):
        self._reference_point = self.add_node(value)
        value._is_reference = True

    @property
    def graph(self):
        return self._graph

    @property
    def nodes(self) -> NodesGroup:
        return NodesGroup(self._nodes)

    @property
    def nodes_sorted(self) -> List[Node]:
        return self.nodes.sorted_by(key=lambda x: x.part_key)

    @property
    def points(self) -> List[Point]:
        return [node.point for node in self._nodes]

    @property
    def points_sorted(self) -> List[Point]:
        return [node.point for node in self.nodes.sorted_by(key=lambda x: x.part_key)]

    @property
    def elements(self) -> ElementsGroup:
        return ElementsGroup(self._elements)

    @property
    def faces(self) -> FacesGroup:
        return FacesGroup([face for element in self.elements for face in element.faces])

    @property
    def elements_sorted(self) -> List[_Element]:
        return self.elments.sorted_by(key=lambda x: x.part_key)

    @property
    def elements_grouped(self) -> Dict[int, List[_Element]]:
        sub_groups = self.elements.group_by(key=lambda x: x.__class__.__base__)
        return {key: group.members for key, group in sub_groups}

    @property
    def elements_faces(self) -> List[List[List["Face"]]]:
        face_group = FacesGroup([face for element in self.elements for face in element.faces])
        face_group.group_by(key=lambda x: x.element)
        return face_group

    @property
    def elements_faces_grouped(self) -> Dict[int, List[List["Face"]]]:
        return {key: [face for face in element.faces] for key, element in self.elements_grouped.items()}

    @property
    def elements_faces_indices(self) -> List[List[List[float]]]:
        return [face.nodes_key for face in self.elements_faces]

    @property
    def elements_faces_indices_grouped(self) -> Dict[int, List[List[float]]]:
        return {key: [face.nodes_key for face in element.faces] for key, element in self.elements_grouped.items()}

    @property
    def elements_connectivity(self) -> List[List[int]]:
        return [element.nodes_key for element in self.elements]

    @property
    def elements_connectivity_grouped(self) -> Dict[int, List[List[float]]]:
        elements_group = groupby(self.elements, key=lambda x: x.__class__.__base__)
        return {key: [element.nodes_key for element in group] for key, group in elements_group}

    @property
    def elements_centroids(self) -> List[List[float]]:
        return [element.centroid for element in self.elements]

    @property
    def sections(self) -> SectionsGroup:
        return SectionsGroup(self._sections)

    @property
    def sections_sorted(self) -> List[_Section]:
        return self.sections.sorted_by(key=lambda x: x.part_key)

    @property
    def sections_grouped_by_element(self) -> Dict[int, List[_Section]]:
        sections_group = self.sections.group_by(key=lambda x: x.element)
        return {key: group.members for key, group in sections_group}

    @property
    def materials(self) -> MaterialsGroup:
        return MaterialsGroup(self._materials)

    @property
    def materials_sorted(self) -> List[_Material]:
        return self.materials.sorted_by(key=lambda x: x.part_key)

    @property
    def materials_grouped_by_section(self) -> Dict[int, List[_Material]]:
        materials_group = self.materials.group_by(key=lambda x: x.section)
        return {key: group.members for key, group in materials_group}

    @property
    def releases(self) -> Set[_BeamEndRelease]:
        return self._releases

    @property
    def gkey_node(self) -> Dict[str, Node]:
        return self._gkey_node

    @property
    def boundary_mesh(self):
        return self._boundary_mesh

    @property
    def discretized_boundary_mesh(self):
        return self._discretized_boundary_mesh

    @property
    def outer_faces(self):
        """Extract the outer faces of the part."""
        # FIXME: extend to shell elements
        face_count = defaultdict(int)
        for tet in self.elements_connectivity:
            faces = [
                tuple(sorted([tet[0], tet[1], tet[2]])),
                tuple(sorted([tet[0], tet[1], tet[3]])),
                tuple(sorted([tet[0], tet[2], tet[3]])),
                tuple(sorted([tet[1], tet[2], tet[3]])),
            ]
            for face in faces:
                face_count[face] += 1
        # Extract faces that appear only once (boundary faces)
        outer_faces = np.array([face for face, count in face_count.items() if count == 1])
        return outer_faces

    @property
    def outer_mesh(self):
        """Extract the outer mesh of the part."""
        unique_vertices, unique_indices = np.unique(self.outer_faces, return_inverse=True)
        vertices = np.array(self.points_sorted)[unique_vertices]
        faces = unique_indices.reshape(self.outer_faces.shape).tolist()
        return Mesh.from_vertices_and_faces(vertices.tolist(), faces)

    def extract_clustered_planes(self, tol: float = 1e-3, angle_tol: float = 2, verbose: bool = False):
        """Extract unique planes from the part boundary mesh.

        Parameters
        ----------
        tol : float, optional
            Tolerance for geometric operations, by default 1e-3.
        angle_tol : float, optional
            Tolerance for normal vector comparison, by default 2.
        verbose : bool, optional
            If ``True`` print the extracted planes, by default False.

        Returns
        -------
        list[:class:`compas.geometry.Plane`]
        """
        mesh = self.discretized_boundary_mesh.copy()
        unique_planes = []
        plane_data = []
        for fkey in mesh.faces():
            plane = mesh.face_plane(fkey)
            normal = np.array(plane.normal)
            offset = np.dot(normal, plane.point)
            plane_data.append((normal, offset))

        # Clusterize planes based on angular similarity
        plane_normals = np.array([p[0] for p in plane_data])
        plane_offsets = np.array([p[1] for p in plane_data])
        cos_angle_tol = np.cos(np.radians(angle_tol))
        for _, (normal, offset) in enumerate(zip(plane_normals, plane_offsets)):
            is_unique = True
            for existing_normal, existing_offset in unique_planes:
                if np.abs(np.dot(normal, existing_normal)) > cos_angle_tol:
                    if np.abs(offset - existing_offset) < tol:
                        is_unique = False
                        break
            if is_unique:
                unique_planes.append((normal, offset))

        # Convert unique planes back to COMPAS
        planes = []
        for normal, offset in unique_planes:
            normal_vec = Vector(*normal)
            point = normal_vec * offset
            planes.append(Plane(point, normal_vec))

        if verbose:
            num_unique_planes = len(unique_planes)
            print(f"Minimum number of planes describing the geometry: {num_unique_planes}")
            for i, (normal, offset) in enumerate(unique_planes, 1):
                print(f"Plane {i}: Normal = {normal}, Offset = {offset}")

        return planes

    def extract_submeshes(self, planes: List[Plane], tol: float = 1e-3, normal_tol: float = 2, split=False):
        """Extract submeshes from the part based on the planes provided.

        Parameters
        ----------
        planes : list[:class:`compas.geometry.Plane`]
            Planes to slice the part.
        tol : float, optional
            Tolerance for geometric operations, by default 1e-3.
        normal_tol : float, optional
            Tolerance for normal vector comparison, by default 2.
        split : bool, optional
            If ``True`` split each submesh into connected components, by default False.

        Returns
        -------
        list[:class:`compas.datastructures.Mesh`]
        """

        def split_into_subsubmeshes(submeshes):
            """Split each submesh into connected components."""
            subsubmeshes = []

            for mesh in submeshes:
                mesh: Mesh
                components = connected_components(mesh.adjacency)

                for comp in components:
                    faces = [fkey for fkey in mesh.faces() if set(mesh.face_vertices(fkey)).issubset(comp)]
                    submesh = Mesh()

                    vkey_map = {
                        v: submesh.add_vertex(
                            x=mesh.vertex_attribute(v, "x"),
                            y=mesh.vertex_attribute(v, "y"),
                            z=mesh.vertex_attribute(v, "z"),
                        )
                        for v in comp
                    }

                    for fkey in faces:
                        submesh.add_face([vkey_map[v] for v in mesh.face_vertices(fkey)])

                    subsubmeshes.append(submesh)

            return subsubmeshes

        mesh: Mesh = self.discretized_boundary_mesh
        submeshes = [Mesh() for _ in planes]

        # Step 1: Compute normalized plane and face normals
        planes_normals = np.array([plane.normal for plane in planes])
        faces_normals = np.array([mesh.face_normal(face) for face in mesh.faces()])
        dot_products = np.dot(planes_normals, faces_normals.T)  # (num_planes, num_faces)
        plane_indices, face_indices = np.where(abs(dot_products) >= (1 - normal_tol))

        for face_idx in np.unique(face_indices):  # Loop over unique faces
            face_vertices = mesh.face_vertices(face_idx)
            face_coords = [mesh.vertex_coordinates(v) for v in face_vertices]

            # Get all planes matching this face's normal
            matching_planes = [planes[p_idx] for p_idx in plane_indices[face_indices == face_idx]]

            # Step 5: Check if all vertices of the face lie on any of the matching planes
            for plane in matching_planes:
                if all(is_point_on_plane(coord, plane, tol) for coord in face_coords):
                    face_mesh = Mesh.from_vertices_and_faces(face_coords, [[c for c in range(len(face_coords))]])
                    submeshes[planes.index(plane)].join(face_mesh)
                    break  # Assign to first valid plane
        if split:
            for submesh in submeshes:
                submesh.weld(precision=2)
            submeshes = split_into_subsubmeshes(submeshes)
        return submeshes

    @property
    def all_interfaces(self):
        from compas_fea2.model.interfaces import Interface

        planes = self.extract_clustered_planes(tol=1, angle_tol=2)
        submeshes = self.extract_submeshes(planes, tol=1, normal_tol=2, split=True)
        return [Interface(mesh=mesh) for mesh in submeshes]

    @property
    def bounding_box(self) -> Optional[Box]:
        # FIXME: add bounding box for lienar elements (bb of the section outer boundary)
        return Box.from_bounding_box(bounding_box([n.xyz for n in self.nodes]))

    @property
    def center(self) -> Point:
        """The geometric center of the part."""
        return centroid_points(self.bounding_box.points)

    @property
    def centroid(self) -> Point:
        """The geometric center of the part."""
        self.compute_nodal_masses()
        return centroid_points_weighted([node.point for node in self.nodes], [sum(node.mass) / len(node.mass) for node in self.nodes])

    @property
    def bottom_plane(self) -> Plane:
        return Plane.from_three_points(*[self.bounding_box.points[i] for i in self.bounding_box.bottom[:3]])

    @property
    def top_plane(self) -> Plane:
        return Plane.from_three_points(*[self.bounding_box.points[i] for i in self.bounding_box.top[:3]])

    @property
    def volume(self) -> float:
        self._volume = 0.0
        for element in self.elements:
            if element.volume:
                self._volume += element.volume
        return self._volume

    @property
    def weight(self) -> float:
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
    def nodes_count(self) -> int:
        return len(self.nodes) - 1

    @property
    def elements_count(self) -> int:
        return len(self.elements) - 1

    @property
    def element_types(self) -> Dict[type, List[_Element]]:
        element_types = {}
        for element in self.elements:
            element_types.setdefault(type(element), []).append(element)
        return element_types

    @property
    def groups(self) -> Set[_Group]:
        return self._groups

    def transform(self, transformation: Transformation) -> None:
        """Transform the part.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.

        """
        for node in self.nodes:
            node.transform(transformation)

    def transformed(self, transformation: Transformation) -> "_Part":
        """Return a transformed copy of the part.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.
        """
        part = self.copy()
        part.transform(transformation)
        return part

    def elements_by_dimension(self, dimension: int = 1) -> Iterable[_Element]:
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
    def from_compas_lines(
        cls,
        lines: List["compas.geometry.Line"],
        element_model: str = "BeamElement",
        xaxis: List[float] = [0, 1, 0],
        section: Optional["_Section"] = None,
        name: Optional[str] = None,
        **kwargs,
    ) -> "_Part":
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
        mass = kwargs.get("mass", None)
        for line in lines:
            frame = Frame(line.start, xaxis, line.vector)

            nodes = []
            for p in [line.start, line.end]:
                if g := prt.nodes.subgroup(condition=lambda node: node.point == p):
                    nodes.append(list(g.nodes)[0])
                else:
                    nodes.append(Node(list(p), mass=mass))

            prt.add_nodes(nodes)
            element = getattr(compas_fea2.model, element_model)(nodes=nodes, section=section, frame=frame)
            if not isinstance(element, _Element1D):
                raise ValueError("Provide a 1D element")
            prt.add_element(element)
        return prt

    @classmethod
    def shell_from_compas_mesh(cls, mesh, section: ShellSection, name: Optional[str] = None, **kwargs) -> "_Part":
        """Creates a Part object from a :class:`compas.datastructures.Mesh`.

        To each face of the mesh is assigned a :class:`compas_fea2.model.ShellElement`
        object. Currently, the same section is applied to all the elements.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            Mesh to convert to a Part.
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
    def from_gmsh(cls, gmshModel, section: Optional[Union[SolidSection, ShellSection]] = None, name: Optional[str] = None, **kwargs) -> "_Part":
        """Create a Part object from a gmshModel object with support for C3D4 and C3D10 elements.

        Parameters
        ----------
        gmshModel : object
            Gmsh Model to convert.
        section : Union[SolidSection, ShellSection], optional
            The section type (`SolidSection` or `ShellSection`).
        name : str, optional
            Name of the new part.
        split : bool, optional
            Feature under development.
        verbose : bool, optional
            If `True`, print logs.
        rigid : bool, optional
            If `True`, applies rigid constraints.
        check : bool, optional
            If `True`, performs sanity checks (resource-intensive).

        Returns
        -------
        _Part
            The part meshed.

        Notes
        -----
        - Detects whether elements are C3D4 (4-node) or C3D10 (10-node) and assigns correctly.
        - The `gmshModel` should have the correct dimensions for the given section.

        """
        part = cls(name=name)

        # gmshModel.set_option("Mesh.ElementOrder", 2)
        # gmshModel.set_option("Mesh.Optimize", 1)
        # gmshModel.set_option("Mesh.OptimizeNetgen", 1)
        # gmshModel.set_option("Mesh.SecondOrderLinear", 0)
        # gmshModel.set_option("Mesh.OptimizeNetgen", 1)

        gmshModel.heal()
        gmshModel.generate_mesh(3)
        model = gmshModel.model

        # Add nodes
        node_coords = model.mesh.get_nodes()[1].reshape((-1, 3), order="C")
        fea2_nodes = np.array([part.add_node(Node(coords)) for coords in node_coords])

        # Get elements
        gmsh_elements = model.mesh.get_elements()
        dimension = 2 if isinstance(section, SolidSection) else 1
        ntags_per_element = np.split(gmsh_elements[2][dimension] - 1, len(gmsh_elements[1][dimension]))  # gmsh keys start from 1

        verbose = kwargs.get("verbose", False)
        rigid = kwargs.get("rigid", False)
        implementation = kwargs.get("implementation", None)

        for ntags in ntags_per_element:
            if kwargs.get("split", False):
                raise NotImplementedError("This feature is under development")

            element_nodes = fea2_nodes[ntags]

            if ntags.size == 3:
                part.add_element(ShellElement(nodes=element_nodes, section=section, rigid=rigid, implementation=implementation))

            elif ntags.size == 4:
                if isinstance(section, ShellSection):
                    part.add_element(ShellElement(nodes=element_nodes, section=section, rigid=rigid, implementation=implementation))
                else:
                    part.add_element(TetrahedronElement(nodes=element_nodes, section=section, rigid=rigid))
                    part.ndf = 3  # FIXME: try to move outside the loop

            elif ntags.size == 10:  # C3D10 tetrahedral element
                part.add_element(TetrahedronElement(nodes=element_nodes, section=section, rigid=rigid))  # Automatically supports C3D10
                part.ndf = 3

            elif ntags.size == 8:
                part.add_element(HexahedronElement(nodes=element_nodes, section=section, rigid=rigid))

            else:
                raise NotImplementedError(f"Element with {ntags.size} nodes not supported")

            if verbose:
                print(f"Element {ntags} added")

        if not part._boundary_mesh:
            gmshModel.generate_mesh(2)  # FIXME: Get the volumes without the mesh
            part._boundary_mesh = gmshModel.mesh_to_compas()

        if not part._discretized_boundary_mesh:
            part._discretized_boundary_mesh = part._boundary_mesh

        if rigid:
            point = part._discretized_boundary_mesh.centroid()
            part.reference_point = Node(xyz=point)

        return part

    @classmethod
    def from_boundary_mesh(cls, boundary_mesh, name: Optional[str] = None, **kwargs) -> "_Part":
        """Create a Part object from a 3-dimensional :class:`compas.datastructures.Mesh`
        object representing the boundary envelope of the Part. The Part is
        discretized uniformly in Tetrahedra of a given mesh size.
        The same section is applied to all the elements.

        Parameters
        ----------
        boundary_mesh : :class:`compas.datastructures.Mesh`
            Boundary envelope of the Part.
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
        _Part
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

        if gmshModel:
            del gmshModel

        return part

    @classmethod
    def from_step_file(cls, step_file: str, name: Optional[str] = None, **kwargs) -> "_Part":
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
        _Part
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

        if gmshModel:
            del gmshModel
        print("Part created.")

        return part

    @classmethod
    def from_brep(cls, brep, name: Optional[str] = None, **kwargs) -> "_Part":
        from compas_gmsh.models import MeshModel

        mesh_size_at_vertices = kwargs.get("mesh_size_at_vertices", None)
        target_point_mesh_size = kwargs.get("target_point_mesh_size", None)
        meshsize_max = kwargs.get("meshsize_max", None)
        meshsize_min = kwargs.get("meshsize_min", None)

        print("Creating the part from the step file...")
        gmshModel = MeshModel.from_brep(brep)

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

        if gmshModel:
            del gmshModel
        print("Part created.")

        return part

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def find_materials_by_name(self, name: str) -> List[_Material]:
        """Find all materials with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        List[_Material]
        """
        mg = MaterialsGroup(self.materials)
        return mg.subgroup(condition=lambda x: x.name == name).materials

    def find_material_by_uid(self, uid: str) -> Optional[_Material]:
        """Find a material with a given unique identifier.

        Parameters
        ----------
        uid : str

        Returns
        -------
        Optional[_Material]
        """
        for material in self.materials:
            if material.uid == uid:
                return material
        return None

    def contains_material(self, material: _Material) -> bool:
        """Verify that the part contains a specific material.

        Parameters
        ----------
        material : _Material

        Returns
        -------
        bool
        """
        return material in self.materials

    def add_material(self, material: _Material) -> _Material:
        """Add a material to the part so that it can be referenced in section and element definitions.

        Parameters
        ----------
        material : _Material

        Returns
        -------
        _Material

        Raises
        ------
        TypeError
            If the material is not a material.
        """
        if not isinstance(material, _Material):
            raise TypeError(f"{material!r} is not a material.")

        self._materials.add(material)
        material._registration = self
        return material

    def add_materials(self, materials: List[_Material]) -> List[_Material]:
        """Add multiple materials to the part.

        Parameters
        ----------
        materials : List[_Material]

        Returns
        -------
        List[_Material]
        """
        return [self.add_material(material) for material in materials]

    def find_material_by_name(self, name: str) -> Optional[_Material]:
        """Find a material with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        Optional[_Material]
        """
        for material in self.materials:
            if material.name == name:
                return material
        return None

    # =========================================================================
    #                        Sections methods
    # =========================================================================

    def find_sections_by_name(self, name: str) -> List[_Section]:
        """Find all sections with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        List[_Section]
        """
        return [section for section in self.sections if section.name == name]

    def find_section_by_uid(self, uid: str) -> Optional[_Section]:
        """Find a section with a given unique identifier.

        Parameters
        ----------
        uid : str

        Returns
        -------
        Optional[_Section]
        """
        for section in self.sections:
            if section.uid == uid:
                return section
        return None

    def contains_section(self, section: _Section) -> bool:
        """Verify that the part contains a specific section.

        Parameters
        ----------
        section : _Section

        Returns
        -------
        bool
        """
        return section in self.sections

    def add_section(self, section: _Section) -> _Section:
        """Add a section to the part so that it can be referenced in element definitions.

        Parameters
        ----------
        section : :class:`compas_fea2.model.Section`

        Returns
        -------
        _Section

        Raises
        ------
        TypeError
            If the section is not a section.

        """
        if not isinstance(section, _Section):
            raise TypeError("{!r} is not a section.".format(section))

        self.add_material(section.material)
        self._sections.add(section)
        section._registration = self
        return section

    def add_sections(self, sections: List[_Section]) -> List[_Section]:
        """Add multiple sections to the part.

        Parameters
        ----------
        sections : list[:class:`compas_fea2.model.Section`]

        Returns
        -------
        list[:class:`compas_fea2.model.Section`]
        """
        return [self.add_section(section) for section in sections]

    def find_section_by_name(self, name: str) -> Optional[_Section]:
        """Find a section with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        Optional[_Section]
        """
        for section in self.sections:
            if section.name == name:
                return section
        return

    # =========================================================================
    #                           Nodes methods
    # =========================================================================
    def find_node_by_uid(self, uid: str) -> Optional[Node]:
        """Retrieve a node in the part using its unique identifier.

        Parameters
        ----------
        uid : str
            The node's unique identifier.

        Returns
        -------
        Optional[Node]
            The corresponding node, or None if not found.

        """
        for node in self._nodes:
            if node.uid == uid:
                return node
        return None

    def find_node_by_key(self, key: int) -> Optional[Node]:
        """Retrieve a node in the model using its key.

        Parameters
        ----------
        key : int
            The node's key.

        Returns
        -------
        Optional[Node]
            The corresponding node, or None if not found.

        """
        for node in self._nodes:
            if node.key == key:
                return node
        print(f"No nodes found with key {key}")
        return None

    def find_node_by_name(self, name: str) -> List[Node]:
        """Find a node with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        List[Node]
            List of nodes with the given name.

        """
        for node in self._nodes:
            if node.name == name:
                return node
        print(f"No nodes found with name {name}")
        return None

    def find_nodes_on_plane(self, plane: Plane, tol: float = 1.0) -> List[Node]:
        """Find all nodes on a given plane.

        Parameters
        ----------
        plane : Plane
            The plane.
        tol : float, optional
            Tolerance for the search, by default 1.0.

        Returns
        -------
        List[Node]
            List of nodes on the given plane.
        """
        return self.nodes.subgroup(condition=lambda x: is_point_on_plane(x.point, plane, tol))

    def find_closest_nodes_to_point(self, point: List[float], number_of_nodes: int = 1, report: bool = False, single: bool = False) -> Union[List[Node], Dict[Node, float]]:
        """
        Find the closest number_of_nodes nodes to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point` | List[float]
            Point or List of coordinates representing the point in x, y, z.
        number_of_nodes : int
            The number of closest points to find.
        report : bool
            Whether to return distances along with the nodes.

        Returns
        -------
        List[Node] or Dict[Node, float]
            A list of the closest nodes, or a dictionary with nodes
            and distances if report=True.
        """
        if number_of_nodes > len(self.nodes):
            if compas_fea2.VERBOSE:
                print(f"The number of nodes to find exceeds the available nodes. Capped to {len(self.nodes)}")
            number_of_nodes = len(self.nodes)
        if number_of_nodes < 0:
            raise ValueError("The number of nodes to find must be positive")

        if number_of_nodes == 0:
            return None

        tree = KDTree(self.points)
        distances, indices = tree.query(point, k=number_of_nodes)
        if number_of_nodes == 1:
            if single:
                return list(self.nodes)[indices]
            else:
                distances = [distances]
                indices = [indices]
                closest_nodes = [list(self.nodes)[i] for i in indices]

        if report:
            # Return a dictionary with nodes and their distances
            return {node: distance for node, distance in zip(closest_nodes, distances)}

        return NodesGroup(closest_nodes)

    def find_closest_nodes_to_node(self, node: Node, number_of_nodes: int = 1, report: Optional[bool] = False, single: bool = False) -> List[Node]:
        """Find the n closest nodes around a given node (excluding the node itself).

        Parameters
        ----------
        node : Node
            The given node.
        distance : float
            Distance from the location.
        number_of_nodes : int
            Number of nodes to return.
        plane : Optional[Plane], optional
            Limit the search to one plane.

        Returns
        -------
        List[Node]
            List of the closest nodes.
        """
        return self.find_closest_nodes_to_point(node.xyz, number_of_nodes, report=report, single=single)

    def find_nodes_in_polygon(self, polygon: "compas.geometry.Polygon", tol: float = 1.1) -> List[Node]:
        """Find the nodes of the part that are contained within a planar polygon.

        Parameters
        ----------
        polygon : compas.geometry.Polygon
            The polygon for the search.
        tol : float, optional
            Tolerance for the search, by default 1.1.

        Returns
        -------
        List[Node]
            List of nodes within the polygon.
        """
        if not hasattr(polygon, "plane"):
            try:
                polygon.plane = Frame.from_points(*polygon.points[:3])
            except Exception:
                polygon.plane = Frame.from_points(*polygon.points[-3:])
        S = Scale.from_factors([tol] * 3, polygon.frame)
        T = Transformation.from_frame_to_frame(Frame.from_plane(polygon.plane), Frame.worldXY())
        nodes_on_plane: NodesGroup = self.find_nodes_on_plane(Plane.from_frame(polygon.plane))
        polygon_xy = polygon.transformed(S)
        polygon_xy = polygon.transformed(T)
        return nodes_on_plane.subgroup(condition=lambda x: is_point_in_polygon_xy(Point(*x.xyz).transformed(T), polygon_xy))

    def contains_node(self, node: Node) -> bool:
        """Verify that the part contains a given node.

        Parameters
        ----------
        node : Node
            The node to check.

        Returns
        -------
        bool
            True if the node is in the part, False otherwise.
        """
        return node in self.nodes

    def add_node(self, node: Node) -> Node:
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
        >>> part = Part()
        >>> node = Node(xyz=(1.0, 2.0, 3.0))
        >>> part.add_node(node)

        """
        if not isinstance(node, Node):
            raise TypeError("{!r} is not a node.".format(node))

        # if not compas_fea2.POINT_OVERLAP:
        #     existing_node = self.find_nodes_around_point(node.xyz, distance=compas_fea2.GLOBAL_TOLERANCE)
        #     if existing_node:
        #         if compas_fea2.VERBOSE:
        #             print("NODE SKIPPED: Part {!r} has already a node at {}.".format(self, node.xyz))
        #         return existing_node[0]

        if node not in self._nodes:
            node._part_key = len(self.nodes)
            self._nodes.add(node)
            self._gkey_node[node.gkey] = node
            node._registration = self
            if compas_fea2.VERBOSE:
                print("Node {!r} registered to {!r}.".format(node, self))
        return node

    def add_nodes(self, nodes: List[Node]) -> List[Node]:
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
        >>> part = Part()
        >>> node1 = Node([1.0, 2.0, 3.0])
        >>> node2 = Node([3.0, 4.0, 5.0])
        >>> node3 = Node([3.0, 4.0, 5.0])
        >>> nodes = part.add_nodes([node1, node2, node3])

        """
        return [self.add_node(node) for node in nodes]

    def remove_node(self, node: Node) -> None:
        """Remove a :class:`compas_fea2.model.Node` from the part.

        Warnings
        --------
        Removing nodes can cause inconsistencies.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node to remove.

        """
        if self.contains_node(node):
            self.nodes.remove(node)
            self._gkey_node.pop(node.gkey)
            node._registration = None
            if compas_fea2.VERBOSE:
                print(f"Node {node!r} removed from {self!r}.")

    def remove_nodes(self, nodes: List[Node]) -> None:
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

    def is_node_on_boundary(self, node: Node, precision: Optional[float] = None) -> bool:
        """Check if a node is on the boundary mesh of the Part.

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
            node._on_boundary = TOL.geometric_key(node.xyz, precision) in self.discretized_boundary_mesh.gkey_vertex()
        return node.on_boundary

    def compute_nodal_masses(self) -> List[float]:
        """Compute the nodal mass of the part.

        Warnings
        --------
        Rotational masses are not considered.

        Returns
        -------
        list
            List with the nodal masses.

        """
        # clear masses
        for node in self.nodes:
            for i in range(len(node.mass)):
                node.mass[i] = 0.0
        for element in self.elements:
            for node in element.nodes:
                node.mass = [a + b for a, b in zip(node.mass, element.nodal_mass[:3])] + [0.0, 0.0, 0.0]
        return [sum(node.mass[i] for node in self.nodes) for i in range(3)]

    def visualize_node_connectivity(self):
        """Visualizes nodes with color coding based on connectivity."""
        degrees = {node: self.graph.degree(node) for node in self.graph.nodes}
        pos = nx.spring_layout(self.graph)

        node_colors = [degrees[node] for node in self.graph.nodes]

        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues, node_size=2000)
        plt.title("Node Connectivity Visualization")
        plt.show()

    def visualize_pyvis(self, filename="model_graph.html"):
        from pyvis.network import Network

        """Visualizes the Model-Part and Element-Node graph using Pyvis."""
        net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white")

        # # Add all nodes from Model-Part Graph
        # for node in self.model.graph.nodes:
        #     node_type = self.model.graph.nodes[node].get("type", "unknown")

        #     if node_type == "model":
        #         net.add_node(str(node), label="Model", color="red", shape="box", size=30)
        #     elif node_type == "part":
        #         net.add_node(str(node), label=node.name, color="blue", shape="ellipse")

        # # Add all edges from Model-Part Graph
        # for src, dst, data in self.model.graph.edges(data=True):
        #     net.add_edge(str(src), str(dst), color="gray", title=data.get("relation", ""))

        # Add all nodes from Element-Node Graph
        for node in self.graph.nodes:
            node_type = self.graph.nodes[node].get("type", "unknown")

            if node_type == "element":
                net.add_node(str(node), label=node.name, color="yellow", shape="triangle")
            elif node_type == "node":
                net.add_node(str(node), label=node.name, color="green", shape="dot")

        # # Add all edges from Element-Node Graph
        # for src, dst, data in self.graph.edges(data=True):
        #     net.add_edge(str(src), str(dst), color="lightgray", title=data.get("relation", ""))

        # Save and Open
        net.show(filename)
        print(f"Graph saved as {filename} - Open in a browser to view.")

    # =========================================================================
    #                           Elements methods
    # =========================================================================
    def find_element_by_key(self, key: int) -> Optional[_Element]:
        """Retrieve an element in the model using its key.

        Parameters
        ----------
        key : int
            The element's key.

        Returns
        -------
        Optional[_Element]
            The corresponding element, or None if not found.
        """
        for element in self.elements:
            if element.key == key:
                return element
        return None

    def find_element_by_name(self, name: str) -> List[_Element]:
        """Find all elements with a given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        List[_Element]
            List of elements with the given name.
        """
        for element in self.elements:
            if element.key == name:
                return element
        return None

    def contains_element(self, element: _Element) -> bool:
        """Verify that the part contains a specific element.

        Parameters
        ----------
        element : _Element

        Returns
        -------
        bool
        """
        return element in self.elements

    def add_element(self, element: _Element, checks=True) -> _Element:
        """Add an element to the part.

        Parameters
        ----------
        element : _Element
            The element instance.
        checks : bool, optional
            Perform checks before adding the element, by default True.
            Turned off during copy operations.

        Returns
        -------
        _Element

        Raises
        ------
        TypeError
            If the element is not an instance of _Element.
        """
        if checks and (not isinstance(element, _Element) or self.contains_element(element)):
            if compas_fea2.VERBOSE:
                print(f"SKIPPED: {element!r} is not an element or already in part.")
            return element

        self.add_nodes(element.nodes)
        for node in element.nodes:
            node.connected_elements.add(element)

        self.add_section(element.section)

        element._part_key = len(self.elements)
        self._elements.add(element)
        element._registration = self

        self.graph.add_node(element, type="element")
        for node in element.nodes:
            self.graph.add_node(node, type="node")
            self.graph.add_edge(element, node, relation="connects")

        if compas_fea2.VERBOSE:
            print(f"Element {element!r} registered to {self!r}.")

        return element

    def add_elements(self, elements: List[_Element]) -> List[_Element]:
        """Add multiple elements to the part.

        Parameters
        ----------
        elements : List[_Element]

        Returns
        -------
        List[_Element]
        """
        return [self.add_element(element) for element in elements]

    def remove_element(self, element: _Element) -> None:
        """Remove an element from the part.

        Parameters
        ----------
        element : _Element
            The element to remove.

        Warnings
        --------
        Removing elements can cause inconsistencies.
        """
        if self.contains_element(element):
            self.elements.remove(element)
            element._registration = None
            for node in element.nodes:
                node.connected_elements.remove(element)
            if compas_fea2.VERBOSE:
                print(f"Element {element!r} removed from {self!r}.")

    def remove_elements(self, elements: List[_Element]) -> None:
        """Remove multiple elements from the part.

        Parameters
        ----------
        elements : List[_Element]
            List of elements to remove.

        Warnings
        --------
        Removing elements can cause inconsistencies.
        """
        for element in elements:
            self.remove_element(element)

    def is_element_on_boundary(self, element: _Element) -> bool:
        """Check if the element belongs to the boundary mesh of the part.

        Parameters
        ----------
        element : _Element
            The element to check.

        Returns
        -------
        bool
            True if the element is on the boundary, False otherwise.
        """
        from compas.geometry import centroid_points

        if element.on_boundary is None:
            # if not self._discretized_boundary_mesh.face_centroid:
            #     centroid_face = {}
            #     for face in self._discretized_boundary_mesh.faces():
            #         centroid_face[TOL.geometric_key(self._discretized_boundary_mesh.face_centroid(face))] = face
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

    def find_faces_on_plane(self, plane: Plane) -> List["compas_fea2.model.Face"]:
        """Find the faces of the elements that belong to a given plane, if any.

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
        elements_sub_group = self.elements.subgroup(condition=lambda x: isinstance(x, (_Element2D, _Element3D)))
        faces_group = FacesGroup([face for element in elements_sub_group for face in element.faces])
        faces_subgroup = faces_group.subgroup(condition=lambda x: all(is_point_on_plane(node.xyz, plane) for node in x.nodes))
        return faces_subgroup

    def find_faces_in_polygon(self, polygon: "compas.geometry.Polygon", tol: float = 1.1) -> List["compas_fea2.model.Face"]:
        """Find the faces of the elements that are contained within a planar polygon.

        Parameters
        ----------
        polygon : compas.geometry.Polygon
            The polygon for the search.
        tol : float, optional
            Tolerance for the search, by default 1.1.

        Returns
        -------
        :class:`compas_fea2.model.FaceGroup`]
            Subgroup of the faces within the polygon.
        """
        # filter elements with faces
        elements_sub_group = self.elements.subgroup(condition=lambda x: isinstance(x, (_Element2D, _Element3D)))
        faces_group = FacesGroup([face for element in elements_sub_group for face in element.faces])
        # find faces on the plane of the polygon
        if not hasattr(polygon, "plane"):
            try:
                polygon.plane = Frame.from_points(*polygon.points[:3])
            except Exception:
                polygon.plane = Frame.from_points(*polygon.points[-3:])
        faces_subgroup = faces_group.subgroup(condition=lambda face: all(is_point_on_plane(node.xyz, polygon.plane) for node in face.nodes))
        # find faces within the polygon
        S = Scale.from_factors([tol] * 3, polygon.frame)
        T = Transformation.from_frame_to_frame(Frame.from_plane(polygon.plane), Frame.worldXY())
        polygon_xy = polygon.transformed(S)
        polygon_xy = polygon.transformed(T)
        faces_subgroup.subgroup(condition=lambda face: all(is_point_in_polygon_xy(Point(*node.xyz).transformed(T), polygon_xy) for node in face.nodes))
        return faces_subgroup

    def find_boudary_faces(self) -> List["compas_fea2.model.Face"]:
        """Find the boundary faces of the part.

        Returns
        -------
        list[:class:`compas_fea2.model.Face`]
            List with the boundary faces.
        """
        return self.faces.subgroup(condition=lambda x: all(node.on_boundary for node in x.nodes))

    def find_boundary_meshes(self, tol) -> List["compas.datastructures.Mesh"]:
        """Find the boundary meshes of the part.

        Returns
        -------
        list[:class:`compas.datastructures.Mesh`]
            List with the boundary meshes.
        """
        planes = self.extract_clustered_planes(verbose=True)
        submeshes = [Mesh() for _ in planes]
        for element in self.elements:
            for face in element.faces:
                face_points = [node.xyz for node in face.nodes]
                for i, plane in enumerate(planes):
                    if all(is_point_on_plane(point, plane, tol=tol) for point in face_points):
                        submeshes[i].join(face.mesh)
                        break

        print("Welding the boundary meshes...")
        from compas_fea2 import PRECISION

        for submesh in submeshes:
            submesh.weld(PRECISION)
        return submeshes

    # =========================================================================
    #                           Groups methods
    # =========================================================================

    def find_group_by_name(self, name: str) -> List[Union[NodesGroup, ElementsGroup, FacesGroup]]:
        """Find all groups with a given name.

        Parameters
        ----------
        name : str
            The name of the group.

        Returns
        -------
        List[Union[NodesGroup, ElementsGroup, FacesGroup]]
            List of groups with the given name.
        """
        for group in self.groups:
            if group.name == name:
                return group
        print(f"No groups found with name {name}")
        return None

    def add_group(self, group: Union[NodesGroup, ElementsGroup, FacesGroup]) -> Union[NodesGroup, ElementsGroup, FacesGroup]:
        """Add a node or element group to the part.

        Parameters
        ----------
        group : :class:`compas_fea2.model.NodesGroup` | :class:`compas_fea2.model.ElementsGroup` | :class:`compas_fea2.model.FacesGroup`

        Returns
        -------
        :class:`compas_fea2.model.Group`

        Raises
        ------
        TypeError
            If the group is not a node or element group.

        """
        # if self.__class__ not in group.__class__.allowed_registration:
        #     raise TypeError(f"{group.__class__!r} cannot be registered to {self.__class__!r}.")
        group._registration = self
        self._groups.add(group)

    def add_groups(self, groups: List[Union[NodesGroup, ElementsGroup, FacesGroup]]) -> List[Union[NodesGroup, ElementsGroup, FacesGroup]]:
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

    def sorted_nodes_by_displacement(self, step: "_Step", component: str = "length") -> List[Node]:  # noqa: F821
        """Return a list with the nodes sorted by their displacement

        Parameters
        ----------
        step : :class:`compas_fea2.problem._Step`
            The step.
        component : str, optional
            One of ['x', 'y', 'z', 'length'], by default 'length'.

        Returns
        -------
        list[:class:`compas_fea2.model.Node`]
            The nodes sorted by displacement (ascending).

        """
        return self.nodes.sorted_by(lambda n: getattr(Vector(*n.results[step].get("U", None)), component))

    def get_max_displacement(self, problem: "Problem", step: Optional["_Step"] = None, component: str = "length") -> Tuple[Node, float]:  # noqa: F821
        """Retrieve the node with the maximum displacement

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            The problem.
        step : :class:`compas_fea2.problem._Step`, optional
            The step, by default None. If not provided, the last step of the
            problem is used.
        component : str, optional
            One of ['x', 'y', 'z', 'length'], by default 'length'.

        Returns
        -------
        :class:`compas_fea2.model.Node`, float
            The node and the displacement.

        """
        step = step or problem._steps_order[-1]
        node = self.sorted_nodes_by_displacement(step=step, component=component)[-1]
        displacement = getattr(Vector(*node.results[problem][step].get("U", None)), component)
        return node, displacement

    def get_min_displacement(self, problem: "Problem", step: Optional["_Step"] = None, component: str = "length") -> Tuple[Node, float]:  # noqa: F821
        """Retrieve the node with the minimum displacement

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            The problem.
        step : :class:`compas_fea2.problem._Step`, optional
            The step, by default None. If not provided, the last step of the
            problem is used.
        component : str, optional
            One of ['x', 'y', 'z', 'length'], by default 'length'.

        Returns
        -------
        :class:`compas_fea2.model.Node`, float
            The node and the displacement.

        """
        step = step or problem._steps_order[-1]
        node = self.sorted_nodes_by_displacement(step=step, component=component)[0]
        displacement = getattr(Vector(*node.results[problem][step].get("U", None)), component)
        return node, displacement

    def get_average_displacement_at_point(
        self,
        problem: "Problem",  # noqa: F821
        point: List[float],
        distance: float,
        step: Optional["_Step"] = None,  # noqa: F821
        component: str = "length",
        project: bool = False,  # noqa: F821
    ) -> Tuple[List[float], float]:
        """Compute the average displacement around a point

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`
            The problem.
        step : :class:`compas_fea2.problem._Step`, optional
            The step, by default None. If not provided, the last step of the
            problem is used.
        component : str, optional
            One of ['x', 'y', 'z', 'length'], by default 'length'.
        project : bool, optional
            If True, project the point onto the plane, by default False.

        Returns
        -------
        List[float], float
            The point and the average displacement.

        """
        step = step or problem._steps_order[-1]
        nodes = self.find_nodes_around_point(point=point, distance=distance, report=True)
        if nodes:
            displacements = [getattr(Vector(*node.results[problem][step].get("U", None)), component) for node in nodes]
            return point, sum(displacements) / len(displacements)
        return point, 0.0

    # ==============================================================================
    # Viewer
    # ==============================================================================

    def show(self, scale_factor: float = 1, draw_nodes: bool = False, node_labels: bool = False, solid: bool = False):
        """Draw the parts.

        Parameters
        ----------
        scale_factor : float, optional
            Scale factor for the visualization, by default 1.
        draw_nodes : bool, optional
            If `True` draw the nodes of the part, by default False.
        node_labels : bool, optional
            If `True` add the node labels, by default False.
        solid : bool, optional
            If `True` draw all the elements (also the internal ones) of the part
            otherwise just show the boundary faces, by default False.
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


class Part(_Part):
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
        super().__init__(**kwargs)

    @property
    def materials(self) -> Set[_Material]:
        return self._materials
        return set(section.material for section in self.sections if section.material)

    @property
    def sections(self) -> Set[_Section]:
        return self._sections
        return set(element.section for element in self.elements if element.section)

    @property
    def releases(self) -> Set[_BeamEndRelease]:
        return self._releases

    # =========================================================================
    #                       Constructor methods
    # =========================================================================
    @classmethod
    def frame_from_compas_mesh(cls, mesh: "compas.datastructures.Mesh", section: "compas_fea2.model.BeamSection", name: Optional[str] = None, **kwargs) -> "_Part":
        """Creates a Part object from a :class:`compas.datastructures.Mesh`.

        To each edge of the mesh is assigned a :class:`compas_fea2.model.BeamElement`.
        Currently, the same section is applied to all the elements.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            Mesh to convert to a Part.
        section : :class:`compas_fea2.model.BeamSection`
            Section to assign to the frame elements.
        name : str, optional
            Name of the new part.

        Returns
        -------
        _Part
            The part created from the mesh.
        """
        part = cls(name=name, **kwargs)
        vertex_node = {vertex: part.add_node(Node(mesh.vertex_coordinates(vertex))) for vertex in mesh.vertices()}

        for edge in mesh.edges():
            nodes = [vertex_node[vertex] for vertex in edge]
            faces = mesh.edge_faces(edge)
            normals = [mesh.face_normal(f) for f in faces if f is not None]
            if len(normals) == 1:
                normal = normals[0]
            else:
                normal = normals[0] + normals[1]
            direction = list(mesh.edge_direction(edge))
            frame = normal
            frame.rotate(pi / 2, direction, nodes[0].xyz)
            part.add_element(BeamElement(nodes=nodes, section=section, frame=frame))

        return part

    @classmethod
    def from_gmsh(cls, gmshModel: object, section: Union["compas_fea2.model.SolidSection", "compas_fea2.model.ShellSection"], name: Optional[str] = None, **kwargs) -> "_Part":
        """Create a Part object from a gmshModel object.

        Parameters
        ----------
        gmshModel : object
            gmsh Model to convert.
        section : Union[compas_fea2.model.SolidSection, compas_fea2.model.ShellSection]
            Section to assign to the elements.
        name : str, optional
            Name of the new part.

        Returns
        -------
        _Part
            The part created from the gmsh model.
        """
        return super().from_gmsh(gmshModel, section=section, name=name, **kwargs)

    @classmethod
    def from_boundary_mesh(
        cls, boundary_mesh: "compas.datastructures.Mesh", section: Union["compas_fea2.model.SolidSection", "compas_fea2.model.ShellSection"], name: Optional[str] = None, **kwargs
    ) -> "_Part":
        """Create a Part object from a 3-dimensional :class:`compas.datastructures.Mesh`
        object representing the boundary envelope of the Part.

        Parameters
        ----------
        boundary_mesh : :class:`compas.datastructures.Mesh`
            Boundary envelope of the Part.
        section : Union[compas_fea2.model.SolidSection, compas_fea2.model.ShellSection]
            Section to assign to the elements.
        name : str, optional
            Name of the new part.

        Returns
        -------
        _Part
            The part created from the boundary mesh.
        """
        return super().from_boundary_mesh(boundary_mesh, section=section, name=name, **kwargs)

    # =========================================================================
    #                           Releases methods
    # =========================================================================

    def add_beam_release(self, element: BeamElement, location: str, release: _BeamEndRelease) -> _BeamEndRelease:
        """Add a :class:`compas_fea2.model._BeamEndRelease` to an element in the part.

        Parameters
        ----------
        element : :class:`compas_fea2.model.BeamElement`
            The element to release.
        location : str
            'start' or 'end'.
        release : :class:`compas_fea2.model._BeamEndRelease`
            Release type to apply.

        Returns
        -------
        :class:`compas_fea2.model._BeamEndRelease`
            The release applied to the element.
        """
        if not isinstance(release, _BeamEndRelease):
            raise TypeError(f"{release!r} is not a beam release element.")
        release.element = element
        release.location = location
        self._releases.add(release)
        return release


class RigidPart(_Part):
    """Rigid part."""

    __doc__ += _Part.__doc__
    __doc__ += """
    Additional Attributes
    ---------------------
    reference_point : :class:`compas_fea2.model.Node`
        A node acting as a reference point for the part, by default `None`. This
        is required if the part is rigid as it controls its movement in space.

    """

    def __init__(self, reference_point: Optional[Node] = None, **kwargs):
        super().__init__(**kwargs)
        self._reference_point = reference_point

    @property
    def __data__(self):
        data = super().__data__()
        data.update(
            {
                "class": self.__class__.__name__,
                "reference_point": self.reference_point.__data__ if self.reference_point else None,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data):
        """Create a part instance from a data dictionary.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        _Part
            The part instance.
        """
        from compas_fea2.model import Node

        part = cls(reference_point=Node.__from_data__(data["reference_point"]))
        for element_data in data.get("elements", []):
            part.add_element(_Element.__from_data__(element_data))
        return part

    @classmethod
    def from_gmsh(cls, gmshModel: object, name: Optional[str] = None, **kwargs) -> "_Part":
        """Create a RigidPart object from a gmshModel object.

        Parameters
        ----------
        gmshModel : object
            gmsh Model to convert.
        name : str, optional
            Name of the new part.

        Returns
        -------
        _Part
            The part created from the gmsh model.
        """
        kwargs["rigid"] = True
        return super().from_gmsh(gmshModel, name=name, **kwargs)

    @classmethod
    def from_boundary_mesh(cls, boundary_mesh: "compas.datastructures.Mesh", name: Optional[str] = None, **kwargs) -> "_Part":
        """Create a RigidPart object from a 3-dimensional :class:`compas.datastructures.Mesh`
        object representing the boundary envelope of the Part.

        Parameters
        ----------
        boundary_mesh : :class:`compas.datastructures.Mesh`
            Boundary envelope of the RigidPart.
        name : str, optional
            Name of the new part.

        Returns
        -------
        _Part
            The part created from the boundary mesh.
        """
        kwargs["rigid"] = True
        return super().from_boundary_mesh(boundary_mesh, name=name, **kwargs)

    # =========================================================================
    #                        Elements methods
    # =========================================================================
    # TODO this can be removed and the checks on the rigid part can be done in _part

    def add_element(self, element: _Element) -> _Element:
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
