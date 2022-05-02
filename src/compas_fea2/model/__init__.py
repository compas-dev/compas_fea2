"""
********************************************************************************
model
********************************************************************************

.. currentmodule:: compas_fea2.model

Model
=====

.. autosummary::
    :toctree: generated/

    Model

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

    _Element
    BeamElement
    ShellElement
    SolidElement

Releases
========

.. autosummary::
    :toctree: generated/

    _BeamEndRelease
    BeamEndPinRelease
    BeamEndSliderRelease

Constraints
===========

.. autosummary::
    :toctree: generated/

    _Constraint
    TieConstraint

Interactions
============

.. autosummary::
    :toctree: generated/

    _Interaction
    Contact
    HardContactNoFriction
    HardContactFrictionPenalty

Interfaces
==========

.. autosummary::
    :toctree: generated/

    Interface

Materials
=========

.. autosummary::
    :toctree: generated/

    _Material
    UserMaterial
    Stiff
    ElasticIsotropic
    ElasticOrthotropic
    ElasticPlastic
    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    Steel

Sections
========

.. autosummary::
    :toctree: generated/

    _Section
    BeamSection
    SpringSection
    AngleSection
    BoxSection
    CircularSection
    HexSection
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
    MassSection

Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    BoundaryCondition
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
======

.. autosummary::
    :toctree: generated/

    _Group
    NodesGroup
    ElementsGroup
    FacesGroup
    PartsGroup

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .model import Model
from .parts import Part
from .nodes import Node
from .elements import (
    _Element,
    MassElement,
    BeamElement,
    SpringElement,
    TrussElement,
    StrutElement,
    TieElement,
    ShellElement,
    MembraneElement,
    SolidElement,
)
from .materials import (
    _Material,
    Concrete,
    ConcreteSmearedCrack,
    ConcreteDamagedPlasticity,
    ElasticIsotropic,
    Stiff,
    UserMaterial,
    ElasticOrthotropic,
    ElasticPlastic,
    Steel,
    Timber,
)
from .interfaces import Interface
from .interactions import (
    _Interaction,
    Contact,
    HardContactFrictionPenalty,
    HardContactNoFriction,
)
from .sections import (
    _Section,
    MassSection,
    BeamSection,
    SpringSection,
    AngleSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    PipeSection,
    RectangularSection,
    ShellSection,
    MembraneSection,
    SolidSection,
    TrapezoidalSection,
    TrussSection,
    StrutSection,
    TieSection,
)
from .constraints import (
    _Constraint,
    TieConstraint,
)
from .groups import (
    _Group,
    NodesGroup,
    ElementsGroup,
    FacesGroup,
    PartsGroup,
)
from .releases import (
    _BeamEndRelease,
    BeamEndPinRelease,
    BeamEndSliderRelease,
)
from .bcs import (
    BoundaryCondition,
    FixedBC,
    PinnedBC,
    FixedBCXX,
    FixedBCYY,
    FixedBCZZ,
    RollerBCX,
    RollerBCY,
    RollerBCZ,
    RollerBCXY,
    RollerBCYZ,
    RollerBCXZ,
)


__all__ = [
    'Model',

    'Part',
    'Node',

    '_Element',
    'MassElement',
    'BeamElement',
    'SpringElement',
    'TrussElement',
    'StrutElement',
    'TieElement',
    'ShellElement',
    'MembraneElement',
    'SolidElement',

    '_Material',
    'UserMaterial',
    'Concrete',
    'ConcreteSmearedCrack',
    'ConcreteDamagedPlasticity',
    'ElasticIsotropic',
    'Stiff',
    'ElasticOrthotropic',
    'ElasticPlastic',
    'Steel',
    'Timber',

    'HardContactFrictionPenalty',

    '_Section',
    'MassSection',
    'BeamSection',
    'SpringSection',
    'AngleSection',
    'BoxSection',
    'CircularSection',
    'HexSection',
    'ISection',
    'PipeSection',
    'RectangularSection',
    'ShellSection',
    'MembraneSection',
    'SolidSection',
    'TrapezoidalSection',
    'TrussSection',
    'StrutSection',
    'TieSection',

    '_Constraint',
    'TieConstraint',

    '_BeamEndRelease',
    'BeamEndPinRelease',

    '_Interaction',
    'Contact',
    'HardContactNoFriction',
    'HardContactFrictionPenalty',

    'Interface',

    '_Group',
    'NodesGroup',
    'ElementsGroup',
    'FacesGroup',
    'PartsGroup',


    'BoundaryCondition',
    'FixedBC',
    'PinnedBC',
    'FixedBCXX',
    'FixedBCYY',
    'FixedBCZZ',
    'RollerBCX',
    'RollerBCY',
    'RollerBCZ',
    'RollerBCXY',
    'RollerBCYZ',
    'RollerBCXZ',
]
