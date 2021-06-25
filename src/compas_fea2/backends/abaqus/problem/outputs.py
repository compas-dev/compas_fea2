from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'FieldOutput',
    'HistoryOutput',
]


class FieldOutput():
    def __init__(self, name, node_outputs=None, element_outputs=None, frequency=1):
        self.__name__ = 'FieldOutputRequst'
        self.name = name
        # self.domain    = domain
        # self.frequency = frequency
        # self.variables = variables
        self.node_outputs = node_outputs
        self.element_outputs = element_outputs
        self.frequency = frequency

        self.data = self._generate_data()

    def _generate_data(self):
        data = ['** FIELD OUTPUT: {}\n**'.format(self.name)]
        if not (self.node_outputs and self.element_outputs):
            data.append('*Output, field, variable=PRESELECT\n**\n')
        else:
            data.append("""*Output, field, frequency={}
*Node Output
{}
*Element output, direction=YES
{}\n""".format(self.frequency, ', '.join(self.node_outputs), ', '.join(self.element_outputs)))

        return '\n'.join(data)


class HistoryOutput():
    def __init__(self, name):
        self.__name__ = 'FieldOutputRequst'
        self.name = name
        # self.domain    = domain
        # self.frequency = frequency
        # self.variables = variables
        self.data = """** HISTORY OUTPUT: {}
**
*Output, history, variable=PRESELECT
**\n""".format(self.name)
