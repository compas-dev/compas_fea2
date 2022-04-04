from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Timber(FEAData):
    """Base class for Timber material"""

    def __init__(self, *, name=None, **kwargs):
        super(Timber, self).__init__(name=name, **kwargs)
        raise NotImplementedError('The current material is not available in the selected backend')
