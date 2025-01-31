from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .step import GeneralStep


class DynamicStep(GeneralStep):
    """Step for dynamic analysis."""

    def __init__(self, **kwargs):
        super(DynamicStep, self).__init__(**kwargs)
        raise NotImplementedError

    def __data__(self):
        data = super(DynamicStep, self).__data__()
        # Add DynamicStep specific data here
        return data

    @classmethod
    def __from_data__(cls, data):
        obj = super(DynamicStep, cls).__from_data__(data)
        # Initialize DynamicStep specific attributes here
        return obj

    def add_harmonic_point_load(self):
        raise NotImplementedError

    def add_harmonic_preassure_load(self):
        raise NotImplementedError
