from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.patterns import Pattern

class SofistikPattern(Pattern):
    """Sofistik implementation of :class:`compas_fea2.problem.patterns.Pattern`.\n
    """
    __doc__ += Pattern.__doc__

    def __init__(self, load, distribution, name=None, **kwargs):
        super(SofistikPattern, self).__init__(load=load, distribution=distribution, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

