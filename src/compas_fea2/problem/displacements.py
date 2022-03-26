from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class GeneralDisplacement(FEAData):
    """GeneralDisplacement object.

    Parameters
    ----------
    x : float, optional
        x component of force, by default 0.
    y : float, optional
        y component of force, by default 0.
    z : float, optional
        z component of force, by default 0.
    xx : float, optional
        xx component of moment, by default 0.
    yy : float, optional
        yy component of moment, by default 0.
    zz : float, optional
        zz component of moment, by default 0.
    axes : str, optional
        BC applied via 'local' or 'global' axes, by default 'global'.

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
        x component of force, by default 0.
    y : float, optional
        y component of force, by default 0.
    z : float, optional
        z component of force, by default 0.
    xx : float, optional
        xx component of moment, by default 0.
    yy : float, optional
        yy component of moment, by default 0.
    zz : float, optional
        zz component of moment, by default 0.
    axes : str, optional
        BC applied via 'local' or 'global' axes, by default 'global'.
    """

    def __init__(self, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global', **kwargs):
        super(GeneralDisplacement, self).__init__(**kwargs)
        self._name = id(self)
        self.x = x
        self.y = y
        self.z = z
        self.xx = xx
        self.yy = yy
        self.zz = zz
        self.axes = axes

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
