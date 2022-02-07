from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import BeamEndReleaseBase


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'BeamEndRelease',
]


class BeamEndRelease(BeamEndReleaseBase):
    def __init__(self, name, elem_end_dof):
        super(BeamEndRelease).__init__()
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
