from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.variables import DesignVariables


class AbaqusDesignVariables(DesignVariables):
    def __init__(self, variables, name=None, **kwargs):
        super(AbaqusDesignVariables, self).__init__(variables, name=name, **kwargs)

    def _generate_jobdata(self):
        return f"""!
DV_TOPO
  ID_NAME        = {self._name}
  EL_GROUP       = {self._variables}
END_
"""
