from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from compas_fea2.base import FEAData
from compas_fea2.model.groups import _Group
from compas_fea2.model.nodes import Node
from compas_fea2.model.parts import RigidPart
from compas_fea2.model.groups import NodesGroup


class Connector(FEAData):
    """Base class for connectors.

    A Connector links nodes between parts in the model.

    Parameters
    ----------
    nodes : list[Node] | compas_fea2.model.groups.NodeGroup
        The connected nodes. The nodes must be registered to different parts.
        For connecting nodes in the same part, check :class:`compas_fea2.model.elements.SpringElement`.

    Notes
    -----
    Connectors are registered to a :class:`compas_fea2.model.Model`.

    """

    def __init__(self, nodes: Union[List[Node], _Group], **kwargs):
        super().__init__(**kwargs)
        self._key: Optional[str] = None
        self._nodes: Optional[List[Node]] = nodes

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__.__name__,
            "nodes": [node.__data__ for node in self._nodes],
        }

    @classmethod
    def __from_data__(cls, data, model):
        from compas_fea2.model.nodes import Node

        nodes = [Node.__from_data__(node, model) for node in data["nodes"]]
        return cls(nodes=nodes)

    @property
    def nodes(self) -> List[Node]:
        return self._nodes

    @property
    def model(self):
        return self._registration

    @nodes.setter
    def nodes(self, nodes: Union[List[Node], _Group]):
        if isinstance(nodes, _Group):
            nodes = nodes._members
        if isinstance(nodes, Node):
            nodes = [nodes]
        if len(nodes) != 2:
            raise ValueError("You can only connect two nodes")
        for n in nodes:
            if not isinstance(n, Node):
                raise ValueError("You can only connect Nodes")
            if isinstance(n.part, RigidPart) and not n.is_reference:
                raise ValueError("Connections to rigid parts must be done to the reference point of the part.")
        if nodes[0].part == nodes[-1].part:
            raise ValueError("Nodes must belong to different parts")
        self._nodes = nodes


class LinearConnector(Connector):
    """Linear connector.

    Parameters
    ----------
    nodes : list[Node] | compas_fea2.model.groups.NodeGroup
        The connected nodes. The nodes must be registered to different parts.
        For connecting nodes in the same part, check :class:`compas_fea2.model.elements.SpringElement`.
    dofs : str
        The degrees of freedom to be connected. Options are 'beam', 'bar', or a list of integers.
    """

    def __init__(self, master, slave, section, **kwargs):
        super().__init__(nodes=[master, slave], **kwargs)
        if isinstance(master, _Group):
            master = list(master._members)[0]
        if isinstance(slave, _Group):
            slave = list(slave._members)[0]
        if master.part == slave.part:
            raise ValueError("Nodes must belong to different parts")
        self._master = master
        self._slave = slave
        self._section = section
        self._nodes = NodesGroup(nodes=[self.master, self.slave])

    @property
    def nodes(self):
        return self._nodes

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, value):
        self._master = value
        self._nodes = NodesGroup(nodes=[self.master, self.slave])

    @property
    def slave(self):
        return self._slave

    @slave.setter
    def slave(self, value):
        self._slave = value
        self._nodes = NodesGroup(nodes=[self.master, self.slave])

    @property
    def section(self):
        return self._section

    @property
    def __data__(self):
        data = super().__data__
        data.update({"dofs": self._dofs})
        return data

    @classmethod
    def __from_data__(cls, data, model):
        instance = super().__from_data__(data, model)
        instance._dofs = data["dofs"]
        return instance

    @property
    def dofs(self) -> str:
        return self._dofs


class RigidLinkConnector(Connector):
    """Rigid link connector.

    Parameters
    ----------
    nodes : list[Node] | compas_fea2.model.groups.NodeGroup
        The connected nodes. The nodes must be registered to different parts.
        For connecting nodes in the same part, check :class:`compas_fea2.model.elements.RigidElement`.
    dofs : str
        The degrees of freedom to be connected. Options are 'beam', 'bar', or a list of integers.
    """

    def __init__(self, nodes: Union[List[Node], _Group], dofs: str = "beam", **kwargs):
        super().__init__(nodes, **kwargs)
        self._dofs: str = dofs

    @property
    def __data__(self):
        data = super().__data__
        data.update({"dofs": self._dofs})
        return data

    @classmethod
    def __from_data__(cls, data, model):
        instance = super().__from_data__(data, model)
        instance._dofs = data["dofs"]
        return instance

    @property
    def dofs(self) -> str:
        return self._dofs


class SpringConnector(Connector):
    """Spring connector."""

    def __init__(self, nodes: Union[List[Node], _Group], section, yielding: Optional[Dict[str, float]] = None, failure: Optional[Dict[str, float]] = None, **kwargs):
        super().__init__(nodes, **kwargs)
        self._section = section
        self._yielding: Optional[Dict[str, float]] = yielding
        self._failure: Optional[Dict[str, float]] = failure

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "section": self._section,
                "yielding": self._yielding,
                "failure": self._failure,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data, model):
        from importlib import import_module

        instance = super().__from_data__(data, model)
        cls_section = import_module(".".join(data["section"]["class"].split(".")[:-1]))
        instance._section = cls_section.__from_data__(data["section"])
        instance._yielding = data["yielding"]
        instance._failure = data["failure"]
        return instance

    @property
    def section(self):
        return self._section

    @property
    def yielding(self) -> Optional[Dict[str, float]]:
        return self._yielding

    @yielding.setter
    def yielding(self, value: Dict[str, float]):
        try:
            value["c"]
            value["t"]
        except KeyError:
            raise ValueError("You must provide the yielding value for both compression and tension")
        self._yielding = value

    @property
    def failure(self) -> Optional[Dict[str, float]]:
        return self._failure

    @failure.setter
    def failure(self, value: Dict[str, float]):
        try:
            value["c"]
            value["t"]
        except KeyError:
            raise ValueError("You must provide the failure value for both compression and tension")
        self._failure = value


class ZeroLengthConnector(Connector):
    """Zero length connector connecting overlapping nodes."""

    def __init__(self, nodes: Union[List[Node], _Group], direction, **kwargs):
        super().__init__(nodes, **kwargs)
        self._direction = direction

    @property
    def __data__(self):
        data = super().__data__
        data.update({"direction": self._direction})
        return data

    @classmethod
    def __from_data__(cls, data, model):
        instance = super().__from_data__(data, model)
        instance._direction = data["direction"]
        return instance

    @property
    def direction(self):
        return self._direction


class ZeroLengthSpringConnector(ZeroLengthConnector):
    """Spring connector connecting overlapping nodes."""

    def __init__(self, nodes: Union[List[Node], _Group], direction, section, yielding: Optional[Dict[str, float]] = None, failure: Optional[Dict[str, float]] = None, **kwargs):
        # SpringConnector.__init__(self, nodes=nodes, section=section, yielding=yielding, failure=failure)
        super().__init__(nodes, direction, **kwargs)
        self._section = section
        self._yielding = yielding
        self._failure = failure

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "section": self._section,
                "yielding": self._yielding,
                "failure": self._failure,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data, model):
        from importlib import import_module

        instance = super().__from_data__(data, model)
        cls_section = import_module(".".join(data["section"]["class"].split(".")[:-1]))
        instance._section = cls_section.__from_data__(data["section"])
        instance._yielding = data["yielding"]
        instance._failure = data["failure"]
        return instance


class ZeroLengthContactConnector(ZeroLengthConnector):
    """Contact connector connecting overlapping nodes."""

    def __init__(self, nodes: Union[List[Node], _Group], direction, Kn: float, Kt: float, mu: float, **kwargs):
        super().__init__(nodes, direction, **kwargs)
        self._Kn: float = Kn
        self._Kt: float = Kt
        self._mu: float = mu

    @property
    def Kn(self) -> float:
        return self._Kn

    @property
    def Kt(self) -> float:
        return self._Kt

    @property
    def mu(self) -> float:
        return self._mu

    @property
    def __data__(self):
        data = super().__data__
        data.update(
            {
                "Kn": self._Kn,
                "Kt": self._Kt,
                "mu": self._mu,
            }
        )
        return data

    @classmethod
    def __from_data__(cls, data, model):
        instance = super().__from_data__(data, model)
        instance._Kn = data["Kn"]
        instance._Kt = data["Kt"]
        instance._mu = data["mu"]
        return instance
