from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem import GeneralDisplacementBase
# Author(s): Francesco Ranaudo (github.com/franaudo)

# TODO: add the possibility to add bcs to nodes/elements and not only to sets

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class GeneralDisplacement(GeneralDisplacementBase):

    def __init__(self, name, bset, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        super(GeneralDisplacement, self).__init__(name, None, x, y, z, xx, yy, zz, axes)
        self.bset = bset
        self._modify = True

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = []
        line = ("** Name: {} Type: Displacement/Rotation\n"
                "*Boundary, op=NEW").format(self.name)
        data_section.append(line)
        c = 1
        for dof in dofs:
            if dof in self._components.keys() and self._components[dof] != None:
                if not self.components[dof]:
                    line = """{}, {}, {}""".format(self.bset, c, c)
                else:
                    line = """{}, {}, {}, {}""".format(self.bset, c, c, self._components[dof])
                data_section.append(line)
            c += 1
        return '\n'.join(data_section) + '\n'
