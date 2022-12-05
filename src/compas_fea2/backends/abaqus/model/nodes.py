from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Node


# =============================================================================
# General
# =============================================================================

class AbaqusNode(Node):
    """Abaqus implementation of :class:`compas_fea2.model.Node`.

    Note
    ----
    The nodes key numbering in compas_fea2 starts from 0, while in Abaqus it starts
    from 1. The conversion in automatically resolved by compas_fea2.

    """
    __doc__ += Node.__doc__

    def __init__(self, xyz, mass=None, name=None, **kwargs):
        super(AbaqusNode, self).__init__(xyz=xyz, mass=mass, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        x, y, z = self.xyz
        return '{:>10}, {:>10.3f}, {:>10.3f}, {:>10.3f}'.format(self.key+1, x, y, z)
