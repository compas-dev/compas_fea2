from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class GeneralDisplacement(FEAData):
    """GeneralDisplacement object.

    Note
    ----
    Displacements are registered to a :class:`compas_fea2.problem.Step`.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
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
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
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
    """

    def __init__(self, x=0, y=0, z=0, xx=0, yy=0, zz=0, axes='global', name=None, **kwargs):
        super(GeneralDisplacement, self).__init__(name=name, **kwargs)
        self.x = x
        self.y = y
        self.z = z
        self.xx = xx
        self.yy = yy
        self.zz = zz
        self._axes = axes

    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value

    @property
    def components(self):
        return {c: getattr(self, c) for c in ['x', 'y', 'z', 'xx', 'yy', 'zz']}
