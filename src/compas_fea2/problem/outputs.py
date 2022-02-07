from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class FieldOutputBase(FEABase):
    """FieldOutput object for specification of the fields (stresses, displacements,
    etc..) to output from the analysis.

    Parameters
    ----------
    name : str
        name of the output request
    nodes_outputs : list
        list of node fields to output
    elements_outputs : list
        list of elements fields to output
    """

    def __init__(self, name, node_outputs, element_outputs):
        super(FieldOutputBase, self).__init__()
        self.__name__ = 'FieldOutputRequst'
        self._name = name
        self._node_outputs = node_outputs
        self._element_outputs = element_outputs

    @property
    def name(self):
        """str : name of the output request."""
        return self._name

    @property
    def node_outputs(self):
        """list : list of node fields to output."""
        return self._node_outputs

    @property
    def element_outputs(self):
        """list : list of elements fields to output."""
        return self._element_outputs

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


class HistoryOutputBase(FEABase):
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
