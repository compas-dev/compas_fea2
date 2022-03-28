from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities.maps import geometric_key
from compas_fea2.base import FEAData

from .bcs import BoundaryCondition


class Node(FEAData):
    """Initialises base Node object.

    Note
    ----
    Nodes can belong to only one Part. Every time a node is added to a part, it
    gets registered to that part.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    xyz : list[float, float, float] | :class:`compas.geometry.Point`
        The location of the node in the global coordinate system.
    part : `compas_fea2.model.Part`, optional
        Part object where the node will be registered, by default ``None``

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    key : str, read-only
        The identifier of the node.
    xyz : list[float]
        The location of the node in the global coordinate system.
    x : float
        The X coordinate.
    y : float
        The Y coordinate.
    z : float
        The Z coordinate.
    gkey : str, read-only
        The geometric key.
    part : :class:`compas_fea2.model.Part` | None
        The parent part of the node.
    dof : dict
        Dictionary with the active degrees of freedom

    Examples
    --------
    >>> node = Node(1.0, 2.0, 3.0)

    """

    def __init__(self, xyz, part=None, name=None, **kwargs):
        super(Node, self).__init__(name, **kwargs)
        self._key = None
        self._x = None
        self._y = None
        self._z = None
        self._part = part
        self._dof = {'x': True, 'y': True, 'z': True, 'xx': True, 'yy': True, 'zz': True}
        self._loads = set()
        self._displacements = set()
        self.xyz = xyz

    @property
    def key(self):
        return self._key

    @property
    def xyz(self):
        return [self._x, self._y, self._z]

    @xyz.setter
    def xyz(self, value):
        self._x = value[0]
        self._y = value[1]
        self._z = value[2]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = float(value)

    @property
    def gkey(self):
        return geometric_key(self.xyz)

    @property
    def part(self):
        return self._part

    @part.setter
    def part(self, value):
        self._part = value

    @property
    def dof(self):
        return self._dof

    @dof.setter
    def dof(self, bc):
        if not isinstance(bc, BoundaryCondition):
            raise TypeError('{!r} is not a Boundary Condition'.format(bc))
        self._dof = {attr: not bool(getattr(bc, attr)) for attr in ['x', 'y', 'z', 'xx', 'yy', 'zz']}

    @property
    def loads(self):
        return self._loads

    @property
    def displacements(self):
        return self._displacements
