"""
********************************************************************************
model
********************************************************************************

.. currentmodule:: compas_fea2.backends.abaqus.model

Model
=====

.. autosummary::
    :toctree: generated/

    AbaqusModel

Parts
=====

.. autosummary::
    :toctree: generated/

    AbaqusPart

Nodes
=====

.. autosummary::
    :toctree: generated/

    AbaqusNode

Elements
========

.. autosummary::
    :toctree: generated/

    AbaqusBeamElement
    AbaqusShellElement
    AbaqusSolidElement
    AbaqusTetrahedronElement
    AbaqusHexahedronElement

Constraints
===========

.. autosummary::
    :toctree: generated/

    AbaqusTieConstraint

Materials
=========

.. autosummary::
    :toctree: generated/

    AbaqusUserMaterial
    AbaqusStiff
    AbaqusElasticIsotropic
    AbaqusElasticOrthotropic
    AbaqusElasticPlastic
    AbaqusConcrete
    AbaqusConcreteSmearedCrack
    AbaqusConcreteDamagedPlasticity
    AbaqusSteel

Sections
========

.. autosummary::
    :toctree: generated/

    AbaqusBeamSection
    AbaqusSpringSection
    AbaqusAngleSection
    AbaqusBoxSection
    AbaqusCircularSection
    AbaqusHexSection
    AbaqusISection
    AbaqusPipeSection
    AbaqusRectangularSection
    AbaqusShellSection
    AbaqusMembraneSection
    AbaqusSolidSection
    AbaqusTrapezoidalSection
    AbaqusTrussSection
    AbaqusStrutSection
    AbaqusTieSection
    AbaqusMassSection

Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    AbaqusBoundaryCondition
    AbaqusFixedBC
    AbaqusPinnedBC
    AbaqusFixedBCXX
    AbaqusFixedBCYY
    AbaqusFixedBCZZ
    AbaqusRollerBCX
    AbaqusRollerBCY
    AbaqusRollerBCZ
    AbaqusRollerBCXY
    AbaqusRollerBCYZ
    AbaqusRollerBCXZ

Groups
======

.. autosummary::
    :toctree: generated/

    AbaqusNodesGroup
    AbaqusElementsGroup

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Abaqus Materials
from .materials import (
    AbaqusElasticIsotropic,
    AbaqusElasticOrthotropic,
    AbaqusElasticPlastic,
    AbaqusStiff,
    AbaqusUserMaterial,
    AbaqusConcrete,
    AbaqusConcreteDamagedPlasticity,
    AbaqusConcreteSmearedCrack,
    AbaqusSteel,
    AbaqusTimber,
)


# Abaqus Boundary Conditions
from .bcs import (
    AbaqusFixedBC,
    AbaqusFixedBCXX,
    AbaqusFixedBCYY,
    AbaqusFixedBCZZ,
    AbaqusPinnedBC,
    AbaqusRollerBCX,
    AbaqusRollerBCXY,
    AbaqusRollerBCXZ,
    AbaqusRollerBCY,
    AbaqusRollerBCYZ,
    AbaqusRollerBCZ,
)

# Abaqus Constraints
from .constraints import (
    AbaqusTieConstraint,
)

# Abaqus Elements
from .elements import (
    AbaqusMassElement,
    AbaqusBeamElement,
    AbaqusTrussElement,
    AbaqusMembraneElement,
    AbaqusShellElement,
    AbaqusSolidElement,
    AbaqusTetrahedronElement,
    AbaqusHexahedronElement,
)

# Abaqus Groups
from .groups import (
    AbaqusNodesGroup,
    AbaqusElementsGroup,
    AbaqusFacesGroup,
)


# Abaqus Interactions
from .interactions import (
    AbaqusHardContactFrictionPenalty,
    AbaqusHardContactRough,
)

# Abaqus Interfaces
from .interfaces import (
    AbaqusInterface
)

# Abaqus Models
from .model import AbaqusModel

# Abaqus Nodes
from .nodes import AbaqusNode

# Abaqus Parts
from .parts import AbaqusPart

# Abaqus Relseases
from .releases import (
    AbaqusBeamEndPinRelease
)

# Abaqus Sections
from .sections import (
    AbaqusBeamSection,
    AbaqusAngleSection,
    AbaqusBoxSection,
    AbaqusCircularSection,
    AbaqusHexSection,
    AbaqusISection,
    AbaqusMassSection,
    AbaqusPipeSection,
    AbaqusRectangularSection,
    AbaqusSpringSection,
    AbaqusStrutSection,
    AbaqusTieSection,
    AbaqusTrapezoidalSection,
    AbaqusTrussSection,
    AbaqusMembraneSection,
    AbaqusShellSection,
    AbaqusSolidSection,
)

__all__ = [
    'AbaqusElasticIsotropic',
    'AbaqusElasticOrthotropic',
    'AbaqusElasticPlastic',
    'AbaqusStiff',
    'AbaqusUserMaterial',
    'AbaqusConcrete',
    'AbaqusConcreteDamagedPlasticity',
    'AbaqusConcreteSmearedCrack',
    'AbaqusSteel',
    'AbaqusTimber',

    'AbaqusFixedBC',
    'AbaqusFixedBCXX',
    'AbaqusFixedBCYY',
    'AbaqusFixedBCZZ',
    'AbaqusPinnedBC',
    'AbaqusRollerBCX',
    'AbaqusRollerBCXY',
    'AbaqusRollerBCXZ',
    'AbaqusRollerBCY',
    'AbaqusRollerBCYZ',
    'AbaqusRollerBCZ',

    'AbaqusTieConstraint',

    'AbaqusBeamSection',
    'AbaqusAngleSection',
    'AbaqusBoxSection',
    'AbaqusCircularSection',
    'AbaqusHexSection',
    'AbaqusISection',
    'AbaqusMassSection',
    'AbaqusPipeSection',
    'AbaqusRectangularSection',
    'AbaqusSpringSection',
    'AbaqusStrutSection',
    'AbaqusTieSection',
    'AbaqusTrapezoidalSection',
    'AbaqusTrussSection',
    'AbaqusMembraneSection',
    'AbaqusShellSection',
    'AbaqusSolidSection',

    'AbaqusMassElement',
    'AbaqusBeamElement',
    'AbaqusTrussElement',
    'AbaqusMembraneElement',
    'AbaqusShellElement',
    'AbaqusSolidElement',
    'AbaqusTetrahedronElement',
    'AbaqusHexahedronElement',

    'AbaqusNodesGroup',
    'AbaqusElementsGroup',
    'AbaqusFacesGroup',

    'AbaqusHardContactFrictionPenalty',
    'AbaqusHardContactRough',

    'AbaqusInterface',

    'AbaqusBeamEndPinRelease',

    'AbaqusPart',

    'AbaqusNode',

    'AbaqusModel',
]
