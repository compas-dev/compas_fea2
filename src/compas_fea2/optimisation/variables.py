from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class DesignVariables(FEAData):
    """Define the design variables for the optimiation.

    Parameters
    ----------
    name : str
        the name of the objective function.
    variables : str
        variables of the optimisation
    """

    def __init__(self, variables, name=None, **kwargs):
        super(DesignVariables, self).__init__(name=name, **kwargs)
        self._name = name or 'DesignVar_'+str(id(self))
        self._variables = variables

    @property
    def name(self):
        """str : name of the constraint."""
        return self._name

    @property
    def variables(self):
        """str : variables of the optimisation"""
        return self._variables
