from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.interactions import Contact
from compas_fea2.model.interactions import HardContactFrictionPenalty
from compas_fea2.model.interactions import HardContactNoFriction

class AnsysContact(Contact):
    """Ansys implementation of :class:`compas_fea2.model.interactions.Contact`.\n
    """
    __doc__ += Contact.__doc__

    def __init__(self, *, normal, tangent, name=None, **kwargs):
        super(AnsysContact, self).__init__(normal=normal, tangent=tangent, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysHardContactFrictionPenalty(HardContactFrictionPenalty):
    """Ansys implementation of :class:`compas_fea2.model.interactions.HardContactFrictionPenalty`.\n
    """
    __doc__ += HardContactFrictionPenalty.__doc__

    def __init__(self, mu, tollerance, name=None, **kwargs) -> None:
        super(AnsysHardContactFrictionPenalty, self).__init__(mu=mu, tollerance=tollerance, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysHardContactNoFriction(HardContactNoFriction):
    """Ansys implementation of :class:`compas_fea2.model.interactions.HardContactNoFriction`.\n
    """
    __doc__ += HardContactNoFriction.__doc__

    def __init__(self, mu, tollerance, name=None, **kwargs) -> None:
        super(AnsysHardContactNoFriction, self).__init__(mu=mu, tollerance=tollerance, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

