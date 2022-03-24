"""
********************************************************************************
problem
********************************************************************************

.. currentmodule:: compas_fea2.problem

Problem
=======

.. autosummary::
    :toctree: generated/

    Problem

Steps
=====

.. autosummary::
    :toctree: generated/

    Step
    GeneralStep
    HeatStep
    ModalStep
    HarmonicStep
    BucklingStep
    AcousticStep

Loads
=====

.. autosummary::
    :toctree: generated/

    Load
    PointLoad
    PrestressLoad
    LineLoad
    AreaLoad
    GravityLoad
    ThermalLoad
    TributaryLoad
    HarmonicPointLoad
    HarmonicPressureLoad
    AcousticDiffuseFieldLoad

Displacements
=============

.. autosummary::
    :toctree: generated/

    GeneralDisplacement

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .problem import Problem
from .displacements import GeneralDisplacement
from .loads import (
    Load,
    # PrestressLoad,
    PointLoad,
    LineLoad,
    AreaLoad,
    GravityLoad,
    # TributaryLoad,
    # HarmonicPointLoad,
    # HarmonicPressureLoad,
    # AcousticDiffuseFieldLoad
)
from .steps import (
    Step,
    GeneralStep,
    StaticStep,
    # StaticLinearPerturbationStep,
    # HeatStep,
    ModalStep,
    # HarmonicStep,
    # BucklingStep,
    AcousticStep
)
from .outputs import (
    FieldOutput,
    HistoryOutput
)

__all__ = [
    'Problem',

    'GeneralDisplacement',
    'Load',
    'PrestressLoad',
    'PointLoad',
    'LineLoad',
    'AreaLoad',
    'GravityLoad',
    'TributaryLoad',
    'HarmonicPointLoad',
    'HarmonicPressureLoad',
    'AcousticDiffuseFieldLoad',
    'Step',
    'GeneralStaticStep',
    'StaticLinearPerturbationStep',
    'HeatStep',
    'ModalStep',
    'HarmonicStep',
    'BucklingStep',
    'AcousticStep',
    'FieldOutput',
    'HistoryOutput'
]
