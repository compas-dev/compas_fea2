from typing import Dict
from typing import List
from typing import Optional

from compas.geometry import Point
from compas.tolerance import TOL

import compas_fea2
from compas_fea2.base import FEAData
from compas.geometry import transform_points


class Node(FEAData):
    """Class representing a Node object.

    Parameters
    ----------
    xyz : list[float, float, float] | :class:`compas.geometry.Point`
        The location of the node in the global coordinate system.
    mass : float or tuple, optional
        Lumped nodal mass, by default ``None``. If ``float``, the same value is
        used in all 3 directions. If you want to specify a different mass for each
        direction, provide a ``tuple`` as (mass_x, mass_y, mass_z) in global
        coordinates.
    temperature : float, optional
        The temperature at the Node.
    name : str, optional
        Unique identifier. If not provided, it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Unique identifier.
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

    Notes
    -----
    Nodes are registered to a :class:`compas_fea2.model.Part` object and can
    belong to only one Part. Every time a node is added to a Part, it gets
    registered to that Part.

    Examples
    --------
    >>> node = Node(xyz=(1.0, 2.0, 3.0))

    """

    def __init__(self, xyz: List[float], mass: Optional[float] = None, temperature: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self._key = None

        self._xyz = xyz
        self._x = xyz[0]
        self._y = xyz[1]
        self._z = xyz[2]

        self._bc = None
        self._dof = {"x": True, "y": True, "z": True, "xx": True, "yy": True, "zz": True}

        self._mass = mass if isinstance(mass, list) else list([mass] * 6)
        self._temperature = temperature

        self._on_boundary = None
        self._is_reference = False

        self._loads = {}
        self._total_load = None

        self._connected_elements = []

    @classmethod
    def from_compas_point(cls, point: Point, mass: Optional[float] = None, temperature: Optional[float] = None) -> "Node":
        """Create a Node from a :class:`compas.geometry.Point`.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The location of the node in the global coordinate system.
        mass : float or tuple, optional
            Lumped nodal mass, by default ``None``. If ``float``, the same value is
            used in all 3 directions. If you want to specify a different mass for each
            direction, provide a ``tuple`` as (mass_x, mass_y, mass_z) in global
            coordinates.
        temperature : float, optional
            The temperature at the Node.
        name : str, optional
            Unique identifier. If not provided, it is automatically generated. Set a
            name if you want a more human-readable input file.

        Returns
        -------
        :class:`compas_fea2.model.Node`
            The Node object.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> point = Point(1.0, 2.0, 3.0)
        >>> node = Node.from_compas_point(point)

        """
        return cls(xyz=[point.x, point.y, point.z], mass=mass, temperature=temperature)

    @property
    def part(self) -> "_Part":  # noqa: F821
        return self._registration

    @property
    def model(self) -> "Model":  # noqa: F821
        return self.part._registration

    @property
    def xyz(self) -> List[float]:
        return [self._x, self._y, self._z]

    @xyz.setter
    def xyz(self, value: List[float]):
        if len(value) != 3:
            raise ValueError("Provide a 3 element tuple or list")
        self._x = value[0]
        self._y = value[1]
        self._z = value[2]

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = float(value)

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float):
        self._z = float(value)

    @property
    def mass(self) -> List[float]:
        return self._mass

    @mass.setter
    def mass(self, value: float):
        self._mass = value if isinstance(value, list) else list([value] * 6)

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        self._temperature = value

    @property
    def gkey(self) -> str:
        return TOL.geometric_key(self.xyz, precision=compas_fea2.PRECISION)

    @property
    def dof(self) -> Dict[str, bool]:
        if self.bc:
            return {attr: not bool(getattr(self.bc, attr)) for attr in ["x", "y", "z", "xx", "yy", "zz"]}
        else:
            return self._dof

    @property
    def bc(self):
        return self._bc

    @property
    def on_boundary(self) -> Optional[bool]:
        return self._on_boundary

    @property
    def is_reference(self) -> bool:
        return self._is_reference

    @property
    def results(self):
        return self._results

    @property
    def point(self) -> Point:
        return Point(*self.xyz)

    @property
    def connected_elements(self) -> List:
        return self._connected_elements

    # @property
    # def loads(self) -> Dict:
    #     problems = self.model.problems
    #     steps = [problem.step for problem in problems]
    #     return {step: step.loads(step) for step in steps}

    def transform(self, transformation):
        self.xyz = transform_points([self.xyz], transformation)[0]

    def transformed(self, transformation):
        node = self.copy()
        node.transform(transformation)
        return node

    def displacement(self, step):
        if step.displacement_field:
            return step.displacement_field.get_result_at(location=self)

    def reaction(self, step):
        if step.reaction_field:
            return step.reaction_field.get_result_at(location=self)

    @property
    def displacements(self) -> Dict:
        problems = self.model.problems
        steps = [problem.step for problem in problems]
        return {step: self.displacement(step) for step in steps}

    @property
    def reactions(self) -> Dict:
        problems = self.model.problems
        steps = [problem.step for problem in problems]
        return {step: self.reaction(step) for step in steps}

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__.__name__,
            "xyz": self.xyz,
            "mass": self._mass,
            "temperature": self._temperature,
            "on_boundary": self._on_boundary,
            "is_reference": self._is_reference,
            "dof": self._dof,
            "connected_elements": [e.name for e in self._connected_elements],
        }

    @classmethod
    def __from_data__(cls, data):
        node = cls(
            xyz=data["xyz"],
            mass=data.get("mass"),
            temperature=data.get("temperature"),
        )
        node._on_boundary = data.get("on_boundary")
        node._is_reference = data.get("is_reference")
        node._dof = data.get("dof", {"x": True, "y": True, "z": True, "xx": True, "yy": True, "zz": True})
        node._connected_elements = data.get("connected_elements", [])
        return node
