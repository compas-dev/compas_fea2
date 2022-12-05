from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.results.results import Results
from compas_fea2.results.results import StepResults


class AnsysResults(Results):
    """Ansys implementation of :class:`compas_fea2.results.results.Results`.\n
    """
    __doc__ += Results.__doc__

    def __init__(self, database_name, database_path, fields, steps, sets, components, output):
        super(AnsysResults, self).__init__(database_name=database_name, database_path=database_path,
                                           fields=fields, steps=steps, sets=sets, components=components, output=output)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysStepResults(StepResults):
    """Ansys implementation of :class:`compas_fea2.results.results.StepResults`.\n
    """
    __doc__ += StepResults.__doc__

    def __init__(self, name):
        super(AnsysStepResults, self).__init__(name=name)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
