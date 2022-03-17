"""
********************************************************************************
Abaqus
********************************************************************************
<<<<<<< HEAD
=======

This is the Abaqus implementation of compas_fea2.

The following classes are used for the generation of the Model to be analysed in
Abaqus


MODEL
=====

.. currentmodule:: compas_fea2.backends.abaqus.model

Model
-----

.. autosummary::
    :toctree: generated/

    Model

Parts
-----

.. autosummary::
    :toctree: generated/

    Part

Nodes
-----

.. autosummary::
    :toctree: generated/

    Node

Elements
--------

.. autosummary::
    :toctree: generated/

    MassElement
    BeamElement
    TrussElement
    ShellElement
    SolidElement

Constraints
-----------

.. autosummary::
    :toctree: generated/

    NodeTieConstraint

Materials
---------

.. autosummary::
    :toctree: generated/

    ElasticIsotropic
    ElasticPlastic
    Stiff
    Concrete
    ConcreteSmearedCrack
    ConcreteDamagedPlasticity
    Steel
    UserMaterial

Sections
--------

.. autosummary::
    :toctree: generated/

    MassSection
    AngleSection
    BoxSection
    CircularSection
    HexSection
    ISection
    PipeSection
    RectangularSection
    TrapezoidalSection
    TrussSection
    ShellSection
    MembraneSection
    SolidSection

Boundary Conditions
-------------------

.. autosummary::
    :toctree: generated/

    FixedBC
    PinnedBC
    FixedBCXX
    FixedBCYY
    FixedBCZZ
    RollerBCX
    RollerBCY
    RollerBCZ
    RollerBCXY
    RollerBCYZ
    RollerBCXZ

Groups
------

.. autosummary::
    :toctree: generated/

    NodesGroup
    ElementsGroup

PROBLEM
=======

.. currentmodule:: compas_fea2.backends.abaqus.problem

.. autosummary::
    :toctree: generated/

    Problem

Steps
-----

.. autosummary::
    :toctree: generated/

    GeneralStep
    ModalStep

Loads
-----

.. autosummary::
    :toctree: generated/

    PointLoad
    GravityLoad

Displacements
-------------

.. autosummary::
    :toctree: generated/

    GeneralDisplacement


OPTIMISATION
============

.. currentmodule:: compas_fea2.backends.abaqus.optimisation

.. autosummary::
    :toctree: generated/

    OptimisationProblem
    OptimisationParameters
    OptimisationConstraint
    ObjectiveFunction
    DesignVariables
    VolumeResponse
    EnergyStiffnessResponse


RESULTS
=======

.. currentmodule:: compas_fea2.backends.abaqus.results

.. autosummary::
    :toctree: generated/

    Results
>>>>>>> 0fcf42ed8e1eb38788d736a3e47f207522be8a7c
"""

import compas_fea2

from compas.plugins import plugin
from compas_fea2.backends.abaqus.problem.displacements import AbaqusGeneralDisplacement
from compas_fea2.backends.abaqus.problem.loads import AbaqusAcousticDiffuseFieldLoad

from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import Node
# Elements
from compas_fea2.model import BeamElement
from compas_fea2.model import MassElement
from compas_fea2.model import MembraneElement
from compas_fea2.model import ShellElement
from compas_fea2.model import SolidElement
from compas_fea2.model import TrussElement
# Groups
from compas_fea2.model import ElementsGroup
from compas_fea2.model import NodesGroup
# Sections
from compas_fea2.model import AngleSection
from compas_fea2.model import BeamSection
from compas_fea2.model import BoxSection
from compas_fea2.model import CircularSection
from compas_fea2.model import ISection
from compas_fea2.model import MassSection
from compas_fea2.model import MembraneSection
from compas_fea2.model import PipeSection
from compas_fea2.model import RectangularSection
from compas_fea2.model import ShellSection
from compas_fea2.model import SolidSection
from compas_fea2.model import SpringSection
from compas_fea2.model import StrutSection
from compas_fea2.model import TieSection
from compas_fea2.model import TrapezoidalSection
from compas_fea2.model import TrussSection
# Materials
from compas_fea2.model import Concrete
from compas_fea2.model import ConcreteDamagedPlasticity
from compas_fea2.model import ConcreteSmearedCrack
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import ElasticOrthotropic
from compas_fea2.model import ElasticPlastic
from compas_fea2.model import Steel
from compas_fea2.model import Stiff
# Interactions
from compas_fea2.model import ContactHardFrictionPenalty
# Constraints
from compas_fea2.model import Constraint
# from compas_fea2.model import TieConstraint
# Boundary Conditions
from compas_fea2.model import FixedBC
from compas_fea2.model import FixedBCXX
from compas_fea2.model import FixedBCYY
from compas_fea2.model import FixedBCZZ
from compas_fea2.model import PinnedBC
from compas_fea2.model import RollerBCX
from compas_fea2.model import RollerBCXY
from compas_fea2.model import RollerBCXZ
from compas_fea2.model import RollerBCY
from compas_fea2.model import RollerBCYZ
from compas_fea2.model import RollerBCZ

# Problems
from compas_fea2.problem import Problem
# Loads
from compas_fea2.problem import AcousticDiffuseFieldLoad
from compas_fea2.problem import AreaLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import HarmonicPointLoad
from compas_fea2.problem import HarmonicPressureLoad
from compas_fea2.problem import LineLoad
from compas_fea2.problem import PointLoad
from compas_fea2.problem import TributaryLoad
# Displacements
from compas_fea2.problem import GeneralDisplacement
# Cases/Steps
# from compas_fea2.problem import AcousticCase
# from compas_fea2.problem import BucklingCase
# from compas_fea2.problem import GeneralStaticCase
# from compas_fea2.problem import HarmonicCase
# from compas_fea2.problem import HeatCase
# from compas_fea2.problem import ModalCase
# from compas_fea2.problem import StaticLinearPerturbationCase
# Outputs

# Abaqus Models
from .model import AbaqusModel
from .model import AbaqusPart
from .model import AbaqusNode
# Abaqus Elements
from .model import AbaqusBeamElement
from .model import AbaqusMassElement
from .model import AbaqusMembraneElement
from .model import AbaqusShellElement
from .model import AbaqusSolidElement
from .model import AbaqusTrussElement
# Abaqus Groups
from .model import AbaqusElementsGroup
from .model import AbaqusNodesGroup
# Abaqus Sections
from .model import AbaqusAngleSection
# from .model import AbaqusBeamSection
from .model import AbaqusBoxSection
from .model import AbaqusCircularSection
from .model import AbaqusISection
from .model import AbaqusMassSection
from .model import AbaqusMembraneSection
from .model import AbaqusPipeSection
from .model import AbaqusRectangularSection
from .model import AbaqusShellSection
from .model import AbaqusSolidSection
from .model import AbaqusSpringSection
from .model import AbaqusStrutSection
from .model import AbaqusTieSection
from .model import AbaqusTrapezoidalSection
from .model import AbaqusTrussSection
# Abaqus Materials
from .model import AbaqusConcrete
from .model import AbaqusConcreteDamagedPlasticity
from .model import AbaqusConcreteSmearedCrack
from .model import AbaqusElasticIsotropic
from .model import AbaqusElasticOrthotropic
from .model import AbaqusElasticPlastic
from .model import AbaqusSteel
from .model import AbaqusStiff
# Abaqus Interactions
from .model import AbaqusContactHardFrictionPenalty
# Abaqus Constraints
from .model import AbaqusConstraint
# from .model import AbaqusTieConstraint
# Abaqus Boundary Conditions
from .model import AbaqusFixedBC
from .model import AbaqusFixedBCXX
from .model import AbaqusFixedBCYY
from .model import AbaqusFixedBCZZ
from .model import AbaqusPinnedBC
from .model import AbaqusRollerBCX
from .model import AbaqusRollerBCXY
from .model import AbaqusRollerBCXZ
from .model import AbaqusRollerBCY
from .model import AbaqusRollerBCYZ
from .model import AbaqusRollerBCZ

# Abaqus Problems
from .problem import AbaqusProblem
# Abaqus Loads
from .problem import AbaqusAreaLoad
from .problem import AbaqusGravityLoad
from .problem import AbaqusHarmonicPointLoad
from .problem import AbaqusHarmonicPressureLoad
from .problem import AbaqusLineLoad
from .problem import AbaqusPointLoad
from .problem import AbaqusTributaryLoad


@plugin(category='fea_backends')
def register_backend():
    backend = compas_fea2.BACKENDS['abaqus']

    backend[Model] = AbaqusModel
    backend[Part] = AbaqusPart
    backend[Node] = AbaqusNode

    backend[BeamElement] = AbaqusBeamElement
    backend[MassElement] = AbaqusMassElement
    backend[MembraneElement] = AbaqusMembraneElement
    backend[ShellElement] = AbaqusShellElement
    backend[SolidElement] = AbaqusSolidElement
    backend[TrussElement] = AbaqusTrussElement

    backend[ElementsGroup] = AbaqusElementsGroup
    backend[NodesGroup] = AbaqusNodesGroup

    backend[AngleSection] = AbaqusAngleSection
    # backend[BeamSection] = AbaqusBeamSection
    backend[BoxSection] = AbaqusBoxSection
    backend[CircularSection] = AbaqusCircularSection
    backend[ISection] = AbaqusISection
    backend[MassSection] = AbaqusMassSection
    backend[MembraneSection] = AbaqusMembraneSection
    backend[PipeSection] = AbaqusPipeSection
    backend[RectangularSection] = AbaqusRectangularSection
    backend[ShellSection] = AbaqusShellSection
    backend[SolidSection] = AbaqusSolidSection
    backend[SpringSection] = AbaqusSpringSection
    backend[StrutSection] = AbaqusStrutSection
    backend[TieSection] = AbaqusTieSection
    backend[TrapezoidalSection] = AbaqusTrapezoidalSection
    backend[TrussSection] = AbaqusTrussSection

    backend[Concrete] = AbaqusConcrete
    backend[ConcreteDamagedPlasticity] = AbaqusConcreteDamagedPlasticity
    backend[ConcreteSmearedCrack] = AbaqusConcreteSmearedCrack
    backend[ElasticIsotropic] = AbaqusElasticIsotropic
    backend[ElasticOrthotropic] = AbaqusElasticOrthotropic
    backend[ElasticPlastic] = AbaqusElasticPlastic
    backend[Steel] = AbaqusSteel
    backend[Stiff] = AbaqusStiff

    backend[ContactHardFrictionPenalty] = AbaqusContactHardFrictionPenalty

    backend[Constraint] = AbaqusConstraint
    # backend[TieConstraint] = AbaqusTieConstraint

    backend[FixedBC] = AbaqusFixedBC
    backend[FixedBCXX] = AbaqusFixedBCXX
    backend[FixedBCYY] = AbaqusFixedBCYY
    backend[FixedBCZZ] = AbaqusFixedBCZZ
    backend[PinnedBC] = AbaqusPinnedBC
    backend[RollerBCX] = AbaqusRollerBCX
    backend[RollerBCXY] = AbaqusRollerBCXY
    backend[RollerBCXZ] = AbaqusRollerBCXZ
    backend[RollerBCY] = AbaqusRollerBCY
    backend[RollerBCYZ] = AbaqusRollerBCYZ
    backend[RollerBCZ] = AbaqusRollerBCZ

    backend[Problem] = AbaqusProblem

    backend[AcousticDiffuseFieldLoad] = AbaqusAcousticDiffuseFieldLoad
    backend[AreaLoad] = AbaqusAreaLoad
    backend[GravityLoad] = AbaqusGravityLoad
    backend[HarmonicPointLoad] = AbaqusHarmonicPointLoad
    backend[HarmonicPressureLoad] = AbaqusHarmonicPressureLoad
    backend[LineLoad] = AbaqusLineLoad
    backend[PointLoad] = AbaqusPointLoad
    backend[TributaryLoad] = AbaqusTributaryLoad

    backend[GeneralDisplacement] = AbaqusGeneralDisplacement

    print('Abaqus implementations registered...')
