from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class GeneralBC(FEABase):
    """Boundary Condtion object.

    Parameters
    ----------
    name : str
        Name of the BC object.

    """

    def __init__(self, name):
        super(GeneralBC, self).__init__(name=name)
        self.x = 0
        self.y = 0
        self.z = 0
        self.xx = 0
        self.yy = 0
        self.zz = 0


class FixedBC(GeneralBC):
    """A fixed nodal displacement boundary condition.
    """

    def __init__(self, name):
        super(FixedBC, self).__init__(name=name)
        self.x = 1
        self.y = 1
        self.z = 1
        self.xx = 1
        self.yy = 1
        self.zz = 1


class PinnedBC(GeneralBC):
    """A pinned nodal displacement boundary condition.
    """

    def __init__(self, name):
        super(PinnedBC, self).__init__(name=name)
        self.x = 1
        self.y = 1
        self.z = 1


class FixedBCXX(GeneralBC):
    """A pinned nodal displacement boundary condition clamped in XX.
    """

    def __init__(self, name):
        super(FixedBCXX, self).__init__(name=name)
        self.x = 1
        self.y = 1
        self.z = 1
        self.xx = 1


class FixedBCYY(GeneralBC):
    """A pinned nodal displacement boundary condition clamped in YY.
    """

    def __init__(self, name):
        super(FixedBCYY, self).__init__(name=name)
        self.x = 1
        self.y = 1
        self.z = 1
        self.yy = 1


class FixedBCZZ(GeneralBC):
    """A pinned nodal displacement boundary condition clamped in ZZ.
    """

    def __init__(self, name):
        super(FixedBCZZ, self).__init__(name=name)
        self.x = 1
        self.y = 1
        self.z = 1
        self.zz = 1


class RollerBCX(GeneralBC):
    """A pinned nodal displacement boundary condition released in X.
    """

    def __init__(self, name):
        super(RollerBCX, self).__init__(name=name)
        self.y = 1
        self.z = 1


class RollerBCY(GeneralBC):
    """A pinned nodal displacement boundary condition released in Y.
    """

    def __init__(self, name):
        super(RollerBCY, self).__init__(name=name)
        self.x = 1
        self.z = 1


class RollerBCZ(GeneralBC):
    """A pinned nodal displacement boundary condition released in Z.
    """

    def __init__(self, name):
        super(RollerBCZ, self).__init__(name=name)
        self.x = 1
        self.y = 1


class RollerBCXY(GeneralBC):
    """A pinned nodal displacement boundary condition released in X and Y.
    """

    def __init__(self, name):
        super(RollerBCXY, self).__init__(name=name)
        self.z = 1


class RollerBCYZ(GeneralBC):
    """A pinned nodal displacement boundary condition released in Y and Z.
    """

    def __init__(self, name):
        super(RollerBCYZ, self).__init__(name=name)
        self.x = 1


class RollerBCXZ(GeneralBC):
    """A pinned nodal displacement boundary condition released in X and Z.
    """

    def __init__(self, name):
        super(RollerBCXZ, self).__init__(name=name)
        self.y = 1