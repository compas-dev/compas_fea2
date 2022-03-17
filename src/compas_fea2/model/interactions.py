from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Interaction(FEAData):
    """Base class for all interactions.
    """

    def __init__(self, **kwargs):
        super(Interaction, self).__init__(**kwargs)


class Contact(Interaction):
    """General contact interaction between two parts.

    Parameters
    ----------
    tangent :
        tangent behaviour
    normal :
        normal behaviour

    Attributes
    ----------
    tangent :
        tangent behaviour
    normal :
        normal behaviour
    """

    def __init__(self, *, tangent, normal, **kwargs):
        super(Contact, self).__init__(**kwargs)
        self._tangent = tangent
        self._normal = normal

    @property
    def tangent(self):
        return self._tangent

    @property
    def normal(self):
        return self._normal


class ContactNoFrictionBase(Contact):
    """"""


class ContactHardFrictionPenalty(Contact):
    """Hard contact interaction property with friction using a penalty
    formulation.

    Parameters
    ----------
    name : str
        name of the Contact property
    mu : float
        friction coefficient, usually less than 1.
    tollerance : float
        slip tollerance
    """

    def __init__(self, name, mu, tollerance) -> None:
        super(ContactHardFrictionPenalty, self).__init__(
            name=name, tangent=mu, normal='HARD')
        self._tol = tollerance

    @property
    def tollerance(self):
        return self._tol
