from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutput, HistoryOutput


<<<<<<< HEAD
class AbaqusFieldOutput(FieldOutput):
=======
# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'FieldOutput',
    'HistoryOutput',
]


class FieldOutput(FieldOutputBase):
    """Abaqus implementation of the :class:`FieldOutputBase`.\n
    """
    __doc__ += FieldOutputBase.__doc__
    __doc__ += """

    Additional Parameters
    ---------------------
    frequency : ???
        ?????
    """

>>>>>>> 0fcf42ed8e1eb38788d736a3e47f207522be8a7c
    def __init__(self, name, node_outputs=None, element_outputs=None, frequency=1):
        super(AbaqusFieldOutput, self).__init__(name, node_outputs, element_outputs)
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


<<<<<<< HEAD
class AbaqusHistoryOutput(HistoryOutput):
=======
class HistoryOutput(HistoryOutputBase):
    """Abaqus implementation of the :class:`HistoryOutputBase`.\n
    """
    __doc__ += HistoryOutputBase.__doc__

>>>>>>> 0fcf42ed8e1eb38788d736a3e47f207522be8a7c
    def __init__(self, name):
        super(AbaqusHistoryOutput, self).__init__(name)

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
