from compas_fea2._base.model.interactions import ContactHardFrictionPenaltyBase


class ContactHardFrictionPenalty(ContactHardFrictionPenaltyBase):
    def __init__(self, name, mu, tollerance=0.005) -> None:
        super(ContactHardFrictionPenalty, self).__init__(name, mu, tollerance)

    def _generate_jobdata(self):
        return f"""*Surface Interaction, name={self._name}
1.,
*Friction, slip tolerance={self._tollerance}
{self._tangent},
*Surface Behavior, pressure-overclosure={self._normal}
**"""
