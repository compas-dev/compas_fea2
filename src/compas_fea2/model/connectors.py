from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas_fea2.model.groups import _Group
from compas_fea2.model.nodes import Node
from compas_fea2.model.parts import RigidPart


class Connector(FEAData):
    """Base class for connectors.

    A Connector links nodes between parts in the model.

    Parameters
    ----------
    nodes : list, :class:`compas_fea2.model.groups.NodeGroup`
        The connected nodes. The nodes must be registered to different parts.
        For connecting nodes in the same part, check :class:`compas_fea2.model.elements.SpringElement`.
    section : :class:`compas_fea2.model.sections.ConnectorSection`
        The section containing the mechanical properties of the connector.

    Notes
    -----
    Connectors are registered to a :class:`compas_fea2.model.Model`.

    """

    def __init__(self, nodes, **kwargs):
        super(Connector, self).__init__(**kwargs)
        self._key = None
        self._nodes = None
        self.nodes = nodes

    @property
    def nodes(self):
        return self._nodes

    @property
    def model(self):
        return self._registration

    @nodes.setter
    def nodes(self, nodes):
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


class RigidLinkConnector(Connector):
    """Rigid link connector.

    Parameters
    ----------
    nodes : list, :class:`compas_fea2.model.groups.NodeGroup`
        The connected nodes. The nodes must be registered to different parts.
        For connecting nodes in the same part, check :class:`compas_fea2.model.elements.SpringElement`.
    dofs : str
        The degrees of freedom to be connected. Options are 'beam', 'bar', or a list of integers.
    """

    def __init__(self, nodes, dofs="beam", **kwargs):
        super(RigidLinkConnector, self).__init__(nodes, **kwargs)
        self._dofs = dofs

    @property
    def dofs(self):
        return self._dofs


class SpringConnector(Connector):
    """Spring connector."""

    def __init__(self, nodes, section, yielding=None, failure=None, **kwargs):
        super(SpringConnector, self).__init__(nodes, **kwargs)
        self._section = section
        self._yielding = yielding
        self._failure = failure

    @property
    def section(self):
        return self._section

    @property
    def yielding(self):
        return self._yielding

    @yielding.setter
    def yielding(self, value):
        try:
            value["c"]
            value["t"]
        except KeyError:
            raise ValueError("You must provide the yielding value for both compression and tension")
        self._yielding = value

    @property
    def failure(self):
        return self._failure

    @failure.setter
    def failure(self, value):
        try:
            value["c"]
            value["t"]
        except KeyError:
            raise ValueError("You must provide the failure value for both compression and tension")
        self._failure = value


class ZeroLengthConnector(Connector):
    """Zero length connector connecting overlapping nodes."""

    def __init__(self, nodes, direction, **kwargs):
        super(ZeroLengthConnector, self).__init__(nodes, **kwargs)
        self._direction = direction

    @property
    def direction(self):
        return self._direction


class ZeroLengthSpringConnector(ZeroLengthConnector):
    """Spring connector connecting overlapping nodes."""

    def __init__(self, nodes, direction, section, yielding=None, failure=None, **kwargs):
        # SpringConnector.__init__(self, nodes=nodes, section=section, yielding=yielding, failure=failure)
        ZeroLengthConnector.__init__(self, nodes, direction, **kwargs)


class ZeroLengthContactConnector(ZeroLengthConnector):
    """Contact connector connecting overlapping nodes."""

    def __init__(self, nodes, direction, Kn, Kt, mu, **kwargs):
        super(ZeroLengthContactConnector, self).__init__(nodes, direction, **kwargs)
        self._Kn = Kn
        self._Kt = Kt
        self._mu = mu

    @property
    def Kn(self):
        return self._Kn

    @property
    def Kt(self):
        return self._Kt

    @property
    def mu(self):
        return self._mu
