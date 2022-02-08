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
    components : dict
        BC components.
    axes : str, optional
        BC applied via 'local' or 'global' axes, by default 'global'.

    """

    def __init__(self, name,  components, axes):
        super(GeneralBC, self).__init__(name=name)

        self._components = components
        for c, a in self._components.items():
            if a is not None:
                setattr(self, '_' + c, a)
        self._axes = axes

    @property
    def components(self):
        """dict : Values of x, y, z, xx, yy, zz degrees-of-freedom."""
        return self._components

    @property
    def axes(self):
        """str : 'local' or 'global' coordinate axes."""
        return self._axes

    @axes.setter
    def axes(self, value):
        self._axes = value

    def _set_component_attribute(self):
        """set the components attribute from the components dictionary
        """
        for c, a in self.components:
            setattr(self, c, a)


class FixedBC(GeneralBC):
    """A fixed nodal displacement boundary condition.
    """

    def __init__(self, name,  axes):
        components = {'x': 0, 'y': 0, 'z': 0, 'xx': 0, 'yy': 0, 'zz': 0}
        super(FixedBC, self).__init__(name=name,  components=components, axes=axes)


class PinnedBC(GeneralBC):
    """A pinned nodal displacement boundary condition.
    """

    def __init__(self, name,  axes):
        components = {'x': 0, 'y': 0, 'z': 0}
        super(PinnedBC, self).__init__(name=name,  components=components, axes=axes)


class FixedBCXX(GeneralBC):
    """A pinned nodal displacement boundary condition clamped in XX.
    """

    def __init__(self, name,  axes):
        components = {'x': 0, 'y': 0, 'z': 0, 'xx': 0}
        super(FixedBCXX, self).__init__(name=name, components=components, axes=axes)


class FixedBCYY(GeneralBC):
    """A pinned nodal displacement boundary condition clamped in YY.
    """

    def __init__(self, name,  axes):
        components = {'x': 0, 'y': 0, 'z': 0, 'yy': 0}
        super(FixedBCYY, self).__init__(name=name, components=components, axes=axes)


class FixedBCZZ(GeneralBC):
    """A pinned nodal displacement boundary condition clamped in ZZ.
    """

    def __init__(self, name,  axes):
        components = {'x': 0, 'y': 0, 'z': 0, 'zz': 0}
        super(FixedBCZZ, self).__init__(name=name, components=components, axes=axes)


class RollerBCX(GeneralBC):
    """A pinned nodal displacement boundary condition released in X.
    """

    def __init__(self, name,  axes):
        super(RollerBCX, self).__init__(name=name,  components={'y': 0, 'z': 0}, axes=axes)


class RollerBCY(GeneralBC):
    """A pinned nodal displacement boundary condition released in Y.
    """

    def __init__(self, name,  axes):
        super(RollerBCY, self).__init__(name=name,  components={'x': 0, 'z': 0}, axes=axes)


class RollerBCZ(GeneralBC):
    """A pinned nodal displacement boundary condition released in Z.
    """

    def __init__(self, name,  axes):
        super(RollerBCZ, self).__init__(name=name,  components={'x': 0, 'y': 0}, axes=axes)


class RollerBCXY(GeneralBC):
    """A pinned nodal displacement boundary condition released in X and Y.
    """

    def __init__(self, name,  axes):
        super(RollerBCXY, self).__init__(name=name,  components={'z': 0}, axes=axes)


class RollerBCYZ(GeneralBC):
    """A pinned nodal displacement boundary condition released in Y and Z.
    """

    def __init__(self, name,  axes):
        super(RollerBCYZ, self).__init__(name=name,  components={'x': 0}, axes=axes)


class RollerBCXZ(GeneralBC):
    """A pinned nodal displacement boundary condition released in X and Z.
    """

    def __init__(self, name,  axes):
        super(RollerBCXZ, self).__init__(name=name,  components={'y': 0}, axes=axes)
