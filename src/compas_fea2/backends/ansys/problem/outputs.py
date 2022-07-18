from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput

class AnsysFieldOutput(FieldOutput):
    """Ansys implementation of :class:`compas_fea2.problem.outputs.FieldOutput`.\n
    """
    __doc__ += FieldOutput.__doc__

    def __init__(self, node_outputs, element_outputs, name=None, **kwargs):
        super(AnsysFieldOutput, self).__init__(node_outputs=node_outputs, element_outputs=element_outputs, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class AnsysHistoryOutput(HistoryOutput):
    """Ansys implementation of :class:`compas_fea2.problem.outputs.HistoryOutput`.\n
    """
    __doc__ += HistoryOutput.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysHistoryOutput, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

