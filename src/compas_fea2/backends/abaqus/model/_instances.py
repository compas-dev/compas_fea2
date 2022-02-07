from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class _Instance(FEABase):
    """Initialises a base Instance object.

    Note
    ----
    This is a abaqus specific class.

    Parameters
    ----------
    name : str
        Name of the set.
    part : obj
        The Part from which the instance is created.
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
        if group.name not in self.groups:
            self._groups[group.name] = group

    def add_groups(self, groups):
        for group in groups:
            self.add_group(group)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return ''.join([f'*Instance, name={self.name}, part={self.part.name}\n',
                        '*End Instance\n**\n'])
