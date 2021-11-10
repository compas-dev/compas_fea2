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

    def __init__(self, name, part, sets):
        self.__name__ = 'Instance'
        self.name = name
        self.part = part
        self.sets = sets

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.part.name)


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass
