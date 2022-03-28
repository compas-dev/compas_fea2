from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import HardContactFrictionPenalty


class AbaqusHardContactFrictionPenalty(HardContactFrictionPenalty):
    def __init__(self, mu, tollerance=0.005, name=None, **kwargs) -> None:
        super(AbaqusHardContactFrictionPenalty, self).__init__(mu, tollerance, name=None, **kwargs)

    def _generate_jobdata(self):
        return f"""
*Surface Interaction, name={self._name}
1.,
*Friction, slip tolerance={self._tollerance}
{self._tangent},
*Surface Behavior, pressure-overclosure={self._normal}
**
"""
