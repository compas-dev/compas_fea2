from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Interface(FEAData):
    """An interface is defined as a pair of master and slave surfaces
    with an interaction property between them.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Master surface.
    slave : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Slave surface.
    interaction : :class:`compas_fea2.model._Interaction`
        Interaction type between master and slave.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    master : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Master surface.
    slave : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Slave surface.
    interaction : :class:`compas_fea2.model._Interaction`
        Interaction type between master and slave.

    """

    def __init__(self, *, master, slave, interaction, name=None, **kwargs):
        super(Interface, self).__init__(name=name, **kwargs)
        self._master = master
        self._slave = slave
        self._interaction = interaction

    @property
    def master(self):
        return self._master

    @property
    def slave(self):
        return self._slave

    @property
    def interaction(self):
        return self._interaction
