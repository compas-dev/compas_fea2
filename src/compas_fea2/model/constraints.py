from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _Constraint(FEAData):
    """A constraint removes degree of freedom of nodes in the model.

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


class _MultiPointConstraint(_Constraint):
    """A MultiPointContrstaint (MPC) links a node (master) to other nodes
    (slaves) in the model.

    Note
    ----
    Constraints are registered to a :class:`compas_fea2.model.Model`.

    Parameters
    ----------
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.
    name : str,optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.
    """

    def __init__(self, constraint_type, name=None, **kwargs):
        super(_MultiPointConstraint, self).__init__(name=name, **kwargs)
        self.constraint_type = constraint_type


class TieMPC(_MultiPointConstraint):
    """Tie MPC that constraints axial translations.
    """
    __doc__ += _MultiPointConstraint.__doc__


class BeamMPC(_MultiPointConstraint):
    """Beam MPC that constraints axial translations and rotations.
    """
    __doc__ += _MultiPointConstraint.__doc__

#TODO check!
class _SurfaceConstraint(_Constraint):
    """A SurfaceContrstaint links a surface (master) to another surface (slave)
    in the model.

    Note
    ----
    Constraints are registered to a :class:`compas_fea2.model.Model`.

    Parameters
    ----------
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.
    name : str,optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.Node`
        Node that act as master.
    slaves : [:class:`compas_fea2.model.Node`] | :class:`compas_fea2.model.NodesGroup`
        List or Group of nodes that act as slaves.
    tol : float
        Constraint tolerance, distance limit between master and slaves.
    """

class TieConstraint(_SurfaceConstraint):
    """Tie constraint between two surfaces.
    """
