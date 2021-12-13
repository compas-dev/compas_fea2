from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase

__all__ = [
    'InstanceBase',
]


class InstanceBase(FEABase):
    """Initialises a base Instance object.

    Parameters
    ----------
    name : str
        Name of the set.
    part : obj
        The Part from which the instance is created.
    sets : list
        A list with the Set objects belonging to the instance.
    data : str
        The data block for the generation of the input file.
    """

    def __init__(self, name, part):
        self.__name__ = 'Instance'
        self._name = name
        self._part = part
        self._groups = {}

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.part.name)

    @property
    def name(self):
        """The name property."""
        return self._name

    @property
    def part(self):
        """The part property."""
        return self._part

    @property
    def groups(self):
        """The sets property."""
        return self._groups

    def add_group(self, group):
        if group not in self.groups:
            self._groups[group] = group

    def add_groups(self, groups):
        for group in groups:
            self.add_group(group)
