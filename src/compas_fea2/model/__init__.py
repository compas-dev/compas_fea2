"""
********************************************************************************
model
********************************************************************************

.. currentmodule:: compas_fea2.model

Model
=====

.. autosummary::
    :toctree: generated/

    ModelBase

Parts
=====

.. autosummary::
    :toctree: generated/

    PartBase

Nodes
=====

.. autosummary::
    :toctree: generated/

    NodeBase

Elements
========

.. autosummary::
    :toctree: generated/

    ElementBase
    BeamElementBase
    ShellElementBase
    SolidElementBase

Constraints
===========

.. autosummary::
    :toctree: generated/

    ConstraintBase
    TieConstraintBase

Materials
=========

.. autosummary::
    :toctree: generated/

    MaterialBase
    StiffBase
    ElasticIsotropicBase
    ElasticOrthotropicBase
    ElasticPlasticBase
    ConcreteBase
    ConcreteSmearedCrackBase
    ConcreteDamagedPlasticityBase
    SteelBase
    ThermalMaterialBase

Sections
========

.. autosummary::
    :toctree: generated/

    SectionBase
    BeamSectionBase
    SpringSectionBase
    AngleSectionBase
    BoxSectionBase
    CircularSectionBase
    ISectionBase
    PipeSectionBase
    RectangularSectionBase
    ShellSectionBase
    MembraneSectionBase
    SolidSectionBase
    TrapezoidalSectionBase
    TrussSectionBase
    StrutSectionBase
    TieSectionBase
    MassSectionBase

Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    GeneralBCBase
    FixedBCBase
    PinnedBCBase
    FixedBCXXBase
    FixedBCYYBase
    FixedBCZZBase
    RollerBCXBase
    RollerBCYBase
    RollerBCZBase
    RollerBCXYBase
    RollerBCYZBase
    RollerBCXZBase

Groups
======

.. autosummary::
    :toctree: generated/

    NodesGroupBase
    ElementsGroupBase

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from .model import ModelBase
from .parts import PartBase
from .nodes import NodeBase
from .elements import (
    ElementBase,
    MassElementBase,
    BeamElementBase,
    SpringElementBase,
    TrussElementBase,
    StrutElementBase,
    TieElementBase,
    ShellElementBase,
    MembraneElementBase,
    # FaceElementBase,
    SolidElementBase,
    PentahedronElementBase,
    TetrahedronElementBase,
    HexahedronElementBase,
)
from .materials import (
    MaterialBase,
    ConcreteBase,
    ConcreteSmearedCrackBase,
    ConcreteDamagedPlasticityBase,
    ElasticIsotropicBase,
    StiffBase,
    ElasticOrthotropicBase,
    ElasticPlasticBase,
    ThermalMaterialBase,
    SteelBase
)
from .sections import (
    SectionBase,
    MassSectionBase,
    BeamSectionBase,
    SpringSectionBase,
    AngleSectionBase,
    BoxSectionBase,
    CircularSectionBase,
    ISectionBase,
    PipeSectionBase,
    RectangularSectionBase,
    ShellSectionBase,
    MembraneSectionBase,
    SolidSectionBase,
    TrapezoidalSectionBase,
    TrussSectionBase,
    StrutSectionBase,
    TieSectionBase,
)
from .constraints import (
    ConstraintBase,
    TieConstraintBase,
)
from .groups import (
    GroupBase,
    NodesGroupBase,
    ElementsGroupBase,
    PartsGroup
)
from .releases import (
    BeamEndReleaseBase,
)
from .bcs import (
    GeneralBCBase,
    FixedBCBase,
    PinnedBCBase,
    FixedBCXXBase,
    FixedBCYYBase,
    FixedBCZZBase,
    RollerBCXBase,
    RollerBCYBase,
    RollerBCZBase,
    RollerBCXYBase,
    RollerBCYZBase,
    RollerBCXZBase
)


__all__ = [
    'ModelBase',
    'PartBase',
    'NodeBase',
    'ElementBase',
    'MassElementBase',
    'BeamElementBase',
    'SpringElementBase',
    'TrussElementBase',
    'StrutElementBase',
    'TieElementBase',
    'ShellElementBase',
    'MembraneElementBase',
    'SolidElementBase',
    'PentahedronElementBase',
    'TetrahedronElementBase',
    'HexahedronElementBase',
    'MaterialBase',
    'ConcreteBase',
    'ConcreteSmearedCrackBase',
    'ConcreteDamagedPlasticityBase',
    'ElasticIsotropicBase',
    'StiffBase',
    'ElasticOrthotropicBase',
    'ElasticPlasticBase',
    'ThermalMaterialBase',
    'SteelBase',
    'SectionBase',
    'MassSectionBase',
    'BeamSectionBase',
    'SpringSectionBase',
    'AngleSectionBase',
    'BoxSectionBase',
    'CircularSectionBase',
    'ISectionBase',
    'PipeSectionBase',
    'RectangularSectionBase',
    'ShellSectionBase',
    'MembraneSectionBase',
    'SolidSectionBase',
    'TrapezoidalSectionBase',
    'TrussSectionBase',
    'StrutSectionBase',
    'TieSectionBase',
    'ConstraintBase',
    'TieConstraintBase',
    'GroupBase',
    'NodesGroupBase',
    'ElementsGroupBase',
    'PartsGroup',
    'BeamEndReleaseBase',
    'GeneralBCBase',
    'FixedBCBase',
    'PinnedBCBase',
    'FixedBCXXBase',
    'FixedBCYYBase',
    'FixedBCZZBase',
    'RollerBCXBase',
    'RollerBCYBase',
    'RollerBCZBase',
    'RollerBCXYBase',
    'RollerBCYZBase',
    'RollerBCXZBase',
]
