from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData

docs = """
Parameters
----------
name : str, optional
    Uniqe identifier. If not provided it is automatically generated. Set a
    name if you want a more human-readable input file.

Attributes
----------
name : str
    Uniqe identifier. If not provided it is automatically generated. Set a
    name if you want a more human-readable input file.
x : bool
    If True, tralations along global x are fixed.
y : bool
    If True, tralations along global y are fixed.
z : bool
    If True, tralations along global z are fixed.
xx : bool
    If True, tralations around global xx are fixed.
yy : bool
    If True, tralations around global yy are fixed.
zz : bool
    If True, tralations around global zz are fixed.

"""


class _BoundaryCondition(FEAData):
    """Base class for all zero-valued boundary conditions.

    Note
    ----
    BoundaryConditions are registered to a :class:`compas_fea2.model.Model`.
    """
    __doc__ += docs

    def __init__(self, axes='global', name=None, **kwargs):
        super(_BoundaryCondition, self).__init__(name=name, **kwargs)
        self._axes = axes
        self.x = False
        self.y = False
        self.z = False
        self.xx = False
        self.yy = False
        self.zz = False

    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value

    @property
    def components(self):
        return {c: getattr(self, c) for c in ['x', 'y', 'z', 'xx', 'yy', 'zz']}


class GeneralBC(_BoundaryCondition):
    """Costumized boundary condition.
    """
    __doc__ += docs

    def __init__(self, name=None, x=False, y=False, z=False, xx=False, yy=False, zz=False, **kwargs):
        super(GeneralBC, self).__init__(name=name, **kwargs)
        self.x = x
        self.y = y
        self.z = z
        self.xx = xx
        self.yy = yy
        self.zz = zz


class FixedBC(_BoundaryCondition):
    """A fixed nodal displacement boundary condition.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(FixedBC, self).__init__(name=name, **kwargs)
        self.x = True
        self.y = True
        self.z = True
        self.xx = True
        self.yy = True
        self.zz = True


class PinnedBC(_BoundaryCondition):
    """A pinned nodal displacement boundary condition.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(PinnedBC, self).__init__(name=name, **kwargs)
        self.x = True
        self.y = True
        self.z = True


class ClampBCXX(PinnedBC):
    """A pinned nodal displacement boundary condition clamped in XX.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(ClampBCXX, self).__init__(name=name, **kwargs)
        self.xx = True


class ClampBCYY(PinnedBC):
    """A pinned nodal displacement boundary condition clamped in YY.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(ClampBCYY, self).__init__(name=name, **kwargs)
        self.yy = True


class ClampBCZZ(PinnedBC):
    """A pinned nodal displacement boundary condition clamped in ZZ.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(ClampBCZZ, self).__init__(name=name, **kwargs)
        self.zz = True


class RollerBCX(PinnedBC):
    """A pinned nodal displacement boundary condition released in X.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCX, self).__init__(name=name, **kwargs)
        self.x = False


class RollerBCY(PinnedBC):
    """A pinned nodal displacement boundary condition released in Y.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCY, self).__init__(name=name, **kwargs)
        self.y = False


class RollerBCZ(PinnedBC):
    """A pinned nodal displacement boundary condition released in Z.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCZ, self).__init__(name=name, **kwargs)
        self.z = False


class RollerBCXY(PinnedBC):
    """A pinned nodal displacement boundary condition released in X and Y.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCXY, self).__init__(name=name, **kwargs)
        self.x = False
        self.y = False


class RollerBCYZ(PinnedBC):
    """A pinned nodal displacement boundary condition released in Y and Z.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCYZ, self).__init__(name=name, **kwargs)
        self.y = False
        self.z = False


class RollerBCXZ(PinnedBC):
    """A pinned nodal displacement boundary condition released in X and Z.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCXZ, self).__init__(name=name, **kwargs)
        self.x = False
        self.z = False
