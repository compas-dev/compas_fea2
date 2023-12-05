"""
********************************************************************************
Materials
********************************************************************************

.. currentmodule:: compas_fea2.model.materials

General Materials
=================

.. autosummry::
    :toctree: generated/

    _Material
    ElasticIsotropic
    ElasticOrthotropic
    ElasticPlastic
    Stiff
    UserMaterial

Concrete
========

.. autosummary::
    :toctree: generated/

    Concrete
    ConcreteDamagedPlasticity
    ConcreteSmearedCrack

Steel
=====

.. autosummary::
    :toctree: generated/

    Steel

Timber
======

.. autosummary::
    :toctree: generated/

    Timber

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Concrete
from .concrete import Concrete  # noqa : F401
from .concrete import ConcreteDamagedPlasticity  # noqa : F401
from .concrete import ConcreteSmearedCrack  # noqa : F401

# Basic Materials
from .material import _Material  # noqa : F401
from .material import ElasticIsotropic  # noqa : F401
from .material import ElasticOrthotropic  # noqa : F401
from .material import ElasticPlastic  # noqa : F401
from .material import Stiff  # noqa : F401
from .material import UserMaterial  # noqa : F401

# Steel
from .steel import Steel  # noqa : F401

# Timber
from .timber import Timber
