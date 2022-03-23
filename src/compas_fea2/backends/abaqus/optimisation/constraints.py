from compas_fea2.optimisation.constraints import OptimisationConstraint


class AbaqusOptimisationConstraint(OptimisationConstraint):
    def __init__(self, name, design_response, relative=False) -> None:
        super().__init__(name, design_response, relative)

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
