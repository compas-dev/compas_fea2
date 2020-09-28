"""
********************************************************************************
PreProcess
********************************************************************************

.. currentmodule:: compas_fea2.preprocess


Meshing
=======

.. autosummary::
    :toctree: generated/

    discretise_faces
    extrude_mesh
    tets_from_vertices_faces


Discretization
==============

.. autosummary::
    :toctree: generated/

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .meshing import *
from .discretize import *

__all__ = [name for name in dir() if not name.startswith('_')]
