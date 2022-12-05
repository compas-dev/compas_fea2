from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import GeneralDisplacement

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']

# TODO check if `modify` can be moved to _base


class AbaqusGeneralDisplacement(GeneralDisplacement):
    """Abaqus implementation of :class:`GeneralDisplacement`.\n"""
    __doc__ += GeneralDisplacement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    modify : bool, optional
        If ``True``, change previous displacements applied at the same location, otherwise
        add the displacement to the previous. By defult is ``True``.
    """

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=True, name=None, **kwargs):
        super(AbaqusGeneralDisplacement, self).__init__(
            x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)
        self._modify = ', OP=MOD' if modify else ', OP=NEW'

    def _generate_jobdata(self, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = ['** Name: {} Type:  Displacement/Rotation'.format(self.name),
                        '*Boundary{}'.format(self._modify)]
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if getattr(self, dof):
                    data_section += ['{0}-1.{1}, {2}, {2}, {3}'.format(
                        node.part.name, node.key+1, comp, self.components[dof])]
        return '\n'.join(data_section)
