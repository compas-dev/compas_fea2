"""
********************************************************************************
abaqus.model
********************************************************************************

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

Properties
==========

.. autosummary::
    :toctree: generated/

    ElementProperties


Materials
=========

.. autosummary::
    :toctree: generated/

    Material
    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    Stiff
    ElasticIsotropic
    ElasticOrthotropic
    ElasticPlastic
    Steel
    UserMaterial


Sections
========

.. autosummary::
    :toctree: generated/

    Section
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

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# additional software-based classes
from .model import *
from .parts import *
from .nodes import *
from .interactions import *
from .sets import *
from .constraints import *
from .elements import *
from .materials import *
from .sections import *


__all__ = [name for name in dir() if not name.startswith('_')]

