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
        super(AbaqusGeneralDisplacement, self).__init__(name, None, x, y, z, xx, yy, zz, axes, name=name, **kwargs)
        self._op = 'NEW' if modify else 'MOD'

    def _generate_jobdata(self, instance, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = ['** Name: {} Type:  Displacement/Rotation\n'.format(self.name),
                        '*Boundary, OP={}'.format(self._op)]
        for comp, dof in enumerate(dofs, 1):
            data_section += ['{}.{}, {}, {}'.format(instance, node.key+1, comp, self.components[dof]) for node in nodes if self.components[dof]]
        return '\n'.join(data_section)
