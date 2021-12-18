"""
********************************************************************************
Abaqus
********************************************************************************

This is the Abaqus implementation of compas_fea2.

The following classes are used for the generation of the Model to be analysed in
Abaqus


MODEL
=====

.. currentmodule:: compas_fea2.backends.abaqus.model

.. autosummary::
    :toctree: generated/

    Model

Nodes
-----

.. autosummary::
    :toctree: generated/

    Node

Elements
--------

.. autosummary::
    :toctree: generated/

    BeamElement
    TrussElement
    ShellElement
    MembraneElement
    SolidElement

Constraints
-----------

.. autosummary::
    :toctree: generated/

    Constraint
    TieConstraint

Materials
---------

.. autosummary::
    :toctree: generated/

    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    ElasticIsotropic
    Stiff
    ElasticOrthotropic
    ElasticPlastic
    ThermalMaterial
    Steel


Sections
--------

.. autosummary::
    :toctree: generated/

    AngleSection
    BoxSection
    CircularSection
    GeneralSection
    ISection
    PipeSection
    RectangularSection
    ShellSection
    MembraneSection
    SolidSection
    TrapezoidalSection
    TrussSection
    StrutSection
    TieSection
    SpringSection

Boundary Conditions
-------------------

.. autosummary::
    :toctree: generated/

    FixedBC
    PinnedBC
    FixedBCXX
    FixedBCYY
    FixedBCZZ
    RollerBCX
    RollerBCY
    RollerBCZ
    RollerBCXY
    RollerBCYZ
    RollerBCXZ


PROBLEM
=======

.. currentmodule:: compas_fea2.backends.abaqus.problem

.. autosummary::
    :toctree: generated/

    Problem

Steps
-----

.. autosummary::
    :toctree: generated/

    GeneralStep
    HeatStep
    ModalStep
    HarmonicStep
    BucklingStep
    AcousticStep

Loads
-----

.. autosummary::
    :toctree: generated/

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
-------------

.. autosummary::
    :toctree: generated/

    GeneralDisplacement


RESULTS
=======

.. currentmodule:: compas_fea2.backends.abaqus.results

.. autosummary::
    :toctree: generated/

    Results
"""

from .model import *
from .problem import *
from .results import *

__all__ = [name for name in dir() if not name.startswith('_')]
