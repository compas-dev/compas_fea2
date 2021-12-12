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
        self._name = name
        self._node_outputs = node_outputs
        self._element_outputs = element_outputs
        self._frequency = frequency

    @property
    def name(self):
        """The name property."""
        return self._name

    @property
    def node_outputs(self):
        """The node_outputs property."""
        return self._node_outputs

    @property
    def element_outputs(self):
        """The element_outputs property."""
        return self._element_outputs

    @property
    def frequency(self):
        """The frequency property."""
        return self._frequency

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class HistoryOutputBase():
    def __init__(self, name):
        super(HistoryOutputBase, self).__init__()
        self.__name__ = 'HistoryOutputRequst'
        self._name = name

    @property
    def name(self):
        """The name property."""
        return self._name

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)
