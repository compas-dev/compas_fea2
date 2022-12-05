from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import ContactAnalysisOutput
from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput

class SofistikContactAnalysisOutput(ContactAnalysisOutput):
    """Sofistik implementation of :class:`compas_fea2.problem.outputs.ContactAnalysisOutput`.\n
    """
    __doc__ += ContactAnalysisOutput.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikContactAnalysisOutput, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikFieldOutput(FieldOutput):
    """Sofistik implementation of :class:`compas_fea2.problem.outputs.FieldOutput`.\n
    """
    __doc__ += FieldOutput.__doc__

    def __init__(self, node_outputs, element_outputs, contact_outputs, name=None, **kwargs):
        super(SofistikFieldOutput, self).__init__(node_outputs=node_outputs, element_outputs=element_outputs, contact_outputs=contact_outputs, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikHistoryOutput(HistoryOutput):
    """Sofistik implementation of :class:`compas_fea2.problem.outputs.HistoryOutput`.\n
    """
    __doc__ += HistoryOutput.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikHistoryOutput, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

