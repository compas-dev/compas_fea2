from compas_fea2._base.base import FEABase


class ContactPairBase(FEABase):
    """Pair of master and slave surfaces to assign an interaction property

    Parameters
    ----------
    name : str
        name of the contanct pair
    master : obj
        type :class:`SurfaceBase` object to be used as master.
    slave : obj
        type :class:`SurfaceBase` object to be used as slave.
    str : name of a previusly defined :class:`InterfaceBase` object to
        define the type of interaction between master and slave.
    """

    def __init__(self, name, master, slave, interaction):
        self.__name__ = 'ContactPair'
        self._name = name
        self._master = master
        self._slave = slave
        self._interaction = interaction

    @property
    def name(self):
        """str : the name of the contact pair."""
        return self._name

    @property
    def master(self):
        """obj : type :class:`SurfaceBase` object to be used as master."""
        return self._master

    @property
    def slave(self):
        """obj : type :class:`SurfaceBase` object to be used as slave."""
        return self._slave

    @property
    def interaction(self):
        """str : name of a previusly defined :class:`InterfaceBase` object to
        define the type of interaction between master and slave."""
        return self._interaction

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)
