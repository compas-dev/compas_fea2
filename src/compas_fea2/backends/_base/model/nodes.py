from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import compas
import compas_fea2

from compas.utilities.maps import geometric_key
from compas_fea2.backends._base.base import FEABase
# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'NodeBase',
]


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
        self.__name__ = 'Node'
        self.key = 0
        self.xyz = [float(x) for x in xyz]
        self.x = self.xyz[0]
        self.y = self.xyz[1]
        self.z = self.xyz[2]
        self.ex = ex
        self.ey = ey
        self.ez = ez
        self.mass = mass
        self.label = label
        self.gkey = geometric_key(self.xyz, precision=compas_fea2.precision,
                                  sanitize=False)  # '{}_{}_{}'.format(self.x, self.y, self.z)

    def __repr__(self):

        return '{0}({1} - {2})'.format(self.__name__, self.key, self.label)
