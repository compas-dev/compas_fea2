from compas_fea2.backends._base.model.contacts import ContactBase


class Contact(ContactBase):
    def __init__(self, name, master, slave, interaction):
        super(Contact, self).__init__(name, master, slave, interaction)

    def _generate_jobdata(self):
        return f"""** Interaction: {self._name}
*Contact Pair, interaction={self._interaction}, type=SURFACE TO SURFACE
{self._master}, {self._slave}
**"""
