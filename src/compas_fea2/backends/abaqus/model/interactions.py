from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.interactions import HardContactFrictionPenalty
from compas_fea2.model.interactions import LinearContactFrictionPenalty
from compas_fea2.model.interactions import HardContactRough


class AbaqusHardContactFrictionPenalty(HardContactFrictionPenalty):
    """Abaqus implementation of the :class:`HardContactFrictionPenalty`.\n"""
    __doc__ += HardContactFrictionPenalty.__doc__

    def __init__(self, *, mu, tolerance=0.005, name=None, **kwargs) -> None:
        super(AbaqusHardContactFrictionPenalty, self).__init__(mu=mu, tolerance=tolerance, name=name, **kwargs)

    def _generate_jobdata(self):
        return """*Surface Interaction, name={}
*Friction, slip tolerance={}
{},
*Surface Behavior, pressure-overclosure={}
**""".format(self._name,
             self._tolerance,
             self._tangent,
             self._normal)

class AbaqusLinearContactFrictionPenalty(LinearContactFrictionPenalty):
    """Abaqus implementation of the :class:`LinearContactFrictionPenalty`.\n"""
    __doc__ += LinearContactFrictionPenalty.__doc__

    def __init__(self, *, mu, tolerance=0.005, name=None, **kwargs) -> None:
        super(AbaqusLinearContactFrictionPenalty, self).__init__(mu=mu, tolerance=tolerance, name=name, **kwargs)

    def _generate_jobdata(self):
        return """*Surface Interaction, name={}
*Friction, slip tolerance={}
{},
*Surface Behavior, pressure-overclosure={}
{}
**""".format(self._name,
             self._tolerance,
             self._tangent,
             self._normal,
             self._stiffness)


class AbaqusHardContactRough(HardContactRough):
    """Abaqus implementation of the :class:`HardContactRough`.\n"""
    __doc__ += HardContactRough.__doc__

    def __init__(self, *, name=None, **kwargs) -> None:
        super(AbaqusHardContactRough, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self):
        return """*Surface Interaction, name={}
*Friction, rough
*Surface Behavior, pressure-overclosure={}
**""".format(self._name,
             self._normal)
