from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import GeneralDisplacement

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']

# TODO check if `modify` can be moved to _base


<<<<<<< HEAD
class AbaqusGeneralDisplacement(GeneralDisplacement):

    def __init__(self, name, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=True):
        super(AbaqusGeneralDisplacement, self).__init__(name, None, x, y, z, xx, yy, zz, axes)
=======
class GeneralDisplacement(GeneralDisplacementBase):
    """Abaqus implementation of the :class:`GeneralDisplacementBase`.\n
    """
    __doc__ += GeneralDisplacementBase.__doc__

    def __init__(self, name, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=True):
        super(GeneralDisplacement, self).__init__(name, x, y, z, xx, yy, zz, axes)
>>>>>>> 0fcf42ed8e1eb38788d736a3e47f207522be8a7c
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
