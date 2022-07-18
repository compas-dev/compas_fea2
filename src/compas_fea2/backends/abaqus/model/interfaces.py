from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Interface

# TODO maybe move the extra parameters to base


class AbaqusInterface(Interface):
    """Abaqus implementation of :class:`Interface`.

    Note
    ----
    This is equivalent to a `Contact Pair` in Abaqus.

    """
    __doc__ += Interface.__doc__

    def __init__(self, *, master, slave, interaction, name=None, small_sliding=False, adjust=True, no_tickness=False, **kwargs):
        super(AbaqusInterface, self).__init__(master=master, slave=slave, interaction=interaction, name=name, **kwargs)

        self._small_sliding = ' small_sliding,' if small_sliding else ''
        self._no_tickness = ' no tickness,' if no_tickness else ''
        self._adjust = ' adjust=0.0' if adjust else ''

    def _generate_jobdata(self):
        return """** Interface: {}
*Contact Pair, interaction={}, type=SURFACE TO SURFACE,{}{}{}
{}, {}
**""".format(self._name,
             self._interaction.name,
             self._no_tickness,
             self._small_sliding,
             self._adjust,
             self._master.name,
             self._slave.name)

    def _generate_controls_jobdata(self):
        return """**
*CONTACT CONTROLS,  STABILIZE, MASTER={}, SLAVE ={}
**""".format(self._master.name,
             self._slave.name)
