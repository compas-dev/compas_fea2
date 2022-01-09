from compas_fea2.backends._base.model.interactions import ContactHardFrictionPenaltyBase


class ContactHardFrictionPenalty(ContactHardFrictionPenaltyBase):
    def __init__(self, name, mu, slip_tollerance=0.005) -> None:
        super(ContactHardFrictionPenalty, self).__init__(name, mu, slip_tollerance)

    def _generate_jobdata(self):
        return f"""*Surface Interaction, name={self._name}
1.,
*Friction, slip tolerance={self._slip_tollerance}
{self._mu},
*Surface Behavior, pressure-overclosure={self._normal}
**"""
