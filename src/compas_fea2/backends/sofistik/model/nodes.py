from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.nodes import Node

class SofistikNode(Node):
    """Sofistik implementation of :class:`compas_fea2.model.nodes.Node`.\n
    """
    __doc__ += Node.__doc__

    def __init__(self, xyz, mass=None, name=None, **kwargs):
        super(SofistikNode, self).__init__(xyz=xyz, mass=mass, name=name, **kwargs)

    def _generate_jobdata(self):
        return """NODE NO {} X {} Y {} Z {}""".format(self.key+1, self.x, self.y, self.z)

