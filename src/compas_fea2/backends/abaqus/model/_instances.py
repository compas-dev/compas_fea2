from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _Instance(FEAData):
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

    Attributes
    ----------
    name : str
        Name of the set.
    part : obj
        The Part from which the instance is created.
    groups : dict
        Dictionary with the instance level sets.

    """

    def __init__(self, name, part, **kwargs):
        super(_Instance, self).__init__(name=name, **kwargs)
        self._part = part
        self._groups = {}  # TODO consider to change to set

    @property
    def part(self):
        return self._part

    @property
    def groups(self):
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
        return '\n'.join(['*Instance, name={}, part={}'.format(self.name, self.part.name),
                          '*End Instance\n**\n'])
