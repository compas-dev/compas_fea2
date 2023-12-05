from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from operator import itemgetter

from compas.geometry import Frame
from compas.geometry import Plane
from compas.utilities import pairwise
from compas.geometry import Polygon

from compas_fea2.base import FEAData


class Element(FEAData):
    """Initialises a base Element object.

    Parameters
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        Ordered list of node identifiers to which the element connects.
    section : :class:`compas_fea2.model._Section`
        Section Object assigned to the element.
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system for property assignement.
        Default to the global coordinate system.
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
    frame : :class:`compas.geometry.Frame`
        The local coordinate system for property assignement.
        Default to the global coordinate system.
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

    def __init__(self, nodes, section, frame=None, implementation=None, **kwargs):
        super(Element, self).__init__(**kwargs)
        self._nodes = self._check_nodes(nodes)
        self._registration = nodes[0]._registration
        self._section = section
        self._frame = frame
        self._implementation = implementation
        self._on_boundary = None
        self._key = None
        self._area = None
        self._volume = None
        self._results = {}
        self._rigid = False

    @property
    def part(self):
        return self._registration

    @property
    def model(self):
        return self.part._registration

    @property
    def key(self):
        return self._key

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
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        self._section = value

    @property
    def frame(self):
        if self._frame is None:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

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
    def results(self):
        return self._results

    @property
    def rigid(self):
        return self._rigid


# ==============================================================================
# 0D elements
# ==============================================================================


class MassElement(Element):
    """A 0D element for concentrated point mass."""


# ==============================================================================
# 1D elements
# ==============================================================================


class Element1D(Element):
    """Element with 1 dimension."""


class BeamElement(Element1D):
    """A 1D element that resists axial, shear, bending and torsion.

    A beam element is a one-dimensional line element in three-dimensional space
    whose stiffness is associated with deformation of the line (the beam's “axis”).
    These deformations consist of axial stretch; curvature change (bending); and,
    in space, torsion.

    """


class SpringElement(Element1D):
    """A 1D spring element."""


class TrussElement(Element1D):
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
        Ordered list of node identifiers to which the element connects.
    tag : str
        The tag of the face.
    element : :class:`compas_fea2.model.Element`
        The element to which the face belongs.

    Attributes
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        Nodes to which the element is connected.
    tag : str
        The tag of the face.
    element : :class:`compas_fea2.model.Element`
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
        self._results = {}

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
    def results(self):
        return self._results

    @property
    def polygon(self):
        return Polygon([n.xyz for n in self.nodes])

    @property
    def area(self):
        return self.polygon.area


class Element2D(Element):
    """Element with 2 dimensions.

    Parameters
    ----------
    faces : [:class:`compas_fea2.model.elements.Face]
        The faces of the element.
    faces : dict
        Dictionary providing for each face the node indices. For example:
        {'s1': (0,1,2), ...}

    """

    def __init__(self, nodes, frame, section=None, implementation=None, rigid=False, **kwargs):
        super(Element2D, self).__init__(
            nodes=nodes,
            section=section,
            frame=frame,
            implementation=implementation,
            **kwargs,
        )

        self._faces = None
        self._face_indices = None
        self._rigid = rigid
        self._implementation = implementation

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
    def volume(self):
        return self._faces[0].area * self.section.t

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
        return [
            Face(nodes=itemgetter(*indices)(self.nodes), tag=name, element=self)
            for name, indices in face_indices.items()
        ]


class ShellElement(Element2D):
    """A 2D element that resists axial, shear, bending and torsion.

    Shell elements are used to model structures in which one dimension, the
    thickness, is significantly smaller than the other dimensions.

    """

    def __init__(self, nodes, frame=None, section=None, implementation=None, rigid=False, **kwargs):
        super(ShellElement, self).__init__(
            nodes=nodes,
            frame=frame,
            section=section,
            implementation=implementation,
            rigid=rigid,
            **kwargs,
        )

        self._face_indices = {"SPOS": tuple(range(len(nodes))), "SNEG": tuple(range(len(nodes)))[::-1]}
        self._faces = self._construct_faces(self._face_indices)


class MembraneElement(Element2D):
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


class Element3D(Element):
    """A 3D element that resists axial, shear, bending and torsion.
    Solid (continuum) elements can be used for linear analysis
    and for complex nonlinear analyses involving contact, plasticity, and large
    deformations.

    Solid elements are general purpose elements and can be used for multiphysics
    problems.

    """

    def __init__(self, nodes, section, implementation=None, **kwargs):
        super(Element3D, self).__init__(
            nodes=nodes,
            section=section,
            frame=None,
            implementation=implementation,
            **kwargs,
        )
        self._face_indices = None
        self._faces = None

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
        return [
            Face(nodes=itemgetter(*indices)(self.nodes), tag=name, element=self)
            for name, indices in face_indices.items()
        ]

    @property
    def area(self):
        return self._area

    @classmethod
    def from_polyhedron(cls, polyhedron, section, implementation=None, **kwargs):
        from compas_fea2.model import Node

        element = cls([Node(vertex) for vertex in polyhedron.vertices], section, implementation, **kwargs)
        return element


class TetrahedronElement(Element3D):
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
            return (
                m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[1][0] * (m[0][1] * m[2][2] - m[0][2] * m[2][1])
                + m[2][0] * (m[0][1] * m[1][2] - m[0][2] * m[1][1])
            )

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


class PentahedronElement(Element3D):
    """A Solid element with 5 faces (extruded triangle)."""


class HexahedronElement(Element3D):
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
