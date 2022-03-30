from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import TieConstraint


class OpenseesTieConstraint(TieConstraint):
    def __init__(self, master, slave, name=None, **kwargs):
        super(OpenseesTieConstraint, self).__init__(master, slave, tol=None, name=name, **kwargs)
        raise NotImplementedError
