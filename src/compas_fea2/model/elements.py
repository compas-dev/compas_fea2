from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas_fea2.base import FEAData

import compas_fea2


class _Element(FEAData):
    """Initialises a base Element object.

    Note
    ----
    Elements can belong to only one Part. When an element is added to a part,
    it is registered to that part.

    Warning
    -------
    If the nodes to which the element connects are not registered to the same part,
    they will be deregistered from the original part and registered to the new
    part once the element is added to it.

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
    part : :class:`compas_fea2.model.Part`, optional
        The parent part of the element.

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
    part : :class:`compas_fea2.model.Part` | None
        The parent part.

    """
# FIXME frame and orientations are a bit different concepts. find a way to unify them

    def __init__(self, *, nodes, section, frame=None, part=None, implementation=None, name=None, **kwargs):
        super(_Element, self).__init__(name, **kwargs)
        self._key = None
        self._nodes = nodes
        self._section = section
        self._frame = frame
        self._part = part
        self._implementation = implementation

    @property
    def key(self):
        return self._key

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

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
    def part(self):
        return self._part

    @part.setter
    def part(self, value):
        if not isinstance(value, compas_fea2.model.parts.Part):
            raise TypeError('{} is not a Part'.format(value))
        for node in self._nodes:
            node._part = value
        self._part = value

    @property
    def implementation(self):
        return self._implementation


# ==============================================================================
# 0D elements
# ==============================================================================
class MassElement(_Element):
    """A 0D element for concentrated point mass.
    """


# ==============================================================================
# 1D elements
# ==============================================================================
class BeamElement(_Element):
    """A 1D element that resists axial, shear, bending and torsion.

    A beam element is a one-dimensional line element in three-dimensional space
    whose stiffness is associated with deformation of the line (the beam's “axis”).
    These deformations consist of axial stretch; curvature change (bending); and,
    in space, torsion.

    """


class SpringElement(_Element):
    """A 1D spring element.
    """


class TrussElement(_Element):
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
class ShellElement(_Element):
    """A 2D element that resists axial, shear, bending and torsion.

    Shell elements are used to model structures in which one dimension, the
    thickness, is significantly smaller than the other dimensions.

    """


class MembraneElement(ShellElement):
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
class SolidElement(_Element):
    """A 3D element that resists axial, shear, bending and torsion.

    Solid (continuum) elements can be used for linear analysis
    and for complex nonlinear analyses involving contact, plasticity, and large
    deformations.

    Solid elements are general purpose elements and can be used for multiphysics
    problems.

    """
