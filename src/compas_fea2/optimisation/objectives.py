from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class ObjectiveFunction(FEAData):
    """Define the obejctive function of an optimisation.

    Parameters
    ----------
    name : str
        the name of the objective function.
    desing_response : obj
        :class:`compas_fea2.optimisation.DesignResponse` subclass of the response to optimise.
    target : str
        target of the optimisation (i.e. 'min', 'MinMax', etc).
    """

    def __init__(self,  design_response, target, name=None, **kwargs):
        super(ObjectiveFunction, self).__init__(name=name, **kwargs)
        self._design_response = design_response
        self._target = target

    @property
    def design_response(self):
        """obj : :class:`compas_fea2.optimisation.DesignResponse` subclass object of the desing response to constraint."""
        return self._design_response

    @property
    def target(self):
        """str :target of the optimisation (i.e. 'min', 'MinMax', etc)."""
        return self._target
