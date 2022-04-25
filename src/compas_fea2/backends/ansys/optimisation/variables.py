from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.optimisation.variables import DesignVariables

class AnsysDesignVariables(DesignVariables):
    """ Ansys implementation of :class:`.DesignVariables`.\n
    """
    __doc__ += DesignVariables.__doc__

    def __init__(self, variables, name=None, **kwargs):
        super(AnsysDesignVariables, self).__init__(variables=variables, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

