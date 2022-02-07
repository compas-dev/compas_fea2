
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class GroupBase(FEABase):
    """Initialises a base Set object.

    Parameters
    ----------
    name : str
        Name of the group.
    selection : list
        A list with either the Node or Element objects belonging to the set.

    """

    def __init__(self, name, keys):
        self.__name__ = 'Group'
        self._name = name
        self._keys = keys

    @property
    def name(self):
        """The name property."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def keys(self):
        """The selection property."""
        return self._keys

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class NodesGroupBase(GroupBase):
    def __init__(self, name, nodes_keys):
        super(NodesGroupBase, self).__init__(name, nodes_keys)


class ElementsGroupBase(GroupBase):
    def __init__(self, name, elements_keys):
        super(ElementsGroupBase, self).__init__(name, elements_keys)


class PartsGroup(GroupBase):
    def __init__(self, name, parts_names):
        super(PartsGroup, self).__init__(name, parts_names)
        raise NotImplementedError()
