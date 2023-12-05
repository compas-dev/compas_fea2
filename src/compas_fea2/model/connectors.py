from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Connector(FEAData):
    """Base class for connectors.

    A Connector links a node to one or more other nodes in the model.

    Notes
    -----
    Connectors are registered to a :class:`compas_fea2.model.Model`.

    """

    def __init__(self, **kwargs):
        super(Connector, self).__init__(**kwargs)


class Spring(Connector):
    """Elastic spring connector."""

    def __init__(self, **kwargs):
        super(Spring, self).__init__(**kwargs)
