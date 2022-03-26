from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class FieldOutput(FEAData):
    """FieldOutput object for specification of the fields (stresses, displacements,
    etc..) to output from the analysis.

    Parameters
    ----------
    nodes_outputs : list
        list of node fields to output
    elements_outputs : list
        list of elements fields to output

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    nodes_outputs : list
        list of node fields to output
    elements_outputs : list
        list of elements fields to output

    """

    def __init__(self, node_outputs, element_outputs):
        super(FieldOutput, self).__init__()
        self._name = "FieldOutput_"+str(id(self))
        self._node_outputs = node_outputs
        self._element_outputs = element_outputs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def node_outputs(self):
        """list : list of node fields to output."""
        return self._node_outputs

    @property
    def element_outputs(self):
        """list : list of elements fields to output."""
        return self._element_outputs


class HistoryOutput(FEAData):
    """HistoryOutput object for recording the fields (stresses, displacements,
    etc..) from the analysis.

    Parameters
    ----------
    None

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    """

    def __init__(self, name):
        super(HistoryOutput, self).__init__()
        self._name = "HistoryOutput_"+str(id(self))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
