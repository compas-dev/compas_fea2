"""
********************************************************************************
Base
********************************************************************************

This is the Base implementation of compas_fea2, where the individual backends
inherit from.


MODEL
=====

.. currentmodule:: compas_fea2.backends._base.model

Model
-----

.. autosummary::
    :toctree: generated/

    ModelBase

Parts
-----

.. autosummary::
    :toctree: generated/

    PartBase

Nodes
-----

.. autosummary::
    :toctree: generated/

    NodeBase

Elements
--------

.. autosummary::
    :toctree: generated/

    ElementBase
    BeamElementBase
    ShellElementBase
    SolidElementBase

Constraints
-----------

.. autosummary::
    :toctree: generated/

    ConstraintBase
    TieConstraintBase

Materials
---------

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
--------

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
-------------------

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
------

.. autosummary::
    :toctree: generated/

    NodesGroupBase
    ElementsGroupBase


PROBLEM
=======

.. currentmodule:: compas_fea2.backends._base.problem

Problem
-------

.. autosummary::
    :toctree: generated/

    ProblemBase

Cases
-----

.. autosummary::
    :toctree: generated/

    CaseBase
    GeneralCaseBase
    HeatCaseBase
    ModalCaseBase
    HarmonicCaseBase
    BucklingCaseBase
    AcousticCaseBase

Loads
-----

.. autosummary::
    :toctree: generated/

    LoadBase
    PointLoadBase
    PrestressLoadBase
    LineLoadBase
    AreaLoadBase
    GravityLoadBase
    ThermalLoadBase
    TributaryLoadBase
    HarmonicPointLoadBase
    HarmonicPressureLoadBase
    AcousticDiffuseFieldLoadBase

Displacements
-------------

.. autosummary::
    :toctree: generated/

    GeneralDisplacementBase


RESULTS
=======

.. currentmodule:: compas_fea2.backends._base.results

.. autosummary::
    :toctree: generated/

    ResultsBase
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = [name for name in dir() if not name.startswith('_')]
