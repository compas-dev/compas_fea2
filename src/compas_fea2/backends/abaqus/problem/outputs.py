from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutput, HistoryOutput


class AbaqusFieldOutput(FieldOutput):
    def __init__(self, node_outputs=None, element_outputs=None, frequency=1):
        super(AbaqusFieldOutput, self).__init__(node_outputs, element_outputs)
        self._frequency = frequency

    @property
    def frequency(self):
        """????"""
        return self._frequency

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data = [f'** FIELD OUTPUT: {self.name}\n**']
        if not self.node_outputs and not self.element_outputs:
            data.append('*Output, field, variable=PRESELECT\n**')
        else:
            data.append(f'*Output, field, frequency={self.frequency}')
            if self.node_outputs:
                data.append('\n'.join(['*Node Output', f'{", ".join(self.node_outputs)}']))
            if self.element_outputs:
                data.append('\n'.join(['*Element output, direction=YES', f'{", ".join(self.element_outputs)}']))
        return '\n'.join(data)


class AbaqusHistoryOutput(HistoryOutput):
    def __init__(self):
        super(AbaqusHistoryOutput, self).__init__()

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return """** HISTORY OUTPUT: {}
**
*Output, history, variable=PRESELECT
**""".format(self._name)
