"""
********************************************************************************
opensees.model
********************************************************************************

.. currentmodule:: compas_fea2.backends.opensees.model


Constraints
===========

.. autosummary::
    :toctree: generated/

    Constraint
    TieConstraint


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


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# additional software-based classes
from .set import * #TODO remove
from .constraints import *
from .elements import *
from .materials import *
from .sections import *


__all__ = [name for name in dir() if not name.startswith('_')]
