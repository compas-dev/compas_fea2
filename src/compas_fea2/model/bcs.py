from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class BoundaryCondition(FEAData):
    """Base class for all boundary conditions.
    """

    def __init__(self, **kwargs):
        super(BoundaryCondition, self).__init__(**kwargs)
        self.x = 0
        self.y = 0
        self.z = 0
        self.xx = 0
        self.yy = 0
        self.zz = 0


class FixedBC(BoundaryCondition):
    """A fixed nodal displacement boundary condition.
    """

    def __init__(self, **kwargs):
        super(FixedBC, self).__init__(**kwargs)
        self.x = 1
        self.y = 1
        self.z = 1
        self.xx = 1
        self.yy = 1
        self.zz = 1


class PinnedBC(BoundaryCondition):
    """A pinned nodal displacement boundary condition.
    """

    def __init__(self, **kwargs):
        super(PinnedBC, self).__init__(**kwargs)
        self.x = 1
        self.y = 1
        self.z = 1


class FixedBCXX(BoundaryCondition):
    """A pinned nodal displacement boundary condition clamped in XX.
    """

    def __init__(self, **kwargs):
        super(FixedBCXX, self).__init__(**kwargs)
        self.x = 1
        self.y = 1
        self.z = 1
        self.xx = 1


class FixedBCYY(BoundaryCondition):
    """A pinned nodal displacement boundary condition clamped in YY.
    """

    def __init__(self, **kwargs):
        super(FixedBCYY, self).__init__(**kwargs)
        self.x = 1
        self.y = 1
        self.z = 1
        self.yy = 1


class FixedBCZZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition clamped in ZZ.
    """

    def __init__(self, **kwargs):
        super(FixedBCZZ, self).__init__(**kwargs)
        self.x = 1
        self.y = 1
        self.z = 1
        self.zz = 1


class RollerBCX(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in X.
    """

    def __init__(self, **kwargs):
        super(RollerBCX, self).__init__(**kwargs)
        self.y = 1
        self.z = 1


class RollerBCY(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in Y.
    """

    def __init__(self, **kwargs):
        super(RollerBCY, self).__init__(**kwargs)
        self.x = 1
        self.z = 1


class RollerBCZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in Z.
    """

    def __init__(self, **kwargs):
        super(RollerBCZ, self).__init__(**kwargs)
        self.x = 1
        self.y = 1


class RollerBCXY(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in X and Y.
    """

    def __init__(self, **kwargs):
        super(RollerBCXY, self).__init__(**kwargs)
        self.z = 1


class RollerBCYZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in Y and Z.
    """

    def __init__(self, **kwargs):
        super(RollerBCYZ, self).__init__(**kwargs)
        self.x = 1


class RollerBCXZ(BoundaryCondition):
    """A pinned nodal displacement boundary condition released in X and Z.
    """

    def __init__(self, **kwargs):
        super(RollerBCXZ, self).__init__(**kwargs)
        self.y = 1
