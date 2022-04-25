from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Interface


class AbaqusInterface(Interface):
    """Abaqus implementation of :class:`Interface`.

    Note
    ----
    This is equivalent to a `Contact Pair` in Abaqus.

    """
    __doc__ += Interface.__doc__

    def __init__(self, master, slave, interaction, name=None, **kwargs):
        super(AbaqusInterface, self).__init__(master, slave, interaction, name=name, **kwargs)

    def _generate_jobdata(self):
        return f"""** Interaction: {self._name}
*Contact Pair, interaction={self._interaction.name}, type=SURFACE TO SURFACE
{self._master.name}, {self._slave.name}
**
"""
