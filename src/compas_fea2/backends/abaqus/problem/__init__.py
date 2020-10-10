"""
********************************************************************************
abaqus.problem
********************************************************************************

.. currentmodule:: compas_fea2.backends.abaqus.problem

Problem
=======
.. autosummary::
    :toctree: generated/

    Problem

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

    PointLoad
    LineLoad
    AreaLoad
    GravityLoad
    TributaryLoad
    HarmoniPointLoadBase

Steps
=====

.. autosummary::
    :toctree: generated/

    GeneralStaticStep
    StaticLinearPertubationStep
    ModalStep
    HarmoniStepBase
    BucklingStep
    AcoustiStepBase


Output Requests
===============

.. autosummary::
    :toctree: generated/

    FieldOutput
    HistoryOutput

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# additional software-based classes
from .bcs import *
from .steps import *
from .loads import *
from .outputs import *
from .problem import *


__all__ = [name for name in dir() if not name.startswith('_')]

