from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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


def _generate_jobdata(bc, nodes):
    return '\n'.join(['fix {} {}'.format(node.key, ' '.join([str(int(getattr(bc, dof))) for dof in dofs])) for node in nodes])


class OpenseesFixedBC(FixedBC):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBC`.\n
    """
    __doc__ += FixedBC.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesFixedBC, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesPinnedBC(PinnedBC):
    """OpenSees implementation of :class:`compas_fea2.model.PinnedBC`.\n
    """
    __doc__ += PinnedBC.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesPinnedBC, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesFixedBCXX(FixedBCXX):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBCXX`.\n
    """
    __doc__ += FixedBCXX.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesFixedBCXX, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesFixedBCYY(FixedBCYY):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBCYY`.\n
    """
    __doc__ += FixedBCYY.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesFixedBCYY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesFixedBCZZ(FixedBCZZ):
    """OpenSees implementation of :class:`FixedBCZZ`.\n
    """
    __doc__ += FixedBCZZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesFixedBCZZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesRollerBCX(RollerBCX):
    """OpenSees implementation of :class:`RollerBCX`.\n
    """
    __doc__ += RollerBCX.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesRollerBCX, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesRollerBCY(RollerBCY):
    """OpenSees implementation of :class:`RollerBCY`.\n
    """
    __doc__ += RollerBCY.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesRollerBCY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesRollerBCZ(RollerBCZ):
    """OpenSees implementation of :class:`RollerBCZ`.\n
    """
    __doc__ += RollerBCZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesRollerBCZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesRollerBCXY(RollerBCXY):
    """OpenSees implementation of :class:`RollerBCXY`.\n
    """
    __doc__ += RollerBCXY.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesRollerBCXY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesRollerBCYZ(RollerBCYZ):
    """OpenSees implementation of :class:`RollerBCYZ`.\n
    """
    __doc__ += RollerBCYZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesRollerBCYZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)


class OpenseesRollerBCXZ(RollerBCXZ):
    """OpenSees implementation of :class:`RollerBCXZ`.\n
    """
    __doc__ += RollerBCXZ.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesRollerBCXZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, nodes):
        return _generate_jobdata(self, nodes)
