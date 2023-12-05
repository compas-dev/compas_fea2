from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Constraint(FEAData):
    """Base class for constraints.

    A constraint removes degree of freedom of nodes in the model.

    """

    def __init__(self, **kwargs):
        super(Constraint, self).__init__(**kwargs)


# ------------------------------------------------------------------------------
# MPC
# ------------------------------------------------------------------------------


class MultiPointConstraint(Constraint):
    """A MultiPointContrstaint (MPC) links a node (master) to other nodes (slaves) in the model.

    Parameters
    ----------
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.

    Attributes
    ----------
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.

    Notes
    -----
    Constraints are registered to a :class:`compas_fea2.model.Model`.

    """

    def __init__(self, constraint_type, **kwargs):
        super(MultiPointConstraint, self).__init__(**kwargs)
        self.constraint_type = constraint_type


class TieMPC(MultiPointConstraint):
    """Tie MPC that constraints axial translations."""


class BeamMPC(MultiPointConstraint):
    """Beam MPC that constraints axial translations and rotations."""


# TODO check!
class SurfaceConstraint(Constraint):
    """A SurfaceContrstaint links a surface (master) to another surface (slave) in the model.

    Parameters
    ----------
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.

    Attributes
    ----------
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.

    """


class TieConstraint(SurfaceConstraint):
    """Tie constraint between two surfaces."""
