from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.base import FEABase
# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'FieldOutputBase',
    'HistoryOutputBase',
]


class FieldOutputBase(FEABase):
    def __init__(self, name, node_outputs, element_outputs, frequency):
        super(FieldOutputBase, self).__init__()
        self.__name__ = 'FieldOutputRequst'
        self.name = name
        # self.domain    = domain
        # self.frequency = frequency
        # self.variables = variables
        self.node_outputs = node_outputs
        self.element_outputs = element_outputs
        self.frequency = frequency

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class HistoryOutputBase():
    def __init__(self, name):
        super(HistoryOutputBase, self).__init__()
        self.__name__ = 'HistoryOutputRequst'
        self.name = name
        # self.domain    = domain
        # self.frequency = frequency
        # self.variables = variables

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)
