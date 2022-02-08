from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class Group(FEABase):
    """Initialises a base Set object.

    Parameters
    ----------
    name : str
        Name of the group.
    selection : list
        A list with either the Node or Element objects belonging to the set.

    """

    def __init__(self, name, keys):
        super(Group, self).__init__(name=name)
        self._keys = keys

    @property
    def keys(self):
        """The selection property."""
        return self._keys


class NodesGroup(Group):
    def __init__(self, name, nodes_keys):
        super(NodesGroup, self).__init__(name, nodes_keys)


class ElementsGroup(Group):
    def __init__(self, name, elements_keys):
        super(ElementsGroup, self).__init__(name, elements_keys)


class PartsGroup(Group):
    def __init__(self, name, parts_names):
        super(PartsGroup, self).__init__(name, parts_names)
