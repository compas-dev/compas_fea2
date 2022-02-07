from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutputBase, HistoryOutputBase


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'FieldOutput',
    'HistoryOutput',
]


class FieldOutput(FieldOutputBase):
    def __init__(self, name, node_outputs=None, element_outputs=None, frequency=1):
        super(FieldOutput, self).__init__(name, node_outputs, element_outputs)
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
            data.append('*Output, field, variable=PRESELECT\n**\n')
        else:
            data.append(f'*Output, field, frequency={self.frequency}')
            if self.node_outputs:
                data.append('\n'.join([f'*Node Output',
                                       f'{", ".join(self.node_outputs)}']))
            if self.element_outputs:
                data.append('\n'.join([f'*Element output, direction=YES',
                                       f'{", ".join(self.element_outputs)}']))
        return '\n'.join(data)


class HistoryOutput(HistoryOutputBase):
    def __init__(self, name):
        super(HistoryOutput, self).__init__(name)
        self.__name__ = 'FieldOutputRequst'

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
**\n""".format(self._name)
