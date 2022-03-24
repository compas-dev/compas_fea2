from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import Constraint
from compas_fea2.model import TieConstraint


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Constraint',
    'TieConstraint',
]


class Constraint(Constraint):
    def __init__(self, name):
        super(Constraint).__init__(name)
        raise NotImplementedError


class TieConstraint(TieConstraint):
    def __init__(self, name, master, slave, tol):
        super(TieConstraint).__init__(name, master, slave, tol)
        raise NotImplementedError
