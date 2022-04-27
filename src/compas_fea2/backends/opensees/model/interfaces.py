from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Interface


class OpenseesInterface(Interface):
    """Opensees implementation of an Interface.

    """
    __doc__ += Interface.__doc__

    def __init__(self, master, slave, interaction, name=None, **kwargs):
        super(OpenseesInterface, self).__init__(master, slave, interaction, name=name, **kwargs)
        raise NotImplementedError
