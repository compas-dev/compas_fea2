from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .step import GeneralStep


class DynamicStep(GeneralStep):
    """Step for dynamic analysis."""

    def __init__(self, **kwargs):
        super(DynamicStep, self).__init__(**kwargs)
        raise NotImplementedError

    def add_harmonic_point_load(self):
        raise NotImplementedError

    def add_harmonic_preassure_load(self):
        raise NotImplementedError
