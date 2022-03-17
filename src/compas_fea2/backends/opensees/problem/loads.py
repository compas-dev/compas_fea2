from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import LoadBase
from compas_fea2.problem import PrestressLoadBase
from compas_fea2.problem import PointLoadBase
from compas_fea2.problem import LineLoadBase
from compas_fea2.problem import AreaLoadBase
from compas_fea2.problem import GravityLoadBase
from compas_fea2.problem import TributaryLoadBase
from compas_fea2.problem import HarmonicPointLoadBase
from compas_fea2.problem import HarmonicPressureLoadBase
from compas_fea2.problem import AcousticDiffuseFieldLoadBase


__all__ = [
    'PointLoad',
]

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class PointLoad(PointLoadBase):
    """OpenSees implementation of :class:`PointLoadBase`.\n
    """
    __doc__ += PointLoadBase.__doc__

    def __init__(self, name, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=False, follow=False):
        super(PointLoad, self).__init__(name=name, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes)

    def _generate_jobdata(self):
        jobdata = []
        for node in self.nodes:
            jobdata.append('load {} {}'.format(node, ' '.join([str(self.components[dof]) for dof in dofs])))
        return '\n'.join(jobdata)
