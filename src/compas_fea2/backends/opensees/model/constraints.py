from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base.model import ConstraintBase
from compas_fea2.backends._base.model import TieConstraintBase


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Constraint',
    'TieConstraint',
]


class Constraint(ConstraintBase):
    def __init__(self, name):
        super(Constraint).__init__(name)
        raise NotImplementedError


class TieConstraint(TieConstraintBase):
    def __init__(self, name, master, slave, tol):
        super(TieConstraint).__init__(name, master, slave, tol)
        raise NotImplementedError
