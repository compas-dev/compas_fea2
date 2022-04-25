from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.displacements import GeneralDisplacement

class AnsysGeneralDisplacement(GeneralDisplacement):
    """ Ansys implementation of :class:`.GeneralDisplacement`.\n
    """
    __doc__ += GeneralDisplacement.__doc__

    def __init__(self, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global', name=None, **kwargs):
        super(AnsysGeneralDisplacement, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

