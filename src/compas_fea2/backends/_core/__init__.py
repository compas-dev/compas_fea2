"""
********************************************************************************
_core
********************************************************************************

.. code-block:: python

    # example

.. automodule:: compas_fea2.backends._core.components

.. automodule:: compas_fea2.backends._core.job

.. automodule:: compas_fea2.backends._core.writer


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .components import *
from .job import *
from .writer import *
from .structure import *


__all__ = [name for name in dir() if not name.startswith('_')]
