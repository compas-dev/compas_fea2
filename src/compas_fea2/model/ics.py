from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _InitialCondition(FEAData):
    """Base class for all predefined initial conditions.

    Notes
    -----
    InitialConditions are registered to a :class:`compas_fea2.model.Model`. The
    same InitialCondition can be assigned to Nodes or Elements in multiple Parts

    """

    def __init__(self, **kwargs):
        super(_InitialCondition, self).__init__(**kwargs)


#FIXME this is not really a field in the sense that it is only applied to 1 node/element
class InitialTemperatureField(_InitialCondition):
    """Temperature field.

    Parameters
    ----------
    temperature : float
        The temperature value.

    Attributes
    ----------
    temperature : float
        The temperature value.

    Notes
    -----
    InitialConditions are registered to a :class:`compas_fea2.model.Model`. The
    same InitialCondition can be assigned to Nodes or Elements in multiple Parts

    """

    def __init__(self, temperature, **kwargs):
        super(InitialTemperatureField, self).__init__(**kwargs)
        self._t = temperature

    @property
    def temperature(self):
        return self._t

    @temperature.setter
    def temperature(self, value):
        self._t = value


class InitialStressField(_InitialCondition):
    """Stress field.

    Parameters
    ----------
    stress : touple(float, float, float)
        The stress values.

    Attributes
    ----------
    stress : touple(float, float, float)
        The stress values.

    Notes
    -----
    InitialConditions are registered to a :class:`compas_fea2.model.Model`
    The same InitialCondition can be assigned to Nodes or Elements in multiple Parts.

    """

    def __init__(self, stress, **kwargs):
        super(InitialStressField, self).__init__(**kwargs)
        self._s = stress

    @property
    def stress(self):
        return self._s

    @stress.setter
    def stress(self, value):
        if not isinstance(value, tuple) or len(value) != 3:
            raise TypeError("you must provide a tuple with 3 elements")
        self._s = value
