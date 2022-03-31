from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import Node


class OpenseesNode(Node):
    """Opensees implementation of the :class:`Node`. \n
    """
    __doc__ += Node.__doc__

    def __init__(self, xyz, part=None, name=None, **kwargs):
        super(OpenseesNode, self).__init__(xyz=xyz, part=part, name=name, **kwargs)

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
        # FIXME: the approximation on the floating point is not correct because it depends on the units
        return '{0}{1}{2}{3:.3f}{2}{4:.3f}{2}{5:.3f}'.format('node ', self.key, ' ', x, y, z)
