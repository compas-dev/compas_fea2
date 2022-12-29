from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _Connector(FEAData):
    """Initialises base Connector object. A Connector links a node to one or more
    other nodes in the model.

    Note
    ----
    Connectors are registered to a :class:`compas_fea2.model.Model`.

    Parameters
    ----------
    name : str,optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    """

    def __init__(self, *, name=None, **kwargs):
        super(_Connector, self).__init__(name, **kwargs)


class Spring(_Connector):
    """Elastic spring connector.
    """
    __doc__ += _Connector.__doc__
    def __init__(self,  name=None, **kwargs):
        super(Spring, self).__init__(name=name, **kwargs)
