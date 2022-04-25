from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.releases import BeamEndPinRelease


class OpenseesBeamEndPinRelease(BeamEndPinRelease):
    def __init__(self, m1=False, m2=False, t=False, name=None, **kwargs):
        super(OpenseesBeamEndPinRelease, self).__init__(m1=m1, m2=m2, t=t, name=name, **kwargs)
        raise NotImplementedError()
