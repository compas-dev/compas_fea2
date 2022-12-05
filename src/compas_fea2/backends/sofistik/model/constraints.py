from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.constraints import BeamMPC
from compas_fea2.model.constraints import MultiPointConstraint
from compas_fea2.model.constraints import TieConstraint
from compas_fea2.model.constraints import TieMPC

class SofistikBeamMPC(BeamMPC):
    """Sofistik implementation of :class:`compas_fea2.model.constraints.BeamMPC`.\n
    """
    __doc__ += BeamMPC.__doc__

    def __init__(self, constraint_type, name=None, **kwargs):
        super(SofistikBeamMPC, self).__init__(constraint_type=constraint_type, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikMultiPointConstraint(MultiPointConstraint):
    """Sofistik implementation of :class:`compas_fea2.model.constraints.MultiPointConstraint`.\n
    """
    __doc__ += MultiPointConstraint.__doc__

    def __init__(self, constraint_type, name=None, **kwargs):
        super(SofistikMultiPointConstraint, self).__init__(constraint_type=constraint_type, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTieConstraint(TieConstraint):
    """Sofistik implementation of :class:`compas_fea2.model.constraints.TieConstraint`.\n
    """
    __doc__ += TieConstraint.__doc__

    def __init__(self, *, name=None, **kwargs):
        super(SofistikTieConstraint, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikTieMPC(TieMPC):
    """Sofistik implementation of :class:`compas_fea2.model.constraints.TieMPC`.\n
    """
    __doc__ += TieMPC.__doc__

    def __init__(self, constraint_type, name=None, **kwargs):
        super(SofistikTieMPC, self).__init__(constraint_type=constraint_type, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

