from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Constraint(FEAData):
    """Initialises base Constraint object.
    """

    def __init__(self, **kwargs):
        super(Constraint, self).__init__(**kwargs)


class TieConstraint(Constraint):
    """Tie constraint between two sets of nodes, elements or surfaces.

    Parameters
    ----------
    master : :class:`compas_fea2.model.Node`
        Master set.
    slave : :class:`compas_fea2.model.Node`
        Slave set.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    master : :class:`compas_fea2.model.Node`
        Master set.
    slave : :class:`compas_fea2.model.Node`
        Slave set.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """

    def __init__(self, *, master, slave, tol, **kwargs):
        super(TieConstraint, self).__init__(**kwargs)
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
