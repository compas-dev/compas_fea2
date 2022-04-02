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


class BoundaryCondition(FEAData):
    """Base class for all zero-valued boundary conditions.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(BoundaryCondition, self).__init__(name=name, **kwargs)
        self.x = False
        self.y = False
        self.z = False
        self.xx = False
        self.yy = False
        self.zz = False


class FixedBC(BoundaryCondition):
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


class PinnedBC(BoundaryCondition):
    """A pinned nodal displacement boundary condition.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(PinnedBC, self).__init__(name=name, **kwargs)
        self.x = True
        self.y = True
        self.z = True


class FixedBCXX(BoundaryCondition):
    """A pinned nodal displacement boundary condition clamped in XX.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(FixedBCXX, self).__init__(name=name, **kwargs)
        self.x = True
        self.y = True
        self.z = True
        self.xx = True


class FixedBCYY(BoundaryCondition):
    """A pinned nodal displacement boundary condition clamped in YY.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(FixedBCYY, self).__init__(name=name, **kwargs)
        self.x = True
        self.y = True
        self.z = True
        self.yy = True


class FixedBCZZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition clamped in ZZ.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(FixedBCZZ, self).__init__(name=name, **kwargs)
        self.x = True
        self.y = True
        self.z = True
        self.zz = True


class RollerBCX(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in X.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCX, self).__init__(name=name, **kwargs)
        self.y = True
        self.z = True


class RollerBCY(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in Y.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCY, self).__init__(name=name, **kwargs)
        self.x = True
        self.z = True


class RollerBCZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in Z.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCZ, self).__init__(name=name, **kwargs)
        self.x = True
        self.y = True


class RollerBCXY(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in X and Y.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCXY, self).__init__(name=name, **kwargs)
        self.z = True


class RollerBCYZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in Y and Z.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCYZ, self).__init__(name=name, **kwargs)
        self.x = True


class RollerBCXZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in X and Z.
    """
    __doc__ += docs

    def __init__(self, name=None, **kwargs):
        super(RollerBCXZ, self).__init__(name=name, **kwargs)
        self.y = True
