from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class Constraint(FEABase):
    """Initialises base Constraint object.

    Parameters
    ----------
    name : str
        Name of the Constraint object.

    """

    def __init__(self, name):
        super(Constraint, self).__init__(name=name)


class TieConstraint(Constraint):
    """Tie constraint between two sets of nodes, elements or surfaces.

    Parameters
    ----------
    name : str
        TieConstraint name.
    master : str
        Master set name.
    slave : str
        Slave set name.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    name : str
        TieConstraint name.
    master : str
        Master set name.
    slave : str
        Slave set name.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """

    def __init__(self, name, *, master, slave, tol):
        super(TieConstraint, self).__init__(name)
        self._master = master
        self._slave = slave
        self._tol = tol

    @property
    def master(self):
        return self._master

    @property
    def slave(self):
        return self._slave

    @property
    def tol(self):
        return self._tol
