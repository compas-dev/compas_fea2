from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.results.results import Results
from compas_fea2.results.results import StepResults

class SofistikResults(Results):
    """Sofistik implementation of :class:`compas_fea2.results.results.Results`.\n
    """
    __doc__ += Results.__doc__

    def __init__(self, *, database_path, database_name):
        super(SofistikResults, self).__init__(database_path=database_path, database_name=database_name)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikStepResults(StepResults):
    """Sofistik implementation of :class:`compas_fea2.results.results.StepResults`.\n
    """
    __doc__ += StepResults.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikStepResults, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

