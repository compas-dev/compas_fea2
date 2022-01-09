from compas_fea2.backends._base.base import FEABase


class ContactBase(FEABase):
    def __init__(self, name, master, slave, interaction):
        self._name = name
        self._master = master
        self._slave = slave
        self._interaction = interaction
