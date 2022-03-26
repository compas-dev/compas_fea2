from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _Constraint(FEAData):
    """Initialises base Constraint object.

    Parameters
    ----------
    name : str,optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """

    def __init__(self, *, master, slave, tol, name=None, **kwargs):
        super(_Constraint, self).__init__(**kwargs)
        self._name = name or "Constraint_"+str(id(self))
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


class TieConstraint(_Constraint):
    """Tie constraint between two sets of nodes, elements or surfaces.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """

    def __init__(self, *, master, slave, tol, name=None, **kwargs):
        super(TieConstraint, self).__init__(master=master, slave=slave, tol=tol, name=name, **kwargs)


class Pin3DConstraint(_Constraint):
    """Pin constraint between two sets of nodes, elements or surfaces that allows
    all rotations and fixes all translations.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """
    pass


class Pin2DConstraint(_Constraint):
    """Pin constraint between two sets of nodes, elements or surfaces that allows
    rotations about an axis and fixes all translations.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.
    axis : :class:`compas.geometry.Vector`
        Axis of rotation.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.
    axis : :class:`compas.geometry.Vector`
        Axis of rotation.

    """

    def __init__(self, *, master, slave, tol, axis, name=None, **kwargs):
        super(SliderConstraint, self).__init__(master=master, slave=slave, tol=tol, name=name, **kwargs)
        self.axis = axis


class SliderConstraint(_Constraint):

    def __init__(self, *, master, slave, tol, plane, name=None, **kwargs):
        super(SliderConstraint, self).__init__(master=master, slave=slave, tol=tol, name=name, **kwargs)
        self.plane = plane
