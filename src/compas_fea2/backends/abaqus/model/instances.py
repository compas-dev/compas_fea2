from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model import InstanceBase

# __all__ = [
#     'Instance',
# ]

# FIXME this does not make much sense: why the iset are called like that?


class Instance(InstanceBase):
    """Initialises an Instance object.

    Parameters
    ----------
    name : str
        Name of the set.
    part : obj
        The Part from which the instance is created.
    """

    def __init__(self, name, part):
        super(Instance, self).__init__(name, part)

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
