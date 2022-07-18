from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutput, HistoryOutput


class AbaqusFieldOutput(FieldOutput):
    """Abaqus implementation of :class:`FieldOutput`.\n"""
    __doc__ += FieldOutput.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    frequency : int
        ???

    Additional Attributes
    ---------------------
    frequency : int
        ???
    """

    def __init__(self, node_outputs=None, element_outputs=None, frequency=1, name=None, **kwargs):
        super(AbaqusFieldOutput, self).__init__(node_outputs, element_outputs, name=name, **kwargs)
        self._frequency = frequency

    @property
    def frequency(self):
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
        data = ['** FIELD OUTPUT: {}\n**'.format(self.name)]
        if not self.node_outputs and not self.element_outputs:
            data.append('*Output, field, variable=ALL\n**')
        else:
            data.append('*Output, field')
            if self.element_outputs:
                data.append('\n'.join(['*Element Output, direction=YES', '{}'.format(", ".join(self.element_outputs))]))
            if self.node_outputs:
                data.append('\n'.join(['*Node Output', '{}'.format(", ".join(self.node_outputs))]))

        return '\n'.join(data)


class AbaqusHistoryOutput(HistoryOutput):
    """Abaqus implementation of :class:`HistoryOutput`.\n"""
    __doc__ += HistoryOutput.__doc__

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
*Output, history, variable=ALL
**""".format(self._name)
