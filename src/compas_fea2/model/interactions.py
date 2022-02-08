from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class Interaction(FEABase):
    def __init__(self, name):
        super(Interaction, self).__init__(name=name)


class Contact(Interaction):
    """General contact interaction between two parts.
    """

    def __init__(self, name, tangent, normal, tollerance) -> None:
        super(Contact, self).__init__(name)
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


class ContactNoFrictionBase(Contact):
    pass


class ContactHardFrictionPenalty(Contact):
    """Hard contact interaction property with friction using a penalty formulation.
    """

    def __init__(self, name, mu, tollerance):
        super(ContactHardFrictionPenalty, self).__init__(name=name, tangent=mu, normal='HARD', tollerance=tollerance)
