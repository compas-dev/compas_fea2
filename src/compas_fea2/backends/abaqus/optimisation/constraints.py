from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.constraints import OptimisationConstraint


class AbaqusOptimisationConstraint(OptimisationConstraint):
    """Abaqus implementation of :class:`OptimisationConstraint`\n"""
    __doc__ += OptimisationConstraint.__doc__

    def __init__(self, design_response, relative=False, name=None, **kwargs):
        super(AbaqusOptimisationConstraint, self).__init__(design_response, relative, name=name, **kwargs)

    def _generate_jobdata(self):
        equalities = {'=': 'EQ_VALUE', '<=': 'LE_VALUE', '<>=': 'GE_VALUE'}
        return f"""!
CONSTRAINT
  ID_NAME        = {self._name}
  DRESP          = {self._design_response._name}
  MAGNITUDE      = {'REL' if self._relative else 'ABS'}
  {equalities[self._constraint_type]}       = {self._constraint_value}
END_
"""
