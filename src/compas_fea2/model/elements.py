from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas_fea2.base import FEABase


class Element(FEABase):
    """Initialises a base Element object.

    Parameters
    ----------
    key : int
        Key number of the element.
    nodes : list[:class:`compas_fea2.model.Node`]
        Ordered list of node identifiers to which the element connects.
    section : :class:`compas_fea2.model.Section`
        Section Object assigned to the element.
    name : str, optional
        The name of the Element, by default the element key.

    Attributes
    ----------
    key : int
        Key number of the element.
    nodes : list[:class:`compas_fea2.model.Node`]
        Ordered list of node identifiers to which the element connects.
    nodes_key : str, read-only
        Identifier of the conntected nodes.
    section : :class:`compas_fea2.model.Section`
        Section object.
    frame : :class:`compas.geometry.Frame`
        The local coordinate system for property assignement.
        Default to the global coordinate system.

    Warnings
    --------
    The nodes of the element must be provided in the correct order!

    """

    def __init__(self, *, nodes, section, **kwargs):
        super(Element, self).__init__(**kwargs)
        self._key = None
        self._nodes = nodes
        self._connected_nodes = []
        self._section = section
        self._frame = None

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
        return '_'.join(sorted([str(node.key) for node in self.nodes]))

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
