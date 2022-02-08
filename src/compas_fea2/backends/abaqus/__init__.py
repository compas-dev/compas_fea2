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

import compas_fea2

from compas.plugins import plugin
from compas_fea2.model import Model
from compas_fea2.problem import Problem

from .model import AbaqusModel
from .problem import AbaqusProblem


@plugin(category='fea_backends')
def register_backend():
    compas_fea2.BACKENDS['abaqus'][Model] = AbaqusModel
    compas_fea2.BACKENDS['abaqus'][Problem] = AbaqusProblem

    print('Abaqus implementations registered...')


__all__ = [name for name in dir() if not name.startswith('_')]
