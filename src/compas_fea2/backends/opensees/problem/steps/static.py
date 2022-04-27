from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import StaticRiksStep


class OpenseesStaticStep(StaticStep):
    """Opensees implementation of the :class:`LinearStaticStep`.\n
    """
    __doc__ += StaticStep.__doc__

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(OpenseesStaticStep, self).__init__(max_increments, initial_inc_size,
                                                 min_inc_size, time, nlgeom, modify, name=name, **kwargs)

    def _generate_jobdata(self, problem):
        return """#
# {0}
#
#
timeSeries Constant {1} -factor 1.0
pattern Plain {1} {1} -fact 1 {{
{2}
}}""".format(self.name, problem.steps_order.index(self.name), '\n'.join([load._generate_jobdata() for load in self.loads]))


class OpenseesStaticRiksStep(StaticRiksStep):
    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name, **kwargs)
        raise NotImplementedError
