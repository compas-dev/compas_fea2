from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._base.model import BeamEndReleaseBase


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'BeamEndRelease',
]


class BeamEndRelease(BeamEndReleaseBase):
    def __init__(self, name, elem_end_dof):
        super(BeamEndRelease).__init__()
        self.elem_end_dof = elem_end_dof

    def _generate_data(self):
        data = ''
        for k, v in self.elem_end_dof.items():
            for end, dofs in v.items():
                data += '{},{},{}\n'.format(k, end, ','.join(dofs))
        return data
