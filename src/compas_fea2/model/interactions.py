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
    tangent : :class:`compas.geometry.Vector`
        ???
    normal : :class:`compas.geometry.Vector`
        ???
    tol : float

    Attributes
    ----------
    tangent : :class:`compas.geometry.Vector`
        ???
    normal : :class:`compas.geometry.Vector`
        ???
    tol : float

    """

    def __init__(self, *, tangent, normal, tol, **kwargs):
        super(Contact, self).__init__(**kwargs)
        self._tangent = tangent
        self._normal = normal
        self._tol = tol

    @property
    def tangent(self):
        return self._tangent

    @property
    def normal(self):
        return self._normal

    @property
    def tol(self):
        return self._tol


class ContactNoFrictionBase(Contact):
    """"""


class ContactHardFrictionPenalty(Contact):
    """Hard contact interaction property with friction using a penalty formulation.
    """

    def __init__(self, *, mu, tol, **kwargs):
        super(ContactHardFrictionPenalty, self).__init__(tangent=mu, normal='HARD', tol=tol, **kwargs)
