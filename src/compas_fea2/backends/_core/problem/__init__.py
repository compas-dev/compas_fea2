"""
********************************************************************************
_core.components
********************************************************************************

.. currentmodule:: compas_fea2.backends._core.components


Structure
=========

.. autosummary::
    :toctree: generated/

    StructureBase


Constraints
===========

.. autosummary::
    :toctree: generated/

    ConstraintBase
    TieConstraintBase


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
    MassElementBase
    BeamElementBase
    SpringElementBase
    TrussElementBase
    StrutElementBase
    TieElementBase
    ShellElementBase
    MembraneElementBase
    FaceElementBase
    SolidElementBase
    PentahedronElementBase
    TetrahedronElementBase
    HexahedronElementBase


Properties
==========
.. autosummary::
    :toctree: generated/

    ElementPropertiesBase


Loads
=====

.. autosummary::
    :toctree: generated/

    LoadBase
    PrestressLoadBase
    PointLoadBase
    PointLoadsBase
    LineLoadBase
    AreaLoadBase
    GravityLoadBase
    TributaryLoadBase
    HarmonicPointLoadBase


Materials
=========

.. autosummary::
    :toctree: generated/

    MaterialBase
    ConcreteBase
    ConcreteSmearedCrackBase
    ConcreteDamagedPlasticityBase
    StiffBase
    ElasticIsotropicBase
    ElasticOrthotropicBase
    ElasticPlasticBase
    SteelBase


Misc
====

.. autosummary::
    :toctree: generated/

    MiscBase
    AmplitudeBase
    TemperaturesBase


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


Load Cases
==========

.. autosummary::
    :toctree: generated/

    StepBase
    GeneralStepBase
    ModalStepBase
    HarmonicStepBase
    BucklingStepBase


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .problem import *
from .bcs import *
# from .load_cases import *
# from .load_combos import *
from .loads import *
from .steps import *


__all__ = [name for name in dir() if not name.startswith('_')]
