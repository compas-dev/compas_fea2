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

Model
-----

.. autosummary::
    :toctree: generated/

    Model

Parts
-----

.. autosummary::
    :toctree: generated/

    Part

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
    ShellElement
    SolidElement

Constraints
-----------

.. autosummary::
    :toctree: generated/

    NodeTieConstraint

Materials
---------

.. autosummary::
    :toctree: generated/

    ElasticIsotropic
    ElasticOrthotropic
    ElasticPlastic
    Stiff
    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    Steel
    ThermalMaterial


Sections
--------

.. autosummary::
    :toctree: generated/

    AngleSection
    BoxSection
    CircularSection
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

Groups
------

.. autosummary::
    :toctree: generated/

    NodesGroup
    ElementsGroup

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
    ModalStep

Loads
-----

.. autosummary::
    :toctree: generated/

    PointLoad
    GravityLoad

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
