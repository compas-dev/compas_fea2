"""
********************************************************************************
Base
********************************************************************************

This is the Base implementation of compas_fea2, where the individual backends
inherit from.

.. currentmodule:: compas_fea2.backends._base.model


Elements
========

.. autosummary::
    :toctree: generated/

    BeamElementBase
    TrussElementBase
    ShellElementBase
    MembraneElementBase
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
    ConcreteBase
    ConcreteSmearedCrackBase
    ConcreteDamagedPlasticityBase
    ElasticIsotropicBase
    StiffBase
    ElasticOrthotropicBase
    ElasticPlasticBase
    ThermalMaterialBase
    SteelBase


Sections
========

.. autosummary::
    :toctree: generated/

    SectionBase
    AngleSectionBase
    BoxSectionBase
    CircularSectionBase
    GeneralSectionBase
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
    SpringSectionBase


.. currentmodule:: compas_fea2.backends._base.problem

Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    GeneralDisplacementBase
    FixedDisplacementBase
    PinnedDisplacementBase
    FixedDisplacementXXBase
    FixedDisplacementYYBase
    FixedDisplacementZZBase
    RollerDisplacementXBase
    RollerDisplacementYBase
    RollerDisplacementZBase
    RollerDisplacementXYBase
    RollerDisplacementYZBase
    RollerDisplacementXZBase

Loads
=====

.. autosummary::
    :toctree: generated/

    LoadBase
    PointLoadBase
    PointLoadsBase
    LineLoadBase
    AreaLoadBase
    GravityLoadBase
    ThermalLoadBase
    TributaryLoadBase
    HarmonicPointLoadBase
    HarmonicPressureLoadBase
    AcousticDiffuseFieldLoadBase

Steps
=====

.. autosummary::
    :toctree: generated/

    StepBase
    GeneralStepBase
    HeatStepBase
    ModalStepBase
    HarmonicStepBase
    BucklingStepBase
    AcousticStepBase

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = [name for name in dir() if not name.startswith('_')]
