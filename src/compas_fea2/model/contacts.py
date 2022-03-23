from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class ContactPair(FEAData):
    """Pair of master and slave surfaces to assign an interaction property

    Parameters
    ----------
    master : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Master surface.
    slave : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Slave surface.
    interaction : :class:`compas_fea2.model.Interaction`
        Interaction type between master and slave.

    Attributes
    ----------
    master : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Master surface.
    slave : :class:`compas_fea2.model.FacesGroup`
        Group of element faces determining the Slave surface.
    interaction : :class:`compas_fea2.model.Interaction`
        Interaction type between master and slave.

    """

    def __init__(self, *, master, slave, interaction, **kwargs):
        super(ContactPair, self).__init__(**kwargs)
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
