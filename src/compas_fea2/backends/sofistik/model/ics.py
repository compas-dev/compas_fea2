from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.ics import InitialStressField
from compas_fea2.model.ics import InitialTemperatureField

class SofistikInitialStressField(InitialStressField):
    """Sofistik implementation of :class:`compas_fea2.model.ics.InitialStressField`.\n
    """
    __doc__ += InitialStressField.__doc__

    def __init__(self, stress, name=None, **kwargs):
        super(SofistikInitialStressField, self).__init__(stress=stress, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikInitialTemperatureField(InitialTemperatureField):
    """Sofistik implementation of :class:`compas_fea2.model.ics.InitialTemperatureField`.\n
    """
    __doc__ += InitialTemperatureField.__doc__

    def __init__(self, temperature, name=None, **kwargs):
        super(SofistikInitialTemperatureField, self).__init__(temperature=temperature, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

