from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.problem import Problem
from compas_fea2.problem import _Step

class SofistikProblem(Problem):
    """Sofistik implementation of :class:`compas_fea2.problem.problem.Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, name=None, description=None, **kwargs):
        super(SofistikProblem, self).__init__(name=name, description=description, **kwargs)

    def _generate_jobdata(self):
        return """
$ STEPS
{}

$ ANALYSIS
+prog ase 
head analysis
syst prob line
lc no 1000  titl 'linear analysis test load'
lcc no 1  fact 1.0
end

+prog aqb 
head stresses
stre
lc 1000
beam type beam
end
        """.format('\n'.join([step._generate_jobdata() for step in self.steps]))