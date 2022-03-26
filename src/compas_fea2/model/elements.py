from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas_fea2.base import FEAData


class Element(FEAData):
    """Initialises a base Element object.

    Note
    ----
    Elements can belong to only one Part. Every time an element is added to a part,
    it gets registered to that part.

    Warning
    -------
    if the nodes to which the element connects do not belong to the same part,
    they will be deregistered from the original part and registered to the new
    part once the element is added to this part.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    nodes : list[:class:`compas_fea2.model.Node`]
        Ordered list of node identifiers to which the element connects.
    section : :class:`compas_fea2.model.Section`
        Section Object assigned to the element.
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
    section : :class:`compas_fea2.model.Section`
        Section object.
    frame : :class:`compas.geometry.Frame`
        The local coordinate system for property assignement.
        Default to the global coordinate system.
    part : :class:`compas_fea2.model.Part` | None
        The parent part.

    """

    def __init__(self, *, nodes, section, frame=None, part=None, name=None, **kwargs):
        super(Element, self).__init__(**kwargs)
        self._name = name or 'Element_'+str(id(self))
        self._key = None
        self._nodes = nodes
        self._section = section
        self._frame = frame
        self._part = part

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
        self._part = value


# ==============================================================================
# 0D elements
# ==============================================================================


class MassElement(Element):
    """A 0D element for concentrated point mass.
    """


# ==============================================================================
# 1D elements
# ==============================================================================


class BeamElement(Element):
    """A 1D element that resists axial, shear, bending and torsion.
    """


class SpringElement(Element):
    """A 1D spring element.
    """


class TrussElement(Element):
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


class ShellElement(Element):
    """A 2D element that resists axial, shear, bending and torsion.
    """


class MembraneElement(ShellElement):
    """A shell element that resists only axial loads.
    """


# ==============================================================================
# 3D elements
# ==============================================================================


class SolidElement(Element):
    """A 3D element that resists axial, shear, bending and torsion.
    """


class TetrahedronElement(SolidElement):
    """A Solid element with 4 faces.
    """


class PentahedronElement(SolidElement):
    """A Solid element with 5 faces (extruded triangle).
    """


class HexahedronElement(SolidElement):
    """A Solid cuboid element with 6 faces (extruded rectangle).
    """
