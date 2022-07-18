from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import TieConstraint


class AbaqusTieConstraint(TieConstraint):
    """Abaqus implementation of :class:`TieConstraint`\n"""
    __doc__ += TieConstraint.__doc__

    def __init__(self, *, master, slave, name=None, **kwargs):
        super(AbaqusTieConstraint, self).__init__(master=master, slave=slave, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        return (
            "** Constraint: {}\n"
            "*MPC\n"
            "TIE, {}_i, {}_i\n").format(self.name, self._slave.name, self._master.name)

        # return '\n'.join(['** Constraint: {}'.format(self.name),
        #                   '*Tie, name={}, adjust=yes'.format(self.name),
        #                   '{}, {}'.format(self._slave.name, self._master.name)])
