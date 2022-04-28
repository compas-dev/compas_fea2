from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.releases import BeamEndPinRelease
from compas_fea2.model.releases import BeamEndSliderRelease

class AnsysBeamEndPinRelease(BeamEndPinRelease):
    """Ansys implementation of :class:`compas_fea2.model.releases.BeamEndPinRelease`.\n
    """
    __doc__ += BeamEndPinRelease.__doc__

    def __init__(self, m1=False, m2=False, t=False, name=None, **kwargs):
        super(AnsysBeamEndPinRelease, self).__init__(m1=m1, m2=m2, t=t, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysBeamEndSliderRelease(BeamEndSliderRelease):
    """Ansys implementation of :class:`compas_fea2.model.releases.BeamEndSliderRelease`.\n
    """
    __doc__ += BeamEndSliderRelease.__doc__

    def __init__(self, v1=False, v2=False, name=None, **kwargs):
        super(AnsysBeamEndSliderRelease, self).__init__(v1=v1, v2=v2, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

