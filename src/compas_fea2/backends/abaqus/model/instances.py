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
    sets : list
        A list with the Set objects belonging to the instance.
    data : str
        The data block for the generation of the input file.
    """

    def __init__(self, name, part, sets=[]):
        super(Instance, self).__init__(name, part, sets)
        for iset in sets:
            iset.instance = self.name
            iset._jobdata = iset._generate_jobdata()

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        section_data = ['*Instance, name={}, part={}\n'.format(self.name, self.part.name)]
        section_data.append('*End Instance\n**\n')
        return ''.join(section_data)
