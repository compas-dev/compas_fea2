from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from operator import itemgetter

from compas.geometry import Frame
from compas.geometry import Plane
from compas_fea2.base import FEAData

import compas_fea2
from compas.utilities import pairwise


class _Element(FEAData):
    """Initialises a base Element object.

    Note
    ----
    Elements are registered to the same :class:`compas_fea2.model.DeformablePart` as its nodes
    and can belong to only one DeformablePart.

    Warning
    -------
    When an Element is added to a DeformablePart, the nodes of the elements are also added
    and registered to the same part. This might change the original registration
    of the nodes!

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
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
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
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
    implementation : str, optional
        The name of the backend model implementation of the element.
    part : :class:`compas_fea2.model.DeformablePart` | None
        The parent part.
    on_boundary : bool | None
        `True` it the element has a face on the boundary mesh of the part, `False`
        otherwise, by default `None`.

    """
# FIXME frame and orientations are a bit different concepts. find a way to unify them

    def __init__(self, *, nodes, section, frame=None, implementation=None, name=None, **kwargs):
        super(_Element, self).__init__(name, **kwargs)
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
        return '-'.join(sorted([str(node.key) for node in self.nodes], key=int))

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
            raise ValueError('At least one of node is registered to a different part or not registered')
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

# ==============================================================================
# 0D elements
# ==============================================================================


class MassElement(_Element):
    """A 0D element for concentrated point mass.
    """


# ==============================================================================
# 1D elements
# ==============================================================================
class _Element1D(_Element):
    """
    """


class BeamElement(_Element1D):
    """A 1D element that resists axial, shear, bending and torsion.

    A beam element is a one-dimensional line element in three-dimensional space
    whose stiffness is associated with deformation of the line (the beam's “axis”).
    These deformations consist of axial stretch; curvature change (bending); and,
    in space, torsion.

    """


class SpringElement(_Element1D):
    """A 1D spring element.
    """


class TrussElement(_Element1D):
    """A 1D element that resists axial loads.
    """


class StrutElement(TrussElement):
    """A truss element that resists axial compressive loads.
    """


class TieElement(TrussElement):
    """A truss element that resists axial tensile loads.
    """


# ==============================================================================
# 2D elements
# ==============================================================================
class _Element2D(_Element):
    """
    """

    def __init__(self, *, nodes, frame, section=None, implementation=None, rigid=False, name=None, **kwargs):
        super(_Element2D, self).__init__(nodes=nodes, section=section,
                                         frame=frame, implementation=implementation, name=name, **kwargs)

        self._face_indices = None
        self._faces = None


        self._rigid = rigid
        if not section and not rigid:
            raise TypeError('A not-rigid element must have a section')
        if section and rigid:
            raise TypeError('A rigid element cannot have a section')

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
        return [Face(nodes=itemgetter(*indices)(self.nodes), tag=name, element=self) for name, indices in face_indices.items()]

    @property
    def rigid(self):
        return self._rigid



class ShellElement(_Element2D):
    """A 2D element that resists axial, shear, bending and torsion.

    Shell elements are used to model structures in which one dimension, the
    thickness, is significantly smaller than the other dimensions.

    """

    def __init__(self, *, nodes, frame=None, section=None, implementation=None, rigid=False, name=None, **kwargs):
        super(ShellElement, self).__init__(nodes=nodes, frame=frame, section=section,
                                           implementation=implementation, rigid=rigid, name=name, **kwargs)

        self._face_indices = {
            'SPOS': tuple(range(len(nodes))),
            'SNEG': tuple(range(len(nodes)))[::-1]
        }
        self._faces = self._construct_faces(self._face_indices)


class MembraneElement(_Element2D):
    """A shell element that resists only axial loads.

    Note
    ----
    Membrane elements are used to represent thin surfaces in space that offer
    strength in the plane of the element but have no bending stiffness; for
    example, the thin rubber sheet that forms a balloon. In addition, they are
    often used to represent thin stiffening components in solid structures, such
    as a reinforcing layer in a continuum.

    """


# ==============================================================================
# 3D elements
# ==============================================================================

class Face(FEAData):
    """_summary_

    Parameters
    ----------
    FEAData : _type_
        _description_
    """
    def __init__(self, *, nodes, tag, element=None, name=None):
        super(Face, self).__init__(name)
        self._nodes = nodes
        self._tag = tag
        self._plane = Plane.from_three_points(*[node.xyz for node in nodes])  # TODO check when more than 3 nodes
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

# TODO add picture with node lables convention


class _Element3D(_Element):
    """A 3D element that resists axial, shear, bending and torsion.
    Solid (continuum) elements can be used for linear analysis
    and for complex nonlinear analyses involving contact, plasticity, and large
    deformations.

    Solid elements are general purpose elements and can be used for multiphysics
    problems.

    """

    def __init__(self, *, nodes, section, implementation=None, name=None, **kwargs):
        super(_Element3D, self).__init__(nodes=nodes, section=section, frame=None,
                                         implementation=implementation, name=name, **kwargs)
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
        return [Face(nodes=itemgetter(*indices)(self.nodes), tag=name, element=self) for name, indices in face_indices.items()]

    @property
    def area(self):
        return self._area

    @classmethod
    def from_polyhedron(cls, polyhedron, section, implementation=None, name=None, **kwargs):
        # m = importlib.import_module('.'.join(cls.__module__.split('.')[:-1]))
        from compas_fea2.model import Node
        element = cls([Node(vertex) for vertex in polyhedron.vertices], section, implementation, name, **kwargs)
        return element


class TetrahedronElement(_Element3D):
    """A Solid element with 4 faces.

    Note
    ----
    The face labels are as follows:
        - S1: (0, 1, 2)
        - S2: (0, 1, 3)
        - S3: (1, 2, 3)
        - S4: (0, 2, 3)

    where the number is the index of the the node in the nodes list
    """

    def __init__(self, *, nodes, section, implementation=None, name=None, **kwargs):
        super(TetrahedronElement, self).__init__(nodes=nodes, section=section,
                                                 implementation=implementation, name=name, **kwargs)
        self._face_indices = {
            's1': (0, 1, 2),
            's2': (0, 1, 3),
            's3': (1, 2, 3),
            's4': (0, 2, 3)
        }
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

    #TODO use compas funcitons to compute differences and det
    @property
    def volume(self):
        """The volume property."""

        def determinant_3x3(m):
            return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
                    m[1][0] * (m[0][1] * m[2][2] - m[0][2] * m[2][1]) +
                    m[2][0] * (m[0][1] * m[1][2] - m[0][2] * m[1][1]))


        def subtract(a, b):
            return (a[0] - b[0],
                    a[1] - b[1],
                    a[2] - b[2])

        nodes_coord = [node.xyz for node in self.nodes]
        a, b, c ,d = nodes_coord
        return abs(determinant_3x3((subtract(a, b),
                                    subtract(b, c),
                                    subtract(c, d),
                                    ))) / 6.0

class PentahedronElement(_Element3D):
    """A Solid element with 5 faces (extruded triangle).
    """


class HexahedronElement(_Element3D):
    """A Solid cuboid element with 6 faces (extruded rectangle).
    """

    def __init__(self, *, nodes, section, implementation=None, name=None, **kwargs):
        super(HexahedronElement, self).__init__(nodes=nodes, section=section,
                                                implementation=implementation, name=name, **kwargs)
        self._faces_indices = {'s1': (0, 1, 2, 3),
                               's2': (4, 5, 6, 7),
                               's3': (0, 1, 4, 5),
                               's4': (1, 2, 5, 6),
                               's5': (2, 3, 6, 7),
                               's6': (0, 3, 4, 7)
                               }
        self._faces = self._construct_faces(self._face_indices)
