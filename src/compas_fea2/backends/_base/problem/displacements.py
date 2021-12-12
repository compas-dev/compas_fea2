from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model.bcs import GeneralBCBase

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'GeneralDisplacementBase',
]


class GeneralDisplacementBase(GeneralBCBase):

    def __init__(self, name, nodes, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        super(GeneralDisplacementBase, self).__init__(name, nodes, x, y, z, xx, yy, zz, axes)
