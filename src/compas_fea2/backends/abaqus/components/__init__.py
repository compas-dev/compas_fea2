"""
********************************************************************************
Abaqus Analysis Components
********************************************************************************

.. currentmodule:: compas_fea.backends.abaqus.components


Structure
=========

.. autosummary::
    :toctree: generated/

    Structure


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


Elements
========

.. autosummary::
    :toctree: generated/

    Node
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


Load Cases
==========

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


# additional software-based classes
from .bcs import *
from .set import *
from .structure import *
from .constraints import *
from .elements import *
from .steps import *
#from .load_cases import *
#from .load_combos import *
from .loads import *
from .materials import *
from .properties import *
from .sections import *
from .misc import *


__all__ = [name for name in dir() if not name.startswith('_')]
