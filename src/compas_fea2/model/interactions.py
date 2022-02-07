from compas_fea2.base import FEABase


class InteractionBase(FEABase):
    def __init__(self, name) -> None:
        self.__name__ = 'Interaction'
        self._name = name

    @property
    def name(self):
        """str : the name of the interaction property."""
        return self._name

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class ContactBase(InteractionBase):
    """General contact interaction between two parts.
    """

    def __init__(self, name, tangent, normal, tollerance) -> None:
        super(ContactBase, self).__init__(name)
        self._tangent = tangent
        self._normal = normal
        self._tollerance = tollerance

    @property
    def tangent(self):
        """The tangent property."""
        return self._tangent

    @property
    def normal(self):
        """The normal property."""
        return self._normal

    @property
    def tollerance(self):
        """float: slip tollerance."""
        return self._tollerance


class ContactNoFrictionBase():
    pass


class ContactHardFrictionPenaltyBase(ContactBase):
    """Hard contact interaction property with friction using a penalty
    formulation.
    """

    def __init__(self, name, mu, tollerance) -> None:
        super(ContactHardFrictionPenaltyBase, self).__init__(
            name=name, tangent=mu, normal='HARD', tollerance=tollerance)
