from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import geometric_key
from ..base import FEABase


__all__ = ['NodeBase']


class NodeBase(FEABase):
    """Initialises base Node object.

    Parameters
    ----------
    xyz : list
        [x, y, z] co-ordinates of the node.
    ex : list
        Node's local x axis.
    ey : list
        Node's local y axis.
    ez : list
        Node's local z axis.
    mass : float
        Mass in kg associated with the node.
    label : string
        Node's label. If no label is specified, it is automatically generated
        when a node is added. The label does not need to be unique.

    Attributes
    ----------
    xyz : list
        [x, y, z] co-ordinates of the node.
    x : float
        x co-ordinates of the node.
    y : float
        y co-ordinates of the node.
    z : float
        z co-ordinates of the node.
    ex : list
        Node's local x axis.
    ey : list
        Node's local y axis.
    ez : list
        Node's local z axis.
    mass : float
        Mass in kg associated with the node.
    label : string
        Node's label. If no label is specified, it is automatically generated
        when a node is added. The label does not need to be unique.
    key : int
        Node key number. The key number is unique.

    Examples
    --------
    >>> node = Node(1.0, 2.0, 3.0)
    """

    def __init__(self, xyz, ex=None, ey=None, ez=None, mass=None, label=None):
        self._label = None
        self.tag = 0
        self.xyz = [float(x) for x in xyz]
        self.ex = ex
        self.ey = ey
        self.ez = ez
        self.mass = mass
        self.label = label

    @property
    def gkey(self):
        return geometric_key([self.x, self.y, self.z])

    @property
    def x(self):
        return self.xyz[0]

    @property
    def y(self):
        return self.xyz[1]

    @property
    def z(self):
        return self.xyz[2]

    @property
    def label(self):
        if not self._label:
            self._label = "node-{}".format(self.tag)
        return self._label

    @label.setter
    def label(self, label):
        self._label = label
