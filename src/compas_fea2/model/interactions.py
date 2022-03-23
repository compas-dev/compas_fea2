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
    normal : str
        Behaviour of the contact along the direction normal to the interaction
        surface. For faceted surfaces, this is the behavior along the direction
        normal to each face.
    tangent :
        Behaviour of the contact along the directions tangent to the interaction
        surface. For faceted surfaces, this is the behavior along the directions
        tangent to each face.

    Attributes
    ----------
    normal : str
        Behaviour of the contact along the direction normal to the interaction
        surface. For faceted surfaces, this is the behavior along the direction
        normal to each face.
    tangent :
        Behaviour of the contact along the directions tangent to the interaction
        surface. For faceted surfaces, this is the behavior along the directions
        tangent to each face.
    """

    def __init__(self, *, normal, tangent, **kwargs):
        super(Contact, self).__init__(**kwargs)
        self._tangent = tangent
        self._normal = normal

    @property
    def tangent(self):
        return self._tangent

    @property
    def normal(self):
        return self._normal


class HardContactNoFriction(Contact):
    pass


class HardContactFrictionPenalty(Contact):
    """Hard contact interaction property with friction using a penalty
    formulation.

    Parameters
    ----------
    mu : float
        Friction coefficient for tangential behaviour.
    tollerance : float
        Slippage tollerance during contact.

    Attributes
    ----------
    mu : float
        Friction coefficient for tangential behaviour.
    tollerance : float
        Slippage tollerance during contact.
    """

    def __init__(self, name, mu, tollerance) -> None:
        super(HardContactFrictionPenalty, self).__init__(normal='HARD', tangent=mu)
        self.tollerance = tollerance
