from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem.outputs import FieldOutputBase, HistoryOutputBase


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'FieldOutput',
    'HistoryOutput',
]


class FieldOutput(FieldOutputBase):
    def __init__(self, name, node_outputs=None, element_outputs=None, frequency=1):
        super(FieldOutput, self).__init__(name, node_outputs, element_outputs, frequency)
        self.__name__ = 'FieldOutputRequst'
        self._jobdata = self._generate_jobdata()

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file.

        Returns
        -------
        str

        Examples
        --------
        >>>
        """
        return self._jobdata

    def _generate_jobdata(self):
        data = ['** FIELD OUTPUT: {}\n**'.format(self._name)]
        if not (self._node_outputs and self._element_outputs):
            data.append('*Output, field, variable=PRESELECT\n**\n')
        else:
            data.append("""*Output, field, frequency={}
*Node Output
{}
*Element output, direction=YES
{}\n""".format(self.frequency, ', '.join(self.node_outputs), ', '.join(self.element_outputs)))

        return '\n'.join(data)


class HistoryOutput(HistoryOutputBase):
    def __init__(self, name):
        super(HistoryOutput, self).__init__(name)
        self.__name__ = 'FieldOutputRequst'
        self._jobdata = """** HISTORY OUTPUT: {}
**
*Output, history, variable=PRESELECT
**\n""".format(self._name)

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file.

        Returns
        -------
        str

        Examples
        --------
        >>>
        """
        return self._jobdata
