from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _InitialCondition(FEAData):
    """Base class for all predefined initial conditions.

    Note
    ----
    InitialConditions are registered to a :class:`compas_fea2.model.Model`. The
    same InitialCondition can be assigned to Nodes or Elements in multiple Parts

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    name : str
        Uniqe identifier.
    """

    def __init__(self, name=None, **kwargs):
        super(_InitialCondition, self).__init__(name=name, **kwargs)

#FIXME this is not really a field in the sense that it is only applied to 1 node/element
class InitialTemperatureField(_InitialCondition):
    """Temperature field.

    Note
    ----
    InitialConditions are registered to a :class:`compas_fea2.model.Model`. The
    same InitialCondition can be assigned to Nodes or Elements in multiple Parts

    Parameters
    ----------
    temperature : float
        The temperature value.
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    temperature : float
        The temperature value.
    name : str
        Uniqe identifier.
    """

    def __init__(self, temperature, name=None, **kwargs):
        super(InitialTemperatureField, self).__init__(name, **kwargs)
        self._t = temperature

    @property
    def temperature(self):
        return self._t

    @temperature.setter
    def temperature(self, value):
        self._t = value


class InitialStressField(_InitialCondition):
    """Stress field.

    Note
    ----
    InitialConditions are registered to a :class:`compas_fea2.model.Model`. The
    same InitialCondition can be assigned to Nodes or Elements in multiple Parts

    Parameters
    ----------
    stress : touple(float, float, float)
        The stress values.
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.

    Attributes
    ----------
    stress : touple(float, float, float)
        The stress values.
    name : str
        Uniqe identifier.
    """

    def __init__(self, stress, name=None, **kwargs):
        super(InitialStressField, self).__init__(name, **kwargs)
        self._s = stress

    @property
    def stress(self):
        return self._s

    @stress.setter
    def stress(self, value):
        if not isinstance(value, tuple) or len(value) != 3:
            raise TypeError("you must provide a tuple with 3 elements")
        self._s = value
