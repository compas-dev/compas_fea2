from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class FieldOutput(FEAData):
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
        super(FieldOutput, self).__init__(name=name)
        self._node_outputs = node_outputs
        self._element_outputs = element_outputs

    @property
    def node_outputs(self):
        """list : list of node fields to output."""
        return self._node_outputs

    @property
    def element_outputs(self):
        """list : list of elements fields to output."""
        return self._element_outputs


class HistoryOutput(FEAData):
    def __init__(self, name):
        super(HistoryOutput, self).__init__(name=name)
