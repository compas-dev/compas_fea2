from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.nodes import Node

class AnsysNode(Node):
    """ Ansys implementation of :class:`.Node`.\n
    """
    __doc__ += Node.__doc__

    def __init__(self, xyz, mass=None, part=None, name=None, **kwargs):
        super(AnsysNode, self).__init__(xyz=xyz, mass=mass, part=part, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

