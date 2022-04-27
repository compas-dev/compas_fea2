from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import HardContactFrictionPenalty


class OpenseesHardContactFrictionPenalty(HardContactFrictionPenalty):
    """"""
    __doc__ += HardContactFrictionPenalty.__doc__

    def __init__(self, mu, tollerance=0.005, name=None, **kwargs) -> None:
        super(OpenseesHardContactFrictionPenalty, self).__init__(mu, tollerance, name=name, **kwargs)
        raise NotImplementedError
