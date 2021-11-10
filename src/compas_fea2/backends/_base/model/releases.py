
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

from compas_fea2.backends._base.base import FEABase

__all__ = [
    'BeamEndReleaseBase',
]


class BeamEndReleaseBase(FEABase):
    """Initialises base Constraint object.

    Parameters
    ----------
    name : str
        Name of the BeamEndRelease object.

    Attributes
    ----------
    name : str
        Name of the BeamEndRelease object.
    """

    def __init__(self):
        self.__name__ = 'ReleaseObject'
