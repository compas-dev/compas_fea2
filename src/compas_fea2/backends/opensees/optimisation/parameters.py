from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# TODO remove dataclasses
from dataclasses import dataclass
from compas_fea2.optimisation.parameters import OptimisationParameters, SmoothingParameters


@dataclass
class OpenseesOptimisationParameters(OptimisationParameters):
    pass


@dataclass
class OpenseesSmoothingParameters(SmoothingParameters):
    pass
