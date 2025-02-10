from operator import itemgetter

from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Vector
from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.itertools import pairwise

import compas_fea2
from compas_fea2.base import FEAData

from compas_fea2.results import Result
from compas_fea2.results import ShellStressResult
from compas_fea2.results import SolidStressResult


class _Element(FEAData):
    """Initialises a base Element object.

    Parameters
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        Ordered list of node identifiers to which the element connects.
    section : :class:`compas_fea2.model._Section`
        Section Object assigned to the element.
    implementation : str, optional
        The name of the backend model implementation of the element.

    Attributes
    ----------
    key : int, read-only
        Identifier of the element in the parent part.
    nodes : list[:class:`compas_fea2.model.Node`]
        Nodes to which the element is connected.
    nodes_key : str, read-only
        Identifier based on the connected nodes.
    section : :class:`compas_fea2.model._Section`
        Section object.
    implementation : str
        The name of the backend model implementation of the element.
    part : :class:`compas_fea2.model.Part` | None
        The parent part.
    on_boundary : bool | None
        `True` if the element has a face on the boundary mesh of the part, `False`
        otherwise, by default `None`.
    part : :class:`compas_fea2.model._Part`, read-only
        The Part where the element is assigned.
    model : :class:`compas_fea2.model.Model`, read-only
        The Model where the element is assigned.
    area : float, read-only
        The area of the element.
    volume : float, read-only
        The volume of the element.
    rigid : bool, read-only
        Define the element as rigid (no deformations allowed) or not. For Rigid
        elements sections are not needed.

    Notes
    -----
    Elements and their nodes are registered to the same :class:`compas_fea2.model._Part` and can belong to only one Part.

    Warnings
    --------
    When an Element is added to a Part, the nodes of the elements are also added
    and registered to the same part. This might change the original registration
    of the nodes!

    """

    def __init__(self, nodes: List["Node"], section: "_Section", implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(**kwargs)
        self._part_key = None
        self._nodes = self._check_nodes(nodes)
        self._registration = nodes[0]._registration
        self._section = section
        self._implementation = implementation
        self._frame = None
        self._on_boundary = None
        self._area = None
        self._volume = None
        self._results_format = {}
        self._rigid = rigid
        self._reference_point = None
        self._shape = None

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__,
            "nodes": [node.__data__ for node in self.nodes],
            "section": self.section.__data__,
            "implementation": self.implementation,
            "rigid": self.rigid,
        }

    @classmethod
    def __from_data__(cls, data):
        nodes = [node_data.pop("class").__from_data__(node_data) for node_data in data["nodes"]]
        section = data["section"].pop("class").__from_data__(data["section"])
        return cls(nodes, section, implementation=data.get("implementation"), rigid=data.get("rigid"))

    @property
    def part(self) -> "_Part":  # noqa: F821
        return self._registration

    @property
    def model(self) -> "Model":  # noqa: F821
        return self.part.model

    @property
    def results_cls(self) -> Result:
        raise NotImplementedError("The results_cls property must be implemented in the subclass")

    @property
    def nodes(self) -> List["Node"]:  # noqa: F821
        return self._nodes

    @nodes.setter
    def nodes(self, value: List["Node"]):  # noqa: F821
        self._nodes = self._check_nodes(value)

    @property
    def nodes_key(self) -> str:
        return [n.part_key for n in self.nodes]

    @property
    def nodes_inputkey(self) -> str:
        return "-".join(sorted([str(node.input_key) for node in self.nodes], key=int))

    @property
    def points(self) -> List["Point"]:
        return [node.point for node in self.nodes]

    @property
    def section(self) -> "_Section":  # noqa: F821
        return self._section

    @section.setter
    def section(self, value: "_Section"):  # noqa: F821
        self._section = value

    @property
    def frame(self) -> Optional[Frame]:
        return self._frame

    @property
    def implementation(self) -> Optional[str]:
        return self._implementation

    @property
    def on_boundary(self) -> Optional[bool]:
        return self._on_boundary

    @on_boundary.setter
    def on_boundary(self, value: bool):
        self._on_boundary = value

    def _check_nodes(self, nodes: List["Node"]) -> List["Node"]:  # noqa: F821
        if len(set([node._registration for node in nodes])) != 1:
            raise ValueError("At least one of node is registered to a different part or not registered")
        return nodes

    @property
    def part_key(self) -> int:
        return self._part_key

    @property
    def area(self) -> float:
        raise NotImplementedError()

    @property
    def volume(self) -> float:
        raise NotImplementedError()

    @property
    def results_format(self) -> Dict:
        raise NotImplementedError()

    @property
    def reference_point(self) -> "Point":
        raise NotImplementedError()

    @property
    def rigid(self) -> bool:
        return self._rigid

    @property
    def mass(self) -> float:
        return self.volume * self.section.material.density

    def weight(self, g: float) -> float:
        return self.mass * g

    @property
    def nodal_mass(self) -> List[float]:
        return [self.mass / len(self.nodes)] * 3

    @property
    def ndim(self) -> int:
        return self._ndim


class MassElement(_Element):
    """A 0D element for concentrated point mass."""

    @property
    def __data__(self):
        data = super().__data__
        return data

    @classmethod
    def __from_data__(cls, data):
        element = super().__from_data__(data)
        return element


class _Element0D(_Element):
    """Element with 1 dimension."""

    def __init__(self, nodes: List["Node"], frame: Frame, implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(nodes, section=None, implementation=implementation, rigid=rigid, **kwargs)
        self._frame = frame
        self._ndim = 0

    @property
    def __data__(self):
        data = super().__data__()
        data["frame"] = self.frame.__data__
        return data


class SpringElement(_Element0D):
    """A 0D spring element.

    Notes
    -----
    Link elements are used within a part. If you want to connect nodes from different parts
    use :class:`compas_fea2.model.connectors.RigidLinkConnector`.

    """

    def __init__(self, nodes: List["Node"], section: "_Section", implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(nodes, section=section, implementation=implementation, rigid=rigid, **kwargs)


class LinkElement(_Element0D):
    """A 0D link element.

    Notes
    -----
    Link elements are used within a part. If you want to connect nodes from different parts
    use :class:`compas_fea2.model.connectors.RigidLinkConnector`.
    """

    def __init__(self, nodes: List["Node"], section: "_Section", implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(nodes, section=section, implementation=implementation, rigid=rigid, **kwargs)


class _Element1D(_Element):
    """Element with 1 dimension.

    Parameters
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        Ordered list of nodes to which the element connects.
    section : :class:`compas_fea2.model._Section`
        Section Object assigned to the element.
    frame : :class:`compas.geometry.Frame` or list
        Frame or local X axis in global coordinates. This is used to define the section orientation.
    implementation : str, optional
        The name of the backend model implementation of the element.
    rigid : bool, optional
        Define the element as rigid (no deformations allowed) or not. For Rigid
        elements sections are not needed.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The frame of the element.
    length : float
        The length of the element.
    volume : float
        The volume of the element.
    """

    def __init__(self, nodes: List["Node"], section: "_Section", frame: Optional[Frame] = None, implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(nodes, section, implementation=implementation, rigid=rigid, **kwargs)
        if not frame:
            raise ValueError("Frame is required for 1D elements")
        self._frame = frame if isinstance(frame, Frame) else Frame(nodes[0].point, Vector(*frame), Vector.from_start_end(nodes[0].point, nodes[-1].point))
        self._ndim = 1

    @property
    def __data__(self):
        data = super().__data__
        data["frame"] = self.frame.__data__
        return data

    @classmethod
    def __from_data__(cls, data):
        nodes = [node_data.pop("class").__from_data__(node_data) for node_data in data["nodes"]]
        section = data["section"].pop("class").__from_data__(data["section"])
        frame = Frame.__from_data__(data["frame"])
        return cls(nodes=nodes, section=section, frame=frame, implementation=data.get("implementation"), rigid=data.get("rigid"))

    @property
    def curve(self) -> Line:
        return Line(self.nodes[0].point, self.nodes[-1].point)

    @property
    def outermesh(self) -> Mesh:
        self._frame.point = self.nodes[0].point
        self._shape_i = self.section._shape.oriented(self._frame, check_planarity=False)
        self._shape_j = self._shape_i.translated(Vector.from_start_end(self.nodes[0].point, self.nodes[-1].point), check_planarity=False)
        p = self._shape_i.points
        n = len(p)
        self._outermesh = Mesh.from_vertices_and_faces(
            self._shape_i.points + self._shape_j.points, [[p.index(v1), p.index(v2), p.index(v2) + n, p.index(v1) + n] for v1, v2 in pairwise(p)] + [[n - 1, 0, n, 2 * n - 1]]
        )
        return self._outermesh

    @property
    def frame(self) -> Frame:
        return self._frame

    @property
    def shape(self) -> Optional["Shape"]:  # noqa: F821
        return self._shape

    @property
    def length(self) -> float:
        return distance_point_point(*[node.point for node in self.nodes])

    @property
    def volume(self) -> float:
        return self.section.A * self.length

    def plot_section(self):
        self.section.plot()

    def plot_stress_distribution(self, step: "_Step", end: str = "end_1", nx: int = 100, ny: int = 100, *args, **kwargs):  # noqa: F821
        if not hasattr(step, "section_forces_field"):
            raise ValueError("The step does not have a section_forces_field")
        r = step.section_forces_field.get_element_forces(self)
        r.plot_stress_distribution(*args, **kwargs)

    def section_forces_result(self, step: "Step") -> "Result":  # noqa: F821
        if not hasattr(step, "section_forces_field"):
            raise ValueError("The step does not have a section_forces_field")
        return step.section_forces_field.get_result_at(self)

    def forces(self, step: "Step") -> "Result":  # noqa: F821
        r = self.section_forces_result(step)
        return r.forces

    def moments(self, step: "_Step") -> "Result":  # noqa: F821
        r = self.section_forces_result(step)
        return r.moments


class BeamElement(_Element1D):
    """A 1D element that resists axial, shear, bending and torsion.

    A beam element is a one-dimensional line element in three-dimensional space
    whose stiffness is associated with deformation of the line (the beam's “axis”).
    These deformations consist of axial stretch; curvature change (bending); and,
    in space, torsion.

    """


class TrussElement(_Element1D):
    """A 1D element that resists axial loads."""

    def __init__(self, nodes: List["Node"], section: "_Section", implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(nodes, section, frame=[1, 1, 1], implementation=implementation, rigid=rigid, **kwargs)


class StrutElement(TrussElement):
    """A truss element that resists axial compressive loads."""


class TieElement(TrussElement):
    """A truss element that resists axial tensile loads."""


class Face(FEAData):
    """Element representing a face.

    Parameters
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        Ordered list of nodes to which the element connects.
    tag : str
        The tag of the face.
    element : :class:`compas_fea2.model._Element`
        The element to which the face belongs.

    Attributes
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        Nodes to which the element is connected.
    tag : str
        The tag of the face.
    element : :class:`compas_fea2.model._Element`
        The element to which the face belongs.
    plane : :class:`compas.geometry.Plane`
        The plane of the face.
    polygon : :class:`compas.geometry.Polygon`
        The polygon of the face.
    area : float
        The area of the face.
    results : dict
        Dictionary with results of the face.

    """

    def __init__(self, nodes: List["Node"], tag: str, element: Optional["_Element"] = None, **kwargs):  # noqa: F821
        super().__init__(**kwargs)
        self._nodes = nodes
        self._tag = tag
        self._plane = Plane.from_three_points(*[node.xyz for node in nodes[:3]])  # TODO check when more than 3 nodes
        self._registration = element
        self._centroid = centroid_points([node.xyz for node in nodes])

    @property
    def __data__(self):
        return {
            "nodes": [node.__data__ for node in self.nodes],
            "tag": self.tag,
            "element": self.element.__data__ if self.element else None,
        }

    @classmethod
    def __from_data__(cls, data):
        from compas_fea2.model import Node
        from importlib import import_module

        elements_module = import_module("compas_fea2.model.elements")
        element_cls = getattr(elements_module, data["elements"]["class"])

        nodes = [Node.__from_data__(node_data) for node_data in data["nodes"]]
        element = element_cls[data["element"]["class"]].__from_data__(data["element"])
        return cls(nodes, data["tag"], element=element)

    @property
    def nodes(self) -> List["Node"]:  # noqa: F821
        return self._nodes

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def plane(self) -> Plane:
        return self._plane

    @property
    def element(self) -> Optional["_Element"]:
        return self._registration

    @property
    def polygon(self) -> Polygon:
        return Polygon([n.xyz for n in self.nodes])

    @property
    def area(self) -> float:
        return self.polygon.area

    @property
    def centroid(self) -> "Point":
        return self._centroid

    @property
    def nodes_key(self) -> List:
        return [n._part_key for n in self.nodes]

    @property
    def normal(self) -> Vector:
        return self.plane.normal

    @property
    def points(self) -> List["Point"]:
        return [node.point for node in self.nodes]

    @property
    def mesh(self) -> Mesh:
        return Mesh.from_vertices_and_faces(self.points, [[c for c in range(len(self.points))]])


class _Element2D(_Element):
    """Element with 2 dimensions."""

    __doc__ += _Element.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    faces : [:class:`compas_fea2.model.elements.Face]
        The faces of the element.
    face_indices : dict
        Dictionary providing for each face the node indices. For example:
        {'s1': (0,1,2), ...}
    """

    def __init__(self, nodes: List["Node"], section: Optional["_Section"] = None, implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            rigid=rigid,
            **kwargs,
        )

        self._faces = None
        self._face_indices = None
        self._ndim = 2

    @property
    def nodes(self) -> List["Node"]:  # noqa: F821
        return self._nodes

    @nodes.setter
    def nodes(self, value: List["Node"]):  # noqa: F821
        self._nodes = self._check_nodes(value)
        self._faces = self._construct_faces(self._face_indices)

    @property
    def face_indices(self) -> Optional[Dict[str, Tuple[int]]]:
        return self._face_indices

    @property
    def faces(self) -> Optional[List[Face]]:
        return self._faces

    @property
    def volume(self) -> float:
        return self._faces[0].area * self.section.t

    @property
    def reference_point(self) -> "Point":
        return centroid_points([face.centroid for face in self.faces])

    @property
    def outermesh(self) -> Mesh:
        return Mesh.from_vertices_and_faces(self.points, list(self._face_indices.values()))

    def _construct_faces(self, face_indices: Dict[str, Tuple[int]]) -> List[Face]:
        """Construct the face-nodes dictionary.

        Parameters
        ----------
        face_indices : dict
            Dictionary providing for each face the node indices. For example:
            {'s1': (0,1,2), ...}

        Returns
        -------
        dict
            Dictionary with face names and the corresponding nodes.
        """
        return [Face(nodes=itemgetter(*indices)(self.nodes), tag=name, element=self) for name, indices in face_indices.items()]

    def stress_results(self, step: "_Step") -> "Result":  # noqa: F821
        if not hasattr(step, "stress_field"):
            raise ValueError("The step does not have a stress field")
        return step.stress_field.get_result_at(self)


class ShellElement(_Element2D):
    """A 2D element that resists axial, shear, bending and torsion.

    Shell elements are used to model structures in which one dimension, the
    thickness, is significantly smaller than the other dimensions.

    """

    def __init__(self, nodes: List["Node"], section: Optional["_Section"] = None, implementation: Optional[str] = None, rigid: bool = False, **kwargs):  # noqa: F821
        super().__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            rigid=rigid,
            **kwargs,
        )

        self._face_indices = {"SPOS": tuple(range(len(nodes))), "SNEG": tuple(range(len(nodes)))[::-1]}
        self._faces = self._construct_faces(self._face_indices)

    @property
    def results_cls(self) -> Result:
        return {"s": ShellStressResult}


class MembraneElement(_Element2D):
    """A shell element that resists only axial loads.

    Notes
    -----
    Membrane elements are used to represent thin surfaces in space that offer
    strength in the plane of the element but have no bending stiffness; for
    example, the thin rubber sheet that forms a balloon. In addition, they are
    often used to represent thin stiffening components in solid structures, such
    as a reinforcing layer in a continuum.

    """


class _Element3D(_Element):
    """A 3D element that resists axial, shear, bending and torsion.
    Solid (continuum) elements can be used for linear analysis
    and for complex nonlinear analyses involving contact, plasticity, and large
    deformations.

    Solid elements are general purpose elements and can be used for multiphysics
    problems.

    """

    def __init__(self, nodes: List["Node"], section: "_Section", implementation: Optional[str] = None, **kwargs):  # noqa: F821
        super().__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            **kwargs,
        )
        self._face_indices = None
        self._faces = None
        self._frame = Frame.worldXY()
        self._ndim = 3

    @property
    def results_cls(self) -> Result:
        return {"s": SolidStressResult}

    @property
    def frame(self) -> Frame:
        return self._frame

    @property
    def nodes(self) -> List["Node"]:  # noqa: F821
        return self._nodes

    @nodes.setter
    def nodes(self, value: List["Node"]):  # noqa: F821
        self._nodes = value
        self._faces = self._construct_faces(self._face_indices)

    @property
    def face_indices(self) -> Optional[Dict[str, Tuple[int]]]:
        return self._face_indices

    @property
    def faces(self) -> Optional[List[Face]]:
        return self._faces

    @property
    def edges(self):
        seen = set()
        for _, face in self._faces.itmes():
            for u, v in pairwise(face + face[:1]):
                if (u, v) not in seen:
                    seen.add((u, v))
                    seen.add((v, u))
                    yield u, v

    @property
    def centroid(self) -> "Point":
        return centroid_points([node.point for node in self.nodes])

    @property
    def reference_point(self) -> "Point":
        return self._reference_point or self.centroid

    def _construct_faces(self, face_indices: Dict[str, Tuple[int]]) -> List[Face]:
        """Construct the face-nodes dictionary.

        Parameters
        ----------
        face_indices : dict
            Dictionary providing for each face the node indices. For example:
            {'s1': (0,1,2), ...}

        Returns
        -------
        dict
            Dictionary with face names and the corresponding nodes.

        """
        return [Face(nodes=itemgetter(*indices)(self.nodes), tag=name, element=self) for name, indices in face_indices.items()]

    @property
    def area(self) -> float:
        return self._area

    @classmethod
    def from_polyhedron(cls, polyhedron: Polyhedron, section: "_Section", implementation: Optional[str] = None, **kwargs) -> "_Element3D":  # noqa: F821
        from compas_fea2.model import Node

        element = cls([Node(vertex) for vertex in polyhedron.vertices], section, implementation, **kwargs)
        return element

    @property
    def outermesh(self) -> Mesh:
        return Polyhedron(self.points, list(self._face_indices.values())).to_mesh()


class TetrahedronElement(_Element3D):
    """A Solid element with 4 faces.

    Notes
    -----
    The face labels are as follows:

    - S1: (0, 1, 2)
    - S2: (0, 1, 3)
    - S3: (1, 2, 3)
    - S4: (0, 2, 3)

    where the number is the index of the the node in the nodes list

    """

    def __init__(self, *, nodes: List["Node"], section: "_Section", implementation: Optional[str] = None, **kwargs):  # noqa: F821
        super().__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            **kwargs,
        )
        self._face_indices = {"s1": (0, 1, 2), "s2": (0, 1, 3), "s3": (1, 2, 3), "s4": (0, 2, 3)}
        self._faces = self._construct_faces(self._face_indices)

    @property
    def edges(self):
        seen = set()
        for _, face in self._faces.itmes():
            for u, v in pairwise(face + face[:1]):
                if (u, v) not in seen:
                    seen.add((u, v))
                    seen.add((v, u))
                    yield u, v

    @property
    def volume(self) -> float:
        """The volume property."""

        def determinant_3x3(m):
            return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[1][0] * (m[0][1] * m[2][2] - m[0][2] * m[2][1]) + m[2][0] * (m[0][1] * m[1][2] - m[0][2] * m[1][1])

        def subtract(a, b):
            return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

        nodes_coord = [node.xyz for node in self.nodes]
        a, b, c, d = nodes_coord
        return (
            abs(
                determinant_3x3(
                    (
                        subtract(a, b),
                        subtract(b, c),
                        subtract(c, d),
                    )
                )
            )
            / 6.0
        )


class PentahedronElement(_Element3D):
    """A Solid element with 5 faces (extruded triangle)."""


class HexahedronElement(_Element3D):
    """A Solid cuboid element with 6 faces (extruded rectangle)."""

    def __init__(self, nodes: List["Node"], section: "_Section", implementation: Optional[str] = None, **kwargs):  # noqa: F821
        super().__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            **kwargs,
        )
        self._faces_indices = {
            "s1": (0, 1, 2, 3),
            "s2": (4, 5, 6, 7),
            "s3": (0, 1, 4, 5),
            "s4": (1, 2, 5, 6),
            "s5": (2, 3, 6, 7),
            "s6": (0, 3, 4, 7),
        }
        self._faces = self._construct_faces(self._face_indices)
