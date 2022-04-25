from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.materials.steel import Steel

class AnsysSteel(Steel):
    """ Ansys implementation of :class:`.Steel`.\n
    """
    __doc__ += Steel.__doc__

    def __init__(self, *, fy, fu, eu, E, v, density, name=None, **kwargs):
        super(AnsysSteel, self).__init__(fy=fy, fu=fu, eu=eu, E=E, v=v, density=density, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

