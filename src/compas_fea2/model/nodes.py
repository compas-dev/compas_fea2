from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities.maps import geometric_key
from compas.geometry import Point
from compas_fea2.base import FEAData

from .bcs import _BoundaryCondition
import compas_fea2

class Node(FEAData):
    """Initialises base Node object.

    Note
    ----
    Nodes are registered to a :class:`compas_fea2.model.DeformablePart` object and can
    belong to only one Part. Every time a node is added to a Part, it gets
    registered to that Part.

    Parameters
    ----------
    xyz : list[float, float, float] | :class:`compas.geometry.Point`
        The location of the node in the global coordinate system.
    mass : float or tuple, optional
        Lumped nodal mass, by default ``None``. If ``float``, the same value is
        used in all 3 directions. if you want to specify a different mass for each
        direction, provide a ``tuple`` as (mass_x, mass_y, mass_z) in global
        coordinates.
    temperature : float, optional
        The temperature at the Node.
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    mass : tuple
        Lumped nodal mass in the 3 global directions (mass_x, mass_y, mass_z).
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
        The geometric key of the Node.
    dof : dict
        Dictionary with the active degrees of freedom.
    on_boundary : bool | None, read-only
        `True` if the node is on the boundary mesh of the part, `False`
        otherwise, by default `None`.
    is_reference : bool, read-only
        `True` if the node is a reference point of :class:`compas_fea2.model.RigidPart`,
        `False` otherwise.
    part : :class:`compas_fea2.model._Part`, read-only
        The Part where the element is assigned.
    model : :class:`compas_fea2.model.Model`, read-only
        The Model where the element is assigned.
    point : :class:`compas.geometry.Point`
        The Point equivalent of the Node.
    temperature : float
        The temperature at the Node.

    Examples
    --------
    >>> node = Node(xyz=(1.0, 2.0, 3.0))

    """

    def __init__(self, xyz, mass=None, temperature=None, name=None, **kwargs):
        super(Node, self).__init__(name=name, **kwargs)
        self._key = None

        self.xyz = xyz
        self._x = xyz[0]
        self._y = xyz[1]
        self._z = xyz[2]

        self._bc = None
        self._dof = {'x': True, 'y': True, 'z': True, 'xx': True, 'yy': True, 'zz': True}

        self._mass = mass if isinstance(mass, tuple) else tuple([mass]*3)
        self._temperature = temperature

        self._on_boundary = None
        self._is_reference = False

        self._loads = {}
        self._displacements = {}
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
    def xyz(self):
        return [self._x, self._y, self._z]

    @xyz.setter
    def xyz(self, value):
        if len(value)!=3:
            raise ValueError('Provide a 3 element touple or list')
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
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value if isinstance(value, tuple) else tuple([value]*3)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def gkey(self):
        return geometric_key(self.xyz, precision=compas_fea2.PRECISION)

    @property
    def dof(self):
        if self.bc:
            return {attr: not bool(getattr(self.bc, attr)) for attr in ['x', 'y', 'z', 'xx', 'yy', 'zz']}
        else:
            return self._dof

    @property
    def bc(self):
        return self._bc

    @property
    def loads(self):
        return self._loads

    @property
    def displacements(self):
        return self._displacements

    @property
    def on_boundary(self):
        return self._on_boundary

    @property
    def is_reference(self):
        return self._is_reference

    @property
    def results(self):
        return self._results

    @property
    def point(self):
        return Point(*self.xyz)
