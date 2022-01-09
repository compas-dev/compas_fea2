from compas_fea2.backends._base.base import FEABase


class InterfaceBase():
    def __init__(self) -> None:
        self._master = None
        self._slave = None


class ContactBase(FEABase):
    def __init__(self, name) -> None:
        self._name = name


class ContactNoFrictionBase():
    pass


class ContactHardFrictionPenaltyBase(ContactBase):
    def __init__(self, name, mu, slip_tollerance) -> None:
        super(ContactHardFrictionPenaltyBase, self).__init__(name)
        self._slip_tollerance = slip_tollerance
        self._mu = mu
        self._normal = 'HARD'
