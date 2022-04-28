from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.parts import Part

class AnsysPart(Part):
    """Ansys implementation of :class:`compas_fea2.model.parts.Part`.\n
    """
    __doc__ += Part.__doc__

    def __init__(self, model=None, name=None, **kwargs):
        super(AnsysPart, self).__init__(model=model, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

