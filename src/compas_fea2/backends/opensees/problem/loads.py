from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem import LoadBase
from compas_fea2.backends._base.problem import PrestressLoadBase
from compas_fea2.backends._base.problem import PointLoadBase
from compas_fea2.backends._base.problem import LineLoadBase
from compas_fea2.backends._base.problem import AreaLoadBase
from compas_fea2.backends._base.problem import GravityLoadBase
from compas_fea2.backends._base.problem import TributaryLoadBase
from compas_fea2.backends._base.problem import HarmonicPointLoadBase
from compas_fea2.backends._base.problem import HarmonicPressureLoadBase
from compas_fea2.backends._base.problem import AcousticDiffuseFieldLoadBase


# Author(s): Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'PointLoad',
]

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']

# class PrestressLoad(PrestressLoadBase):
#     NotImplemented
#     # def __init__(self, name, elements, sxx):
#     #     super(PrestressLoad, self).__init__(name, elements, sxx)


class PointLoad(PointLoadBase):
    def __init__(self, name,  x=0., y=0., z=0., xx=0., yy=0., zz=0., axes='global'):
        super(PointLoad, self).__init__(name=name, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes)

    def _generate_jobdata(self):
        jobdata = []
        for node in self.nodes:
            jobdata.append('load {} {}'.format(node, ' '.join([str(self.components[dof]) for dof in dofs])))
        return '\n'.join(jobdata)
