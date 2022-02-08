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

    Element
    BeamElement
    ShellElement
    SolidElement

Constraints
===========

.. autosummary::
    :toctree: generated/

    Constraint
    TieConstraint

Materials
=========

.. autosummary::
    :toctree: generated/

    Material
    Stiff
    ElasticIsotropic
    ElasticOrthotropic
    ElasticPlastic
    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    Steel
    ThermalMaterial

Sections
========

.. autosummary::
    :toctree: generated/

    Section
    BeamSection
    SpringSection
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
    MassSection

Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    GeneralBC
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

    NodesGroup
    ElementsGroup

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .model import Model
from .parts import Part
from .nodes import Node
from .elements import (
    Element,
    MassElement,
    BeamElement,
    SpringElement,
    TrussElement,
    StrutElement,
    TieElement,
    ShellElement,
    MembraneElement,
    SolidElement,
    PentahedronElement,
    TetrahedronElement,
    HexahedronElement,
)
from .materials import (
    Material,
    Concrete,
    ConcreteSmearedCrack,
    ConcreteDamagedPlasticity,
    ElasticIsotropic,
    Stiff,
    ElasticOrthotropic,
    ElasticPlastic,
    ThermalMaterial,
    Steel
)
from .interactions import ContactHardFrictionPenalty
from .sections import (
    Section,
    MassSection,
    BeamSection,
    SpringSection,
    AngleSection,
    BoxSection,
    CircularSection,
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
    Constraint,
    TieConstraint,
)
from .groups import (
    Group,
    NodesGroup,
    ElementsGroup,
    PartsGroup
)
from .releases import (
    BeamEndRelease,
)
from .bcs import (
    GeneralBC,
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

    'Element',
    'MassElement',
    'BeamElement',
    'SpringElement',
    'TrussElement',
    'StrutElement',
    'TieElement',
    'ShellElement',
    'MembraneElement',
    'SolidElement',
    'PentahedronElement',
    'TetrahedronElement',
    'HexahedronElement',

    'Material',
    'Concrete',
    'ConcreteSmearedCrack',
    'ConcreteDamagedPlasticity',
    'ElasticIsotropic',
    'Stiff',
    'ElasticOrthotropic',
    'ElasticPlastic',
    'ThermalMaterial',
    'Steel',

    'ContactHardFrictionPenalty',

    'Section',
    'MassSection',
    'BeamSection',
    'SpringSection',
    'AngleSection',
    'BoxSection',
    'CircularSection',
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

    'Constraint',
    'TieConstraint',

    'Group',
    'NodesGroup',
    'ElementsGroup',
    'PartsGroup',

    'BeamEndRelease',

    'GeneralBC',
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
