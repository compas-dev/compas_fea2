from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import Load
from compas_fea2.problem import PrestressLoad
from compas_fea2.problem import PointLoad
from compas_fea2.problem import LineLoad
from compas_fea2.problem import AreaLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import TributaryLoad
from compas_fea2.problem import HarmonicPointLoad
from compas_fea2.problem import HarmonicPressureLoad
from compas_fea2.problem import AcousticDiffuseFieldLoad


__all__ = [
    'PointLoad',
]

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class PointLoad(PointLoad):
    """OpenSees implementation of :class:`PointLoad`.\n
    """
    __doc__ += PointLoad.__doc__

    def __init__(self, name, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', modify=False, follow=False):
        super(PointLoad, self).__init__(name=name, x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes)

    def _generate_jobdata(self):
        jobdata = []
        for node in self.nodes:
            jobdata.append('load {} {}'.format(node, ' '.join([str(self.components[dof]) for dof in dofs])))
        return '\n'.join(jobdata)
