from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput


class OpenseesFieldOutput(FieldOutput):
    def __init__(self, name, node_outputs=None, element_outputs=None, frequency=1):
        super(FieldOutput, self).__init__(name, node_outputs, element_outputs, frequency)

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file."""
        return self._generate_jobdata()

    def _generate_jobdata(self):
        # for no
        "recorder Node -file C:/temp/introduction/step_loads_u.out -time -nodeRange 1 5 -dof 1 2 3 disp"


class OpenseesHistoryOutput(HistoryOutput):
    def __init__(self, name):
        super(HistoryOutput, self).__init__(name)

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file."""
        return self._jobdata

    def _generate_jobdata(self):
        pass
