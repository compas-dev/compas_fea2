"""
********************************************************************************
opensees.model
********************************************************************************

.. currentmodule:: compas_fea2.backends.opensees.model

Model
=====

.. autosummary::
    :toctree: generated/

    Model

Instances
=========

.. autosummary::
    :toctree: generated/

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

Interactions
============

.. autosummary::
    :toctree: generated/

    Interaction

Materials
=========

.. autosummary::
    :toctree: generated/

    ElasticIsotropic
    Stiff
    ElasticOrthotropic
    ElasticPlastic
    Steel
    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    UserMaterial


Sections
========

.. autosummary::
    :toctree: generated/

    MassSection
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

from .model import Model
from .parts import Part
from .nodes import Node
# from .interactions import *
# from .sets import *
# from .constraints import *
from .elements import (BeamElement,
                       )
from .materials import (ElasticIsotropic,
                        )
from .sections import (RectangularSection,
                       )
from .bcs import (FixedBC,
                  PinnedBC,
                  FixedBCXX,
                  FixedBCYY,
                  FixedBCZZ,
                  RollerBCX,
                  RollerBCY,
                  RollerBCZ,
                  RollerBCXY,
                  RollerBCYZ,
                  RollerBCXZ
                  )
