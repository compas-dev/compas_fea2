from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.constraints import TieConstraint

class AnsysTieConstraint(TieConstraint):
    """Ansys implementation of :class:`compas_fea2.model.constraints.TieConstraint`.\n
    """
    __doc__ += TieConstraint.__doc__

    def __init__(self, *, master, slave, tol, name=None, **kwargs):
        super(AnsysTieConstraint, self).__init__(master=master, slave=slave, tol=tol, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

