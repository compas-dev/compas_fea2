from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas_fea2.model.nodes import Node
from compas_fea2.model.groups import _Group
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

    def __init__(self, nodes, section, **kwargs):
        super(Connector, self).__init__(**kwargs)
        self._key = None
        self._nodes = None
        self.nodes = nodes
        self._section = section

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

    @property
    def section(self):
        return self._section


class SpringConnector(Connector):
    """Spring connector."""

    def __init__(self, nodes, section, yielding=None, failure=None, **kwargs):
        super(SpringConnector, self).__init__(nodes, section, **kwargs)
        self._yielding = yielding
        self._failure = failure

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


class ZeroLengthSpringConnector(SpringConnector):
    """Spring connector connecting overlapping nodes."""

    def __init__(self, nodes, section, directions, yielding=None, failure=None, **kwargs):
        super(ZeroLengthSpringConnector, self).__init__(nodes, section, yielding, failure, **kwargs)
        self._directions = directions

    @property
    def directions(self):
        return self._directions


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
        super(RigidLinkConnector, self).__init__(nodes, None, **kwargs)
        self._dofs = dofs

    @property
    def dofs(self):
        return self._dofs
