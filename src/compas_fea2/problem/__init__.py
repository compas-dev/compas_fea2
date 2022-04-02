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

    _Step
    ModalStep
    GeneralStep
    StaticStep


Loads
=====

.. autosummary::
    :toctree: generated/

    _Load
    PointLoad
    PrestressLoad
    LineLoad
    AreaLoad
    GravityLoad
    TributaryLoad

Displacements
=============

.. autosummary::
    :toctree: generated/

    GeneralDisplacement

Outputs
=======

.. autosummary::
    :toctree: generated/

    FieldOutput
    HistoryOutput
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .problem import Problem
from .displacements import GeneralDisplacement
from .loads import (
    _Load,
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
    _Step,
    ModalStep,
    GeneralStep,
    StaticStep,
    # StaticLinearPerturbationStep,
    # HeatStep,
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

    '_Load',
    # 'PrestressLoad',
    'PointLoad',
    'LineLoad',
    'AreaLoad',
    'GravityLoad',
    # 'TributaryLoad',
    # 'HarmonicPointLoad',
    # 'HarmonicPressureLoad',
    # 'AcousticDiffuseFieldLoad',

    '_Step',
    'GeneralStep',
    'StaticStep',
    # 'StaticLinearPerturbationStep',
    # 'HeatStep',
    'ModalStep',
    # 'HarmonicStep',
    # 'BucklingStep',
    'AcousticStep',

    'FieldOutput',
    'HistoryOutput'
]
