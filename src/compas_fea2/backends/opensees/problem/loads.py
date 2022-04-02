from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import _Load
from compas_fea2.problem import PointLoad
from compas_fea2.problem import LineLoad
from compas_fea2.problem import AreaLoad
from compas_fea2.problem import GravityLoad


__all__ = [
    'PointLoad',
]

dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class OpenseesPointLoad(PointLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.PointLoad`.\n
    """
    __doc__ += PointLoad.__doc__

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', name=None, **kwargs):
        super(OpenseesPointLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)

    def _generate_jobdata(self):
        jobdata = []
        for node in self.nodes:
            jobdata.append('load {} {}'.format(node, ' '.join([str(self.components[dof]) for dof in dofs])))
        return '\n'.join(jobdata)
