from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class BoundaryCondition(FEAData):
    """Base class for all zero-valued boundary conditions.

    Parameters
    ----------
    axes : str, optional
        The refernce axes.

    Attributes
    ----------
    x : bool
        Restrain translations along the x axis.
    y : bool
        Restrain translations along the y axis.
    z : bool
        Restrain translations along the z axis.
    xx : bool
        Restrain rotations around the x axis.
    yy : bool
        Restrain rotations around the y axis.
    zz : bool
        Restrain rotations around the z axis.
    components : dict
        Dictionary with component-value pairs summarizing the boundary condition.
    axes : str
        The reference axes.

    Notes
    -----
    BoundaryConditions are registered to a :class:`compas_fea2.model.Model`.

    Warnings
    --------
    The `axes` parameter is WIP. Currently only global axes can be used.

    """

    def __init__(self, axes="global", **kwargs):
        super(BoundaryCondition, self).__init__(**kwargs)
        self._axes = axes
        self._x = False
        self._y = False
        self._z = False
        self._xx = False
        self._yy = False
        self._zz = False

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def xx(self):
        return self._xx

    @property
    def yy(self):
        return self._yy

    @property
    def zz(self):
        return self._zz

    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value

    @property
    def components(self):
        return {c: getattr(self, c) for c in ["x", "y", "z", "xx", "yy", "zz"]}


class GeneralBC(BoundaryCondition):
    """Customized boundary condition.

    Parameters
    ----------
    x : bool
        Restrain translations along the x axis.
    y : bool
        Restrain translations along the y axis.
    z : bool
        Restrain translations along the z axis.
    xx : bool
        Restrain rotations around the x axis.
    yy : bool
        Restrain rotations around the y axis.
    zz : bool
        Restrain rotations around the z axis.

    """

    def __init__(self, x=False, y=False, z=False, xx=False, yy=False, zz=False, **kwargs):
        super(GeneralBC, self).__init__(**kwargs)
        self._x = x
        self._y = y
        self._z = z
        self._xx = xx
        self._yy = yy
        self._zz = zz


class FixedBC(BoundaryCondition):
    """A fixed nodal displacement boundary condition."""

    def __init__(self, **kwargs):
        super(FixedBC, self).__init__(**kwargs)
        self._x = True
        self._y = True
        self._z = True
        self._xx = True
        self._yy = True
        self._zz = True


class PinnedBC(BoundaryCondition):
    """A pinned nodal displacement boundary condition."""

    def __init__(self, **kwargs):
        super(PinnedBC, self).__init__(**kwargs)
        self._x = True
        self._y = True
        self._z = True


class ClampBCXX(PinnedBC):
    """A pinned nodal displacement boundary condition clamped in XX."""

    def __init__(self, **kwargs):
        super(ClampBCXX, self).__init__(**kwargs)
        self._xx = True


class ClampBCYY(PinnedBC):
    """A pinned nodal displacement boundary condition clamped in YY."""

    def __init__(self, **kwargs):
        super(ClampBCYY, self).__init__(**kwargs)
        self._yy = True


class ClampBCZZ(PinnedBC):
    """A pinned nodal displacement boundary condition clamped in ZZ."""

    def __init__(self, **kwargs):
        super(ClampBCZZ, self).__init__(**kwargs)
        self._zz = True


class RollerBCX(PinnedBC):
    """A pinned nodal displacement boundary condition released in X."""

    def __init__(self, **kwargs):
        super(RollerBCX, self).__init__(**kwargs)
        self._x = False


class RollerBCY(PinnedBC):
    """A pinned nodal displacement boundary condition released in Y."""

    def __init__(self, **kwargs):
        super(RollerBCY, self).__init__(**kwargs)
        self._y = False


class RollerBCZ(PinnedBC):
    """A pinned nodal displacement boundary condition released in Z."""

    def __init__(self, **kwargs):
        super(RollerBCZ, self).__init__(**kwargs)
        self._z = False


class RollerBCXY(PinnedBC):
    """A pinned nodal displacement boundary condition released in X and Y."""

    def __init__(self, **kwargs):
        super(RollerBCXY, self).__init__(**kwargs)
        self._x = False
        self._y = False


class RollerBCYZ(PinnedBC):
    """A pinned nodal displacement boundary condition released in Y and Z."""

    def __init__(self, **kwargs):
        super(RollerBCYZ, self).__init__(**kwargs)
        self._y = False
        self._z = False


class RollerBCXZ(PinnedBC):
    """A pinned nodal displacement boundary condition released in X and Z."""

    def __init__(self, name=None, **kwargs):
        super(RollerBCXZ, self).__init__(name=name, **kwargs)
        self._x = False
        self._z = False
