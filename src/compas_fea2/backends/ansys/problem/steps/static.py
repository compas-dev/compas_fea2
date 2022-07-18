from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps.static import StaticRiksStep
from compas_fea2.problem.steps.static import StaticStep

class AnsysStaticRiksStep(StaticRiksStep):
    """Ansys implementation of :class:`compas_fea2.problem.steps.static.StaticRiksStep`.\n
    """
    __doc__ += StaticRiksStep.__doc__

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=1e-05, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(AnsysStaticRiksStep, self).__init__(max_increments=max_increments, initial_inc_size=initial_inc_size, min_inc_size=min_inc_size, time=time, nlgeom=nlgeom, modify=modify, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysStaticStep(StaticStep):
    """Ansys implementation of :class:`compas_fea2.problem.steps.static.StaticStep`.\n
    """
    __doc__ += StaticStep.__doc__

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=1e-05, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(AnsysStaticStep, self).__init__(max_increments=max_increments, initial_inc_size=initial_inc_size, min_inc_size=min_inc_size, time=time, nlgeom=nlgeom, modify=modify, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

