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

    DeformablePart
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

    Element
    MassElement
    BeamElement
    SpringElement
    TrussElement
    StrutElement
    TieElement
    ShellElement
    MembraneElement
    Element3D
    TetrahedronElement
    HexahedronElement

Releases
========

.. autosummary::
    :toctree: generated/

    BeamEndRelease
    BeamEndPinRelease
    BeamEndSliderRelease

Constraints
===========

.. autosummary::
    :toctree: generated/

    Constraint
    MultiPointConstraint
    TieMPC
    BeamMPC
    TieConstraint

Materials
=========

.. autosummary::
    :toctree: generated/

    Material
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

    Section
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

    InitialCondition
    InitialTemperatureField
    InitialStressField

Groups
======

.. autosummary::
    :toctree: generated/

    Group
    NodesGroup
    ElementsGroup
    FacesGroup
    PartsGroup
