"""
********************************************************************************
Core
********************************************************************************

.. currentmodule:: compas_fea2.backends._core


Analysis Components
===================


Analysis Job
============


Analysis Writer
===============


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .components import *
from .job import *
from .writer import *


__all__ = [name for name in dir() if not name.startswith('_')]
