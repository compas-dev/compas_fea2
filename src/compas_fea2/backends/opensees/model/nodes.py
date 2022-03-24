from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import Node


class Node(Node):
    """Opensees implementation of the :class:`Node`. \n
    """
    __doc__ += Node.__doc__

    def __init__(self, xyz, ex=None, ey=None, ez=None, mass=None, name=None):
        super(Node, self).__init__(xyz=xyz, ex=ex, ey=ey, ez=ez, mass=mass, name=name)

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
        return '{0}{1}{2}{3:.3f}{2}{4:.3f}{2}{5:.3f}'.format('node ', self.key, ' ', x, y, z)
