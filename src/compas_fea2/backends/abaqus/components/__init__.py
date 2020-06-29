"""
********************************************************************************
abaqus.components
********************************************************************************

.. currentmodule:: compas_fea2.backends.abaqus.components


Assembly
========

.. autosummary::
    :toctree: generated/

    Assembly
    Instance

Parts
=====

.. autosummary::
    :toctree: generated/

    Part

Constraints
===========

.. autosummary::
    :toctree: generated/

    Constraint
    TieConstraint


Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    GeneralDisplacement
    FixedDisplacement
    PinnedDisplacement
    FixedDisplacementXX
    FixedDisplacementYY
    FixedDisplacementZZ
    RollerDisplacementX
    RollerDisplacementY
    RollerDisplacementZ
    RollerDisplacementXY
    RollerDisplacementYZ
    RollerDisplacementXZ

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
    FaceElement
    SolidElement
    PentahedronElement
    TetrahedronElement
    HexahedronElement


Properties
==========
.. autosummary::
    :toctree: generated/

    ElementProperties


Loads
=====

.. autosummary::
    :toctree: generated/

    Load
    PrestressLoad
    PointLoad
    PointLoads
    LineLoad
    AreaLoad
    GravityLoad
    TributaryLoad
    HarmoniPointLoadBase


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


Misc
====

.. autosummary::
    :toctree: generated/

    Misc
    Amplitude
    Temperatures


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


Steps
=====

.. autosummary::
    :toctree: generated/

    Step
    GeneralStep
    ModalStep
    HarmoniStepBase
    BucklingStep


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

# additional software-based classes
from .nodes import *
from .assembly import *
from .parts import *
from .interactions import *
from .bcs import *
from .sets import *
from .constraints import *
from .elements import *
from .steps import *
#from .load_cases import *
#from .load_combos import *
from .loads import *
from .materials import *
# from .properties import *
from .sections import *
from .misc import *
from .outputs import *


__all__ = [name for name in dir() if not name.startswith('_')]

