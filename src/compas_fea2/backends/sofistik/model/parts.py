from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.parts import DeformablePart
from compas_fea2.model.parts import RigidPart

class SofistikDeformablePart(DeformablePart):
    """Sofistik implementation of :class:`compas_fea2.model.parts.DeformablePart`.\n
    """
    __doc__ += DeformablePart.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikDeformablePart, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikRigidPart(RigidPart):
    """Sofistik implementation of :class:`compas_fea2.model.parts.RigidPart`.\n
    """
    __doc__ += RigidPart.__doc__

    def __init__(self, reference_point=None, name=None, **kwargs):
        super(SofistikRigidPart, self).__init__(reference_point=reference_point, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

