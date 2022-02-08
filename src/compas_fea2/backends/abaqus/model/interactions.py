from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import ContactHardFrictionPenalty


class AbaqusContactHardFrictionPenalty(ContactHardFrictionPenalty):
    def __init__(self, name, mu, tollerance=0.005) -> None:
        super(AbaqusContactHardFrictionPenalty, self).__init__(name, mu, tollerance)

    def _generate_jobdata(self):
        return f"""
*Surface Interaction, name={self._name}
1.,
*Friction, slip tolerance={self._tollerance}
{self._tangent},
*Surface Behavior, pressure-overclosure={self._normal}
**
"""
