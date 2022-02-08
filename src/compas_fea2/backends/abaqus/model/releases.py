from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import BeamEndRelease


class AbaqusBeamEndRelease(BeamEndRelease):
    def __init__(self, name, elem_end_dof):
        super(AbaqusBeamEndRelease).__init__(name=name)
        self.elem_end_dof = elem_end_dof

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data = ''
        for k, v in self.elem_end_dof.items():
            for end, dofs in v.items():
                data += '{},{},{}\n'.format(k, end, ','.join(dofs))
        return data
