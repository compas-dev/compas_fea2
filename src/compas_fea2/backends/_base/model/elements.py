from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ..base import FEABase


__all__ = [
    'ElementBase',
    'MassElementBase',
    'BeamElementBase',
    'SpringElementBase',
    'TrussElementBase',
    'StrutElementBase',
    'TieElementBase',
    'ShellElementBase',
    'MembraneElementBase',
    'FaceElementBase',
    'SolidElementBase',
    'PentahedronElementBase',
    'TetrahedronElementBase',
    'HexahedronElementBase',
]


class ElementBase(FEABase):
    """Base class for model elements.

    Parameters
    ----------
    nodes: list
        Ordered nodes the element connects to.
    section: :class:`compas_fea2.backends.Section`
        Section object assigned to the element.
    thermal: bool, optional
        Flag turning thermal properties on or off.
        Default is ``False``.
    """

    def __init__(self, nodes, section, thermal=False):
        super(ElementBase, self).__init__()
        self.tag = 0
        self.nodes = nodes
        self.section = section
        self.thermal = thermal
        self.etype = None
        self.axes = None

    @property
    def key(self):
        return "-".join(sorted([str(node) for node in self.nodes], key=int))


# ==============================================================================
# 0D elements
# ==============================================================================


class MassElementBase(ElementBase):
    """A 0D element representing a concentrated point mass."""

    def __init__(self, *args, **kwargs):
        super(MassElementBase, self).__init__(*args, **kwargs)
        self.etype = 'mass'


# ==============================================================================
# 1D elements
# ==============================================================================


class BeamElementBase(ElementBase):
    """A 1D element that resists axial, shear, bending and torsion.
    """

    def __init__(self, *args, **kwargs):
        super(BeamElementBase, self).__init__(*args, **kwargs)
        self.etype = 'beam'


class SpringElementBase(ElementBase):
    """A 1D spring element.
    """

    def __init__(self, *args, **kwargs):
        super(SpringElementBase, self).__init__(*args, **kwargs)
        self.etype = 'spring'


class TrussElementBase(ElementBase):
    """A 1D element that resists axial loads.
    """

    def __init__(self, *args, **kwargs):
        super(TrussElementBase, self).__init__(*args, **kwargs)
        self.etype = 'truss'


class StrutElementBase(TrussElementBase):
    """A truss element that resists axial compressive loads.
    """

    def __init__(self, *args, **kwargs):
        super(StrutElementBase, self).__init__(*args, **kwargs)
        self.etype = 'strut'


class TieElementBase(TrussElementBase):
    """A truss element that resists axial tensile loads.
    """

    def __init__(self, *args, **kwargs):
        super(TieElementBase, self).__init__(*args, **kwargs)
        self.etype = 'tie'


# ==============================================================================
# 2D elements
# ==============================================================================


class ShellElementBase(ElementBase):
    """A 2D element that resists axial, shear, bending and torsion.
    """

    def __init__(self, *args, **kwargs):
        super(ShellElementBase, self).__init__(*args, **kwargs)
        self.etype = 'shell'


class FaceElementBase(ElementBase):
    """A 2D Face element used for special loading cases.
    """

    def __init__(self, *args, **kwargs):
        super(ElementBase, self).__init__(*args, **kwargs)
        self.etype = 'face'


class MembraneElementBase(ShellElementBase):
    """A shell element that resists only axial loads.
    """

    def __init__(self, *args, **kwargs):
        super(MembraneElementBase, self).__init__(*args, **kwargs)
        self.etype = 'membrane'


# ==============================================================================
# 3D elements
# ==============================================================================


class SolidElementBase(ElementBase):
    """A 3D element that resists axial, shear, bending and torsion.
    """

    def __init__(self, *args, **kwargs):
        super(SolidElementBase, self).__init__(*args, **kwargs)
        self.etype = 'solid'


class TetrahedronElementBase(SolidElementBase):
    """A Solid element with 4 faces.
    """

    def __init__(self, *args, **kwargs):
        super(TetrahedronElementBase, self).__init__(*args, **kwargs)
        self.etype = 'solid4'


class PentahedronElementBase(SolidElementBase):
    """A Solid element with 5 faces (extruded triangle).
    """

    def __init__(self, *args, **kwargs):
        super(PentahedronElementBase, self).__init__(*args, **kwargs)
        self.etype = 'solid5'


class HexahedronElementBase(SolidElementBase):
    """A Solid cuboid element with 6 faces (extruded rectangle).
    """

    def __init__(self, *args, **kwargs):
        super(HexahedronElementBase, self).__init__(*args, **kwargs)
        self.etype = 'solid6'
