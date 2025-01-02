from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from operator import itemgetter

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import Polygon
from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.itertools import pairwise
from compas.datastructures import Mesh
from compas_occ.brep import Brep
from compas.itertools import pairwise

from compas_fea2.base import FEAData


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
        Identifier based on the conntected nodes.
    section : :class:`compas_fea2.model._Section`
        Section object.
    implementation : str
        The name of the backend model implementation of the element.
    part : :class:`compas_fea2.model.DeformablePart` | None
        The parent part.
    on_boundary : bool | None
        `True` it the element has a face on the boundary mesh of the part, `False`
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

    # FIXME frame and orientations are a bit different concepts. find a way to unify them

    def __init__(self, nodes, section, implementation=None, rigid=False, **kwargs):
        super(_Element, self).__init__(**kwargs)
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
    def part(self):
        return self._registration

    @property
    def model(self):
        return self.part.model

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = self._check_nodes(value)

    @property
    def nodes_key(self):
        return "-".join(sorted([str(node.key) for node in self.nodes], key=int))

    @property
    def nodes_inputkey(self):
        return "-".join(sorted([str(node.input_key) for node in self.nodes], key=int))

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        if self.part:
            self.part.add_section(value)
        self._section = value

    @property
    def frame(self):
        raise NotImplementedError()

    @property
    def implementation(self):
        return self._implementation

    @property
    def on_boundary(self):
        return self._on_boundary

    @on_boundary.setter
    def on_boundary(self, value):
        self._on_boundary = value

    def _check_nodes(self, nodes):
        if len(set([node._registration for node in nodes])) != 1:
            raise ValueError("At least one of node is registered to a different part or not registered")
        return nodes

    @property
    def area(self):
        raise NotImplementedError()

    @property
    def volume(self):
        raise NotImplementedError()

    @property
    def results_format(self):
        raise NotImplementedError()

    @property
    def reference_point(self):
        raise NotImplementedError()

    @property
    def rigid(self):
        return self._rigid

    @property
    def weight(self):
        return self.volume * self.section.material.density

    @property
    def shape(self):
        return self._shape


# ==============================================================================
# 0D elements
# ==============================================================================


# TODO: remove. This is how abaqus does it but it is better to define the mass as a property of the nodes.
class MassElement(_Element):
    """A 0D element for concentrated point mass."""


class _Element0D(_Element):
    """Element with 1 dimension."""

    def __init__(self, nodes, frame, implementation=None, rigid=False, **kwargs):
        super(_Element0D, self).__init__(nodes, section=None, implementation=implementation, rigid=rigid, **kwargs)
        self._frame = frame


class SpringElement(_Element0D):
    """A 0D spring element.
    """
    def __init__(self, nodes, section, implementation=None, rigid=False, **kwargs):
        super(_Element0D, self).__init__(nodes, section=section, implementation=implementation, rigid=rigid, **kwargs)

class LinkElement(_Element0D):
    """A 0D link element.
    """
    def __init__(self, nodes, section, implementation=None, rigid=False, **kwargs):
        super(_Element0D, self).__init__(nodes, section=section, implementation=implementation, rigid=rigid, **kwargs)

# ==============================================================================
# 1D elements
# ==============================================================================
class _Element1D(_Element):
    """Element with 1 dimension."""

    def __init__(self, nodes, section, frame=None, implementation=None, rigid=False, **kwargs):
        super(_Element1D, self).__init__(nodes, section, implementation=implementation, rigid=rigid, **kwargs)
        self._frame = frame if isinstance(frame, Frame) else Frame(
            nodes[0].point,
            Vector.from_start_end(nodes[0].point, nodes[-1].point),
            Vector(*frame)
            )
        self._curve = Line(nodes[0].point, nodes[-1].point)


        # self._shape = Brep.from_extrusion(curve=self.section._shape, vector=Vector.from_start_end(nodes[0].point, nodes[-1].point), cap_ends=False)
        # Brep.from_extrusion(curve=self.section._shape, vector=Vector.from_start_end(nodes[0].point, nodes[-1].point))
        # self._shape = section._shape  # Box(self.length, self.section._w, self.section._h, frame=Frame(self.nodes[0].point, [1,0,0], [0,1,0]))

    @property
    def outermesh(self):
        self._shape_i = self.section._shape.oriented(self._frame)
        self._shape_j = self._shape_i.translated(Vector.from_start_end(self.nodes[0].point, self.nodes[-1].point))
        #create the outer mesh using the section information
        p = self._shape_i.points
        n = len(p)
        self._outermesh = Mesh.from_vertices_and_faces(
            self._shape_i.points+self._shape_j.points,
            [[p.index(v1), p.index(v2), p.index(v2)+n, p.index(v1)+n] for v1, v2 in pairwise(p)]+[[n-1, 0, n, 2*n-1]]
        )
        # self._outermesh.join(self._shape_i.to_mesh())
        # mj = self._shape_j.to_mesh()
        # mj.flip_cycles()
        # self._outermesh.join(mj, weld=True)
        return self._outermesh

    @property
    def frame(self):
        return self._frame

    @property
    def length(self):
        return distance_point_point(*[node.point for node in self.nodes])

    @property
    def volume(self):
        return self.section.A * self.length


class BeamElement(_Element1D):
    """A 1D element that resists axial, shear, bending and torsion.

    A beam element is a one-dimensional line element in three-dimensional space
    whose stiffness is associated with deformation of the line (the beam's “axis”).
    These deformations consist of axial stretch; curvature change (bending); and,
    in space, torsion.

    """


class TrussElement(_Element1D):
    """A 1D element that resists axial loads."""


class StrutElement(TrussElement):
    """A truss element that resists axial compressive loads."""


class TieElement(TrussElement):
    """A truss element that resists axial tensile loads."""


# ==============================================================================
# 2D elements
# ==============================================================================


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

    def __init__(self, nodes, tag, element=None, **kwargs):
        super(Face, self).__init__(**kwargs)
        self._nodes = nodes
        self._tag = tag
        self._plane = Plane.from_three_points(*[node.xyz for node in nodes[:3]])  # TODO check when more than 3 nodes
        self._registration = element
        self._centroid = centroid_points([node.xyz for node in nodes])

    @property
    def nodes(self):
        return self._nodes

    @property
    def tag(self):
        return self._tag

    @property
    def plane(self):
        return self._plane

    @property
    def element(self):
        return self._registration

    @property
    def polygon(self):
        return Polygon([n.xyz for n in self.nodes])

    @property
    def area(self):
        return self.polygon.area

    @property
    def centroid(self):
        return self._centroid


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

    def __init__(self, nodes, section=None, implementation=None, rigid=False, **kwargs):
        super(_Element2D, self).__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            rigid=rigid,
            **kwargs,
        )

        self._faces = None
        self._face_indices = None

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = self._check_nodes(value)
        self._faces = self._construct_faces(self._face_indices)

    @property
    def face_indices(self):
        return self._face_indices

    @property
    def faces(self):
        return self._faces

    @property
    def volume(self):
        return self._faces[0].area * self.section.t

    @property
    def reference_point(self):
        return centroid_points([face.centroid for face in self.faces])

    def _construct_faces(self, face_indices):
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


class ShellElement(_Element2D):
    """A 2D element that resists axial, shear, bending and torsion.

    Shell elements are used to model structures in which one dimension, the
    thickness, is significantly smaller than the other dimensions.

    """

    def __init__(self, nodes, section=None, implementation=None, rigid=False, **kwargs):
        super(ShellElement, self).__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            rigid=rigid,
            **kwargs,
        )

        self._face_indices = {"SPOS": tuple(range(len(nodes))), "SNEG": tuple(range(len(nodes)))[::-1]}
        self._faces = self._construct_faces(self._face_indices)


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


# ==============================================================================
# 3D elements
# ==============================================================================


# TODO add picture with node lables convention


class _Element3D(_Element):
    """A 3D element that resists axial, shear, bending and torsion.
    Solid (continuum) elements can be used for linear analysis
    and for complex nonlinear analyses involving contact, plasticity, and large
    deformations.

    Solid elements are general purpose elements and can be used for multiphysics
    problems.

    """

    def __init__(self, nodes, section, implementation=None, **kwargs):
        super(_Element3D, self).__init__(
            nodes=nodes,
            section=section,
            implementation=implementation,
            **kwargs,
        )
        self._face_indices = None
        self._faces = None
        self._frame = Frame.worldXY()

    @property
    def frame(self):
        return self._frame

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value
        self._faces = self._construct_faces(self._face_indices)

    @property
    def face_indices(self):
        return self._face_indices

    @property
    def faces(self):
        return self._faces

    @property
    def reference_point(self):
        return centroid_points([face.centroid for face in self.faces])

    def _construct_faces(self, face_indices):
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
    def area(self):
        return self._area

    @classmethod
    def from_polyhedron(cls, polyhedron, section, implementation=None, **kwargs):
        from compas_fea2.model import Node

        element = cls([Node(vertex) for vertex in polyhedron.vertices], section, implementation, **kwargs)
        return element


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

    def __init__(self, *, nodes, section, implementation=None, **kwargs):
        super(TetrahedronElement, self).__init__(
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

    # TODO use compas funcitons to compute differences and det
    @property
    def volume(self):
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

    def __init__(self, nodes, section, implementation=None, **kwargs):
        super(HexahedronElement, self).__init__(
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
