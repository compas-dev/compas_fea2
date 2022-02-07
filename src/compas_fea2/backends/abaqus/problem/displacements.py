from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import GeneralDisplacementBase

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class GeneralDisplacement(GeneralDisplacementBase):

    def __init__(self, name, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=True):
        super(GeneralDisplacement, self).__init__(name, None, x, y, z, xx, yy, zz, axes)
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
        data_section = [f'** Name: {self.name} Type:  Displacement/Rotation\n',
                        f'*Boundary, OP={self._op}']
        for comp, dof in enumerate(dofs, 1):
            data_section += [f'{instance}.{node+1}, {comp}, {self.components[dof]}' for node in nodes if self.components[dof]]
        return '\n'.join(data_section) + '\n'
