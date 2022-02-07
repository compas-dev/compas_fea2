from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class GeneralBCBase(FEABase):
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
        self.__name__ = 'GeneralBC'
        self._name = name
        self._components = components
        for c, a in self._components.items():
            if a is not None:
                setattr(self, '_' + c, a)
        self._axes = axes

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)

    @property
    def name(self):
        """str :  Name of the BC object."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

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


class FixedBCBase(GeneralBCBase):
    """A fixed nodal displacement boundary condition.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(FixedBCBase, self).__init__(name=name,  components={'x': 0, 'y': 0, 'z': 0,
                                                                  'xx': 0, 'yy': 0, 'zz': 0}, axes=axes)
        self.__name__ = 'FixedBC'


class PinnedBCBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(PinnedBCBase, self).__init__(name=name,  components={'x': 0, 'y': 0, 'z': 0}, axes=axes)
        self.__name__ = 'PinnedBC'


class FixedBCXXBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition clamped in XX.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(FixedBCXXBase, self).__init__(name=name,
                                            components={'x': 0, 'y': 0, 'z': 0, 'xx': 0}, axes=axes)
        self.__name__ = 'FixedBCXX'


class FixedBCYYBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition clamped in YY.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(FixedBCYYBase, self).__init__(name=name,
                                            components={'x': 0, 'y': 0, 'z': 0, 'yy': 0}, axes=axes)
        self.__name__ = 'FixedBCYY'


class FixedBCZZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition clamped in ZZ.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(FixedBCZZBase, self).__init__(name=name,
                                            components={'x': 0, 'y': 0, 'z': 0, 'zz': 0}, axes=axes)
        self.__name__ = 'FixedBCZZ'


class RollerBCXBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in X.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(RollerBCXBase, self).__init__(name=name,  components={'y': 0, 'z': 0}, axes=axes)
        self.__name__ = 'RollerBCX'


class RollerBCYBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in Y.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(RollerBCYBase, self).__init__(name=name,  components={'x': 0, 'z': 0}, axes=axes)
        self.__name__ = 'RollerBCY'


class RollerBCZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in Z.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(RollerBCZBase, self).__init__(name=name,  components={'x': 0, 'y': 0}, axes=axes)
        self.__name__ = 'RollerBCZ'


class RollerBCXYBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in X and Y.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(RollerBCXYBase, self).__init__(name=name,  components={'z': 0}, axes=axes)

        self.__name__ = 'RollerBCXY'


class RollerBCYZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in Y and Z.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(RollerBCYZBase, self).__init__(name=name,  components={'x': 0}, axes=axes)
        self.__name__ = 'RollerBCYZ'


class RollerBCXZBase(GeneralBCBase):
    """A pinned nodal displacement boundary condition released in X and Z.

    """
    __doc__ += GeneralBCBase.__doc__

    def __init__(self, name,  axes):
        super(RollerBCXZBase, self).__init__(name=name,  components={'y': 0}, axes=axes)
        self.__name__ = 'RollerBCXZ'
