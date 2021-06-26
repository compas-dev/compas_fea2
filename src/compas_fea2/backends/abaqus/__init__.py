"""
********************************************************************************
Abaqus
********************************************************************************

This is the Abaqus implementation of compas_fea2.

The following classes are used for the generation of the Model to be analysed in
Abaqus

.. currentmodule:: compas_fea2.backends.abaqus.model


Model
=====

.. autosummary::
    :toctree: generated/

    Model
    Instance

Parts
=====

.. autosummary::
    :toctree: generated/

    Part

Nodes
=====

.. autosummary::
    :toctree: generated/

    Node

Elements
========

.. autosummary::
    :toctree: generated/

    MassElement
    BeamElement
    TrussElement
    ShellElement
    MembraneElement
    SolidElement

Constraints
===========

.. autosummary::
    :toctree: generated/

    Constraint
    TieConstraint

Interactions
============

.. autosummary::
    :toctree: generated/

    Interaction

Materials
=========

.. autosummary::
    :toctree: generated/

    ElasticIsotropic
    Stiff
    ElasticOrthotropic
    ElasticPlastic
    Steel
    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    UserMaterial


Sections
========

.. autosummary::
    :toctree: generated/

    MassSection
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

Sets
====

.. autosummary::
    :toctree: generated/

    Set
    Surface

The following classes are used to set up the analysis problem

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

from .model import *
from .problem import *
from .results import *

__all__ = [name for name in dir() if not name.startswith('_')]
