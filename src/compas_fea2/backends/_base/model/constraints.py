
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'ConstraintBase',
    'TieConstraintBase',
]


class ConstraintBase(FEABase):
    """Initialises base Constraint object.

    Parameters
    ----------
    name : str
        Name of the Constraint object.

    Attributes
    ----------
    name : str
        Name of the Constraint object.
    """

    def __init__(self, name):
        self.__name__ = 'ConstraintObject'
        self._name = name

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    @property
    def name(self):
        """The name property."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class TieConstraintBase(ConstraintBase):
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

    def __init__(self, name, master, slave, tol):
        super(ConstraintBase, self).__init__(name=name)
        self.__name__ = 'TieConstraint'
        self._master = master
        self._slave = slave
        self._tol = tol

    @property
    def master(self):
        """The master property."""
        return self._master

    @property
    def slave(self):
        """The slave property."""
        return self._slave

    @property
    def tol(self):
        """The tol property."""
        return self._tol
