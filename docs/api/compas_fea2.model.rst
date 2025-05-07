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
    RigidPart

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
    MassElement
    BeamElement
    SpringElement
    TrussElement
    StrutElement
    TieElement
    ShellElement
    MembraneElement
    _Element3D
    TetrahedronElement
    HexahedronElement

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
    _MultiPointConstraint
    TieMPC
    BeamMPC
    TieConstraint

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
    Timber

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

    _BoundaryCondition
    GeneralBC
    FixedBC
    PinnedBC
    ClampBCXX
    ClampBCYY
    ClampBCZZ
    RollerBCX
    RollerBCY
    RollerBCZ
    RollerBCXY
    RollerBCYZ
    RollerBCXZ

Initial Conditions
==================

.. autosummary::
    :toctree: generated/

    _InitialCondition
    InitialTemperatureField
    InitialStressField

Groups
======

.. autosummary::
    :toctree: generated/

    _Group
    NodesGroup
    ElementsGroup
    FacesGroup
    PartsGroup
