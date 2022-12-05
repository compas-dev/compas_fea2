from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _Constraint(FEAData):
    """Initialises base Constraint object. A constraint removes degree of freedom
    of nodes in the model.

    Note
    ----
    Constraints are registered to a :class:`compas_fea2.model.Model`.

    Parameters
    ----------
    name : str,optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    """

    def __init__(self, *, name=None, **kwargs):
        super(_Constraint, self).__init__(name, **kwargs)

# ------------------------------------------------------------------------------
# MPC
# ------------------------------------------------------------------------------


class MultiPointConstraint(_Constraint):
    """A MPC constraint links a node (master) to other nodes (slaves) in the model.

    Parameters
    ----------
    name : str,optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : :class:`compas_fea2.model.NodesGroup`
        Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.

    """

    def __init__(self, constraint_type, name=None, **kwargs):
        super(MultiPointConstraint, self).__init__(name=name, **kwargs)
        self.constraint_type = constraint_type


class TieMPC(MultiPointConstraint):
    """A MPC constraint links a node (master) to other nodes (slaves) in the model.
    """


class BeamMPC(MultiPointConstraint):
    """A MPC constraint links a node (master) to other nodes (slaves) in the model.
    """

class TieConstraint(_Constraint):
    """Tie constraint between two surfaces.
    """
