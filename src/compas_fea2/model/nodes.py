from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_fea2

from compas.utilities.maps import geometric_key
from compas_fea2.base import FEABase
# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


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
    name : string
        Node's label. If no label is specified, it is automatically generated
        when a node is added. The label does not need to be unique.

    Examples
    --------
    >>> node = Node(1.0, 2.0, 3.0)
    """

    def __init__(self, xyz, ex=None, ey=None, ez=None, mass=None, name=None):
        self.__name__ = 'Node'
        self._key = None
        self._name = name
        self._xyz = [float(x) for x in xyz]
        self._x = self.xyz[0]
        self._y = self.xyz[1]
        self._z = self.xyz[2]
        self._gkey = geometric_key(self.xyz, precision=compas_fea2.precision, sanitize=False)
        self._ex = ex
        self._ey = ey
        self._ez = ez
        self._mass = mass

    @property
    def key(self):
        """int : Node key number. The key number is unique."""
        return self._key

    @property
    def name(self):
        """str : Node's name. If no name is specified, it is automatically generated
        when a node is added. The name does not need to be unique."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def xyz(self):
        """list : [x, y, z] coordinates of the node."""
        return self._xyz

    # @xyz.setter
    # def xyz(self, value):
    #     self._xyz = value

    @property
    def x(self):
        """float : x coordinates of the node."""
        return self._x

    # @x.setter
    # def x(self, value):
    #     self._x = value

    @property
    def y(self):
        """float : y coordinates of the node."""
        return self._y

    # @y.setter
    # def y(self, value):
    #     self._y = value

    @property
    def z(self):
        """float : z coordinates of the node."""
        return self._z

    # @z.setter
    # def z(self, value):
    #     self._z = value

    @property
    def ex(self):
        """list : Node's local x axis."""
        return self._ex

    # @ex.setter
    # def ex(self, value):
    #     self._ex = value

    @property
    def ey(self):
        """list : Node's local y axis."""
        return self._ey

    # @ey.setter
    # def ey(self, value):
    #     self._ey = value

    @property
    def ez(self):
        """list : Node's local z axis."""
        return self._ez

    # @ez.setter
    # def ez(self, value):
    #     self._ez = value

    @property
    def mass(self):
        """float : Mass in kg associated with the node."""
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value

    @property
    def gkey(self):
        """The gkey property."""
        return self._gkey

    def __repr__(self):
        return '{0}({1} - {2})'.format(self.__name__, self._key, self._name)

    def move_node(self):
        raise NotImplementedError

    def rotate_node_axes(self):
        raise NotImplementedError
