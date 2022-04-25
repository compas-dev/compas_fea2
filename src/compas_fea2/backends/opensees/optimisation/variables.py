from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.variables import DesignVariables


class OpenseesDesignVariables(DesignVariables):
    def __init__(self, variables, name=None, **kwargs):
        super(OpenseesDesignVariables, self).__init__(variables, name=name, **kwargs)
        raise NotImplementedError()
