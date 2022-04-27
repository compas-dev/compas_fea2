from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.interfaces import Interface


class AnsysInterface(Interface):
    """ Ansys implementation of :class:`.Interface`.\n
    """
    __doc__ += Interface.__doc__

    def __init__(self, *, master, slave, interaction, name=None, **kwargs):
        super(AnsysInterface, self).__init__(master=master, slave=slave, interaction=interaction, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
