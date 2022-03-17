from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import GeneralBCBase
from compas_fea2.model import FixedBCBase
from compas_fea2.model import PinnedBCBase
from compas_fea2.model import FixedBCXXBase
from compas_fea2.model import FixedBCYYBase
from compas_fea2.model import FixedBCZZBase
from compas_fea2.model import RollerBCXBase
from compas_fea2.model import RollerBCYBase
from compas_fea2.model import RollerBCZBase
from compas_fea2.model import RollerBCXYBase
from compas_fea2.model import RollerBCYZBase
from compas_fea2.model import RollerBCXZBase


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


def _generate_jobdata(obj):
    jobdata = []
    for nk in obj.nodes:
        jobdata.append('fix {} {}'.format(nk, ' '.join(
            ['1' if obj.components[dof] is not None else '0' for dof in dofs])))  # dofs[:obj.ndof]
    return '\n'.join(jobdata)


class FixedBC(FixedBCBase):
    """OpenSees implementation of :class:`FixedBCBase`.\n
    """
    __doc__ += FixedBCBase.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBC, self).__init__(name, axes)

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class PinnedBC(PinnedBCBase):
    """OpenSees implementation of :class:`PinnedBCBase`.\n
    """
    __doc__ += PinnedBCBase.__doc__

    def __init__(self, name, axes='global'):
        super(PinnedBC, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCXX(FixedBCXXBase):
    """OpenSees implementation of :class:`FixedBCXXBase`.\n
    """
    __doc__ += FixedBCXXBase.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBCXX, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCYY(FixedBCYYBase):
    """OpenSees implementation of :class:`FixedBCYYBase`.\n
    """
    __doc__ += FixedBCYYBase.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBCYY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCZZ(FixedBCZZBase):
    """OpenSees implementation of :class:`FixedBCZZBase`.\n
    """
    __doc__ += FixedBCZZBase.__doc__

    def __init__(self, name, axes='global'):
        super(FixedBCZZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCX(RollerBCXBase):
    """OpenSees implementation of :class:`RollerBCXBase`.\n
    """
    __doc__ += RollerBCXBase.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCX, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCY(RollerBCYBase):
    """OpenSees implementation of :class:`RollerBCYBase`.\n
    """
    __doc__ += RollerBCYBase.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCZ(RollerBCZBase):
    """OpenSees implementation of :class:`RollerBCZBase`.\n
    """
    __doc__ += RollerBCZBase.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCXY(RollerBCXYBase):
    """OpenSees implementation of :class:`RollerBCXYBase`.\n
    """
    __doc__ += RollerBCXYBase.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCXY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCYZ(RollerBCYZBase):
    """OpenSees implementation of :class:`RollerBCYZBase`.\n
    """
    __doc__ += RollerBCYZBase.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCYZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCXZ(RollerBCXZBase):
    """OpenSees implementation of :class:`RollerBCXZBase`.\n
    """
    __doc__ += RollerBCXZBase.__doc__

    def __init__(self, name, axes='global'):
        super(RollerBCXZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)
