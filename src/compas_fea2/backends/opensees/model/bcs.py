from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model import GeneralBCBase
from compas_fea2.backends._base.model import FixedBCBase
from compas_fea2.backends._base.model import PinnedBCBase
from compas_fea2.backends._base.model import FixedBCXXBase
from compas_fea2.backends._base.model import FixedBCYYBase
from compas_fea2.backends._base.model import FixedBCZZBase
from compas_fea2.backends._base.model import RollerBCXBase
from compas_fea2.backends._base.model import RollerBCYBase
from compas_fea2.backends._base.model import RollerBCZBase
from compas_fea2.backends._base.model import RollerBCXYBase
from compas_fea2.backends._base.model import RollerBCYZBase
from compas_fea2.backends._base.model import RollerBCXZBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

# TODO: add the possibility to add bcs to nodes/elements and not only to sets

__all__ = [
    # 'GeneralBC',
    'FixedBC',
    # 'PinnedBC',
    # 'FixedBCXX',
    # 'FixedBCYY',
    # 'FixedBCZZ',
    # 'RollerBCX',
    # 'RollerBCY',
    # 'RollerBCZ',
    # 'RollerBCXY',
    # 'RollerBCYZ',
    # 'RollerBCXZ'
]

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


def _generate_jobdata(obj):
    jobdata = []
    for nk in obj.nodes:
        jobdata.append('fix {} {}'.format(nk, ' '.join(
            ['1' if obj.components[dof] is not None else '0' for dof in dofs])))  # dofs[:obj.ndof]
    return '\n'.join(jobdata)


class FixedBC(FixedBCBase):

    def __init__(self, name, axes='global'):
        super(FixedBC, self).__init__(name, axes)

    def _generate_jobdata(self):
        return _generate_jobdata(self)


if __name__ == "__main__":
    pass
