from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Part


class OpenseesPart(Part):
    """OpenSees implementation of :class:`compas_fea2.model.Part`.

    Note
    ----
    Models with multiple parts are not currently supported in Opensees.
    """
    __doc__ += Part.__doc__

    def __init__(self, model=None, name=None, **kwargs):
        super(OpenseesPart, self).__init__(model=model, name=name, **kwargs)

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

    def _generate_jobdata(self):
        pass
