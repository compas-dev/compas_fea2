from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import BoundaryCondition
from compas_fea2.model import FixedBC
from compas_fea2.model import PinnedBC
from compas_fea2.model import FixedBCXX
from compas_fea2.model import FixedBCYY
from compas_fea2.model import FixedBCZZ
from compas_fea2.model import RollerBCX
from compas_fea2.model import RollerBCY
from compas_fea2.model import RollerBCZ
from compas_fea2.model import RollerBCXY
from compas_fea2.model import RollerBCYZ
from compas_fea2.model import RollerBCXZ


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


def _generate_jobdata(obj):
    jobdata = []
    for nk in obj.nodes:
        jobdata.append('fix {} {}'.format(nk, ' '.join(
            ['1' if obj.components[dof] is not None else '0' for dof in dofs])))  # dofs[:obj.ndof]
    return '\n'.join(jobdata)


class FixedBC(FixedBC):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBC`.\n
    """
    __doc__ += FixedBC.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBC, self).__init__(name, axes)

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class PinnedBC(PinnedBC):
    """OpenSees implementation of :class:`compas_fea2.model.PinnedBC`.\n
    """
    __doc__ += PinnedBC.__doc__

    def __init__(self, name, axes='global'):
        super(PinnedBC, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCXX(FixedBCXX):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBCXX`.\n
    """
    __doc__ += FixedBCXX.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBCXX, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCYY(FixedBCYY):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBCYY`.\n
    """
    __doc__ += FixedBCYY.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBCYY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCZZ(FixedBCZZ):
    """OpenSees implementation of :class:`FixedBCZZ`.\n
    """
    __doc__ += FixedBCZZ.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBCZZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCX(RollerBCX):
    """OpenSees implementation of :class:`RollerBCX`.\n
    """
    __doc__ += RollerBCX.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCX, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCY(RollerBCY):
    """OpenSees implementation of :class:`RollerBCY`.\n
    """
    __doc__ += RollerBCY.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCZ(RollerBCZ):
    """OpenSees implementation of :class:`RollerBCZ`.\n
    """
    __doc__ += RollerBCZ.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCXY(RollerBCXY):
    """OpenSees implementation of :class:`RollerBCXY`.\n
    """
    __doc__ += RollerBCXY.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCXY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCYZ(RollerBCYZ):
    """OpenSees implementation of :class:`RollerBCYZ`.\n
    """
    __doc__ += RollerBCYZ.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCYZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCXZ(RollerBCXZ):
    """OpenSees implementation of :class:`RollerBCXZ`.\n
    """
    __doc__ += RollerBCXZ.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCXZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)
