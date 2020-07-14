"""
********************************************************************************
abaqus.problem
********************************************************************************

.. currentmodule:: compas_fea2.backends.abaqus.problem


Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    GeneralDisplacement
    FixedDisplacement
    PinnedDisplacement
    FixedDisplacementXX
    FixedDisplacementYY
    FixedDisplacementZZ
    RollerDisplacementX
    RollerDisplacementY
    RollerDisplacementZ
    RollerDisplacementXY
    RollerDisplacementYZ
    RollerDisplacementXZ


Loads
=====

.. autosummary::
    :toctree: generated/

    Load
    PrestressLoad
    PointLoad
    PointLoads
    LineLoad
    AreaLoad
    GravityLoad
    TributaryLoad
    HarmoniPointLoadBase


Misc
====

.. autosummary::
    :toctree: generated/

    Misc
    Amplitude
    Temperatures


Steps
=====

.. autosummary::
    :toctree: generated/

    Step
    GeneralStep
    ModalStep
    HarmoniStepBase
    BucklingStep


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# additional software-based classes
from .bcs import *
from .steps import *
from .loads import *
from .misc import *
from .outputs import *
from .problem import *


__all__ = [name for name in dir() if not name.startswith('_')]

