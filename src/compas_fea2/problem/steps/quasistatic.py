from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData
from .step import _Step


class QuasiStaticStep(_Step):
    """Step for quasi-static analysis.

    Parameters
    ----------
    None

    Attributes
    ----------
    None

    """

    def __init__(self, name=None, **kwargs):
        super(QuasiStaticStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError


class DirectCyclicStep(_Step):
    """Step for a direct cyclic analysis.

    Parameters
    ----------
    None

    Attributes
    ----------
    None

    """

    def __init__(self, name=None, **kwargs):
        super(DirectCyclicStep, self).__init__(name=name, **kwargs)
        raise NotImplementedError
