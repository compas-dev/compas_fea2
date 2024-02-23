from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .step import GeneralStep


class QuasiStaticStep(GeneralStep):
    """Step for quasi-static analysis."""

    def __init__(self, name=None, **kwargs):
        super(QuasiStaticStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError


class DirectCyclicStep(GeneralStep):
    """Step for a direct cyclic analysis."""

    def __init__(self, name=None, **kwargs):
        super(DirectCyclicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError
