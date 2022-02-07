from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.bcs import GeneralBCBase


class GeneralDisplacementBase(GeneralBCBase):
    """GeneralDisplacement object.

    Parameters
    ----------
    name : str
        Name of the BC object.
    x : float, optional
        x component of force, by default `None`.
    y : float, optional
        y component of force, by default `None`.
    z : float, optional
        z component of force, by default `None`.
    xx : float, optional
        xx component of moment, by default `None`.
    yy : float, optional
        yy component of moment, by default `None`.
    zz : float, optional
        zz component of moment, by default `None`.
    axes : str, optional
        BC applied via 'local' or 'global' axes, by default 'global'.
    """

    def __init__(self, name, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        super(GeneralDisplacementBase, self).__init__(name=name,
                                                      components={'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz},
                                                      axes=axes)
