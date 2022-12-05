from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.materials.timber import Timber

class SofistikTimber(Timber):
    """Sofistik implementation of :class:`compas_fea2.model.materials.timber.Timber`.\n
    """
    __doc__ += Timber.__doc__

    def __init__(self, *, name=None, **kwargs):
        super(SofistikTimber, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

