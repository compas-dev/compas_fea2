from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutput, HistoryOutput


class OpenseesFieldOutput(FieldOutput):
    """"""
    __doc__ += FieldOutput.__doc__

    def __init__(self, node_outputs=None, element_outputs=None, frequency=1, name=None, **kwargs):
        super(OpenseesFieldOutput, self).__init__(node_outputs, element_outputs, name=name, **kwargs)
        raise NotImplementedError()


class OpenseesHistoryOutput(HistoryOutput):
    """"""
    __doc__ += HistoryOutput.__doc__

    def __init__(self):
        super(OpenseesHistoryOutput, self).__init__()
        raise NotImplementedError()
