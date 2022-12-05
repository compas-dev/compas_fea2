from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.fields import PrescribedTemperatureField

class SofistikPrescribedTemperatureField(PrescribedTemperatureField):
    """Sofistik implementation of :class:`compas_fea2.problem.fields.PrescribedTemperatureField`.\n
    """
    __doc__ += PrescribedTemperatureField.__doc__

    def __init__(self, temperature, name=None, **kwargs):
        super(SofistikPrescribedTemperatureField, self).__init__(temperature=temperature, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

