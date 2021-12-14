
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase


class GroupBase(FEABase):

    """Initialises a base Set object.

    Parameters
    ----------
    name : str
        Name of the group.
    selection : list
        A list with either the Node or Element objects belonging to the set.
    """

    def __init__(self, name, selection):

        self.__name__ = 'Set'
        self._name = name
        self._selection = selection

    @property
    def name(self):
        """The name property."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def selection(self):
        """The selection property."""
        return self._selection

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class PartLevelGroup(GroupBase):
    def __init__(self, name, selection):
        super(PartLevelGroup, self).__init__(name, selection)
        self._part = None

    @property
    def part(self):
        """The part property."""
        return self._part


class NodesGroupBase(PartLevelGroup):
    def __init__(self, name, selection):
        super(NodesGroupBase, self).__init__(name, selection)


class ElementsGroupBase(PartLevelGroup):
    def __init__(self, name, selection, part):
        super(ElementsGroupBase, self).__init__(name, selection)


class PartsGroup(GroupBase):
    def __init__(self, name, selection):
        super(PartsGroup, self).__init__(name, selection)
        raise NotImplementedError()


class SurfaceBase(FEABase):
    pass
