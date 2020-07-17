from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._core.model import ConstraintBase
from compas_fea2.backends._core.model import TieConstraintBase


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Constraint',
    'TieConstraint',
]


class Constraint(ConstraintBase):
    NotImplemented


class TieConstraint(TieConstraintBase):
    NotImplemented
