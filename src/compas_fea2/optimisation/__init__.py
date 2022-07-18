"""
********************************************************************************
optimisation
********************************************************************************

.. currentmodule:: compas_fea2.optimisation

Problem
=======

.. autosummary::
    :toctree: generated/

    OptimisationProblem
    TopOptSensitivity


Constraints
===========

.. autosummary::
    :toctree: generated/

    OptimisationConstraint

Response
========

.. autosummary::
    :toctree: generated/

    EnergyStiffnessResponse
    VolumeResponse

Objectives
==========

.. autosummary::
    :toctree: generated/

    ObjectiveFunction

Variables
=========

.. autosummary::
    :toctree: generated/

    DesignVariables

Parameters
==========

.. autosummary::
    :toctree: generated/

    OptimisationParameters
    SmoothingParameters

"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .constraints import OptimisationConstraint
from .responses import EnergyStiffnessResponse, VolumeResponse
from .objectives import ObjectiveFunction
from .variables import DesignVariables
from .parameters import OptimisationParameters, SmoothingParameters
from .problem import OptimisationProblem, TopOptSensitivity


__all__ = [
    'OptimisationConstraint',

    'EnergyStiffnessResponse',
    'VolumeResponse',

    'ObjectiveFunction',
    'DesignVariables',

    'OptimisationParameters',
    'SmoothingParameters',

    'OptimisationProblem',
    'TopOptSensitivity',
]
