from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from .step import _Step


class DynamicStep(_Step):
    """"""

    def __init__(self, name=None, **kwargs):
        super(DynamicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError()

    def add_harmonic_point_load(self):
        raise NotImplementedError

    def add_harmonic_preassure_load(self):
        raise NotImplementedError
