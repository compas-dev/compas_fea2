from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.materials import Timber


class AbaqusTimber(Timber):
    """"""
    __doc__ += Timber.__doc__

    def __init__(self, *, name=None, **kwargs):
        super(AbaqusTimber, self).__init__(name=name, **kwargs)
        raise NotImplementedError('The current material is not available in Abaqus')

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        raise NotImplementedError
