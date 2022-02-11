from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class ContactPair(FEABase):
    """Pair of master and slave surfaces to assign an interaction property

    Parameters
    ----------
    name : str
        Name of the contact pair.
    master : :class:`compas_fea2.model.Surface`
        Master object.
    slave : :class:`compas_fea2.model.Surface`
        Slave object.
    interaction : str
        Name of a previusly defined :class:`compas_fea2.model.Interface` object to
        define the type of interaction between master and slave.

    """

    def __init__(self, name, *, master, slave, interaction):
        super(ContactPair, self).__init__(name=name)
        self._master = master
        self._slave = slave
        self._interaction = interaction

    @property
    def master(self):
        """:class:`compas_fea2.model.Surface` : object to be used as master."""
        return self._master

    @property
    def slave(self):
        """:class:`compas_fea2.model.Surface` : object to be used as slave."""
        return self._slave

    @property
    def interaction(self):
        """str : name of a :class:`compas_fea2.model.Interface` defining the type of interaction between master and slave.
        """
        return self._interaction
