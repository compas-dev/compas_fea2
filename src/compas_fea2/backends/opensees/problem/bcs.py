from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem import GeneralDisplacementBase
from compas_fea2.backends._base.problem import FixedDisplacementBase
from compas_fea2.backends._base.problem import PinnedDisplacementBase
from compas_fea2.backends._base.problem import FixedDisplacementXXBase
from compas_fea2.backends._base.problem import FixedDisplacementYYBase
from compas_fea2.backends._base.problem import FixedDisplacementZZBase
from compas_fea2.backends._base.problem import RollerDisplacementXBase
from compas_fea2.backends._base.problem import RollerDisplacementYBase
from compas_fea2.backends._base.problem import RollerDisplacementZBase
from compas_fea2.backends._base.problem import RollerDisplacementXYBase
from compas_fea2.backends._base.problem import RollerDisplacementYZBase
from compas_fea2.backends._base.problem import RollerDisplacementXZBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

# TODO: add the possibility to add bcs to nodes/elements and not only to sets

__all__ = [
    # 'GeneralDisplacement',
    'FixedDisplacement',
    # 'PinnedDisplacement',
    # 'FixedDisplacementXX',
    # 'FixedDisplacementYY',
    # 'FixedDisplacementZZ',
    # 'RollerDisplacementX',
    # 'RollerDisplacementY',
    # 'RollerDisplacementZ',
    # 'RollerDisplacementXY',
    # 'RollerDisplacementYZ',
    # 'RollerDisplacementXZ'
]

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


def _generate_jobdata(obj):
    jobdata = []
    for nk in obj.nodes:
        jobdata.append('fix {} {}'.format(nk, ' '.join(
            ['1' if obj.components[dof] is not None else '0' for dof in dofs])))  # dofs[:obj.ndof]
    return '\n'.join(jobdata)


class FixedDisplacement(FixedDisplacementBase):

    def __init__(self, name, nodes, axes='global'):
        super(FixedDisplacement, self).__init__(name, nodes, axes)
        self._jobdata = self._generate_jobdata()

    def _generate_jobdata(self):
        return _generate_jobdata(self)


if __name__ == "__main__":
    pass
