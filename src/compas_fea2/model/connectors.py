from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from compas_fea2.model.nodes import Node

class Connector(FEAData):
    """Base class for connectors.

    A Connector links nodes between parts in the model.

    Notes
    -----
    Connectors are registered to a :class:`compas_fea2.model.Model`.

    """

    def __init__(self, nodes, **kwargs):
        super(Connector, self).__init__(**kwargs)
        self._nodes = Node
        self.nodes = nodes

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        if len(nodes)!=2:
            raise ValueError("you can only connect two nodes")
        for n in nodes:
            if not isinstance(n, Node):
                raise ValueError("you can only connect Nodes")
        if nodes[0].part == nodes[-1].part:
            raise ValueError("Nodes must belong to different parts")
        self._nodes = nodes


class SpringConnector(Connector):
    """Spring connector."""

    def __init__(self, nodes, **kwargs):
        super(SpringConnector, self).__init__(nodes, **kwargs)
