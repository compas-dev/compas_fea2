from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class DesignResponse(FEAData):
    """

    Parameters
    ----------
    group : obj
        :class:`DesignVariables` subclass object.
    group_operator : str
        operation to evaluate the response (i.e. `sum`)
    """

    def __init__(self, group, group_operator) -> None:
        self._group = group
        self._group_operator = group_operator

    @property
    def group(self):
        """obj : :class:`DesignVariables` subclass object."""
        return self._group

    @property
    def group_operator(self):
        """str : operation to evaluate the response (i.e. `sum`)."""
        return self._group_operator


class VolumeResponse(DesignResponse):
    """Volume response recorder."""
    __doc__ += DesignResponse.__doc__

    def __init__(self, group, group_operator) -> None:
        super().__init__(group, group_operator)
        self._name = 'DR_Volume'
        self._type = 'VOLUME'


class EnergyStiffnessResponse(DesignResponse):
    """Energy stiffness measure response recorder."""
    __doc__ += DesignResponse.__doc__

    def __init__(self, group, group_operator, lc) -> None:
        super().__init__(group, group_operator)
        self._name = 'DR_EnergyStiffness'
        self._type = 'ENERGY_STIFF_MEASURE'
        self._lc = lc
