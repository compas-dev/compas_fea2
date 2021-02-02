from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ..base import FEABase


__all__ = [
    'ConstraintBase',
    'TieConstraintBase',
]


class ConstraintBase(FEABase):
    """Base class for model constraints.

    Parameters
    ----------
    name: str
        Name of the Constraint object.

    Attributes
    ----------
    name: str
        Name of the Constraint object.
    """

    def __init__(self, name):
        super(ConstraintBase, self).__init__()
        self.name = name


class TieConstraintBase(ConstraintBase):
    """Base class for a tie constraint between two sets of nodes, elements or surfaces.

    Parameters
    ----------
    name: str
        Name of the constraint.
    master: str
        Name of the master set.
    slave: str
        Name of the slave set.
    tol: float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    name: str
        Name of the constraint.
    master: str
        Name of the master set.
    slave: str
        Name of the slave set.
    tol: float
        Constraint tolerance, distance limit between master and slave.
    """

    def __init__(self, name, master, slave, tol):
        super(TieConstraintBase, self).__init__(name)
        self.master = master
        self.slave = slave
        self.tol = tol
