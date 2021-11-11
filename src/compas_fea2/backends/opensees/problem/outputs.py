from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem.outputs import FieldOutputBase
from compas_fea2.backends._base.problem.outputs import HistoryOutputBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'FieldOutput',
    'HistoryOutput',
]


class FieldOutput(FieldOutputBase):
    def __init__(self, name, node_outputs=None, element_outputs=None, frequency=1):
        super(FieldOutput, self).__init__(name, node_outputs, element_outputs, frequency)

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file."""
        return self._jobdata

    def _generate_jobdata(self):
        pass


class HistoryOutput(HistoryOutputBase):
    def __init__(self, name):
        super(HistoryOutput, self).__init__(name)

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file."""
        return self._jobdata

    def _generate_jobdata(self):
        pass