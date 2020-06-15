"""
********************************************************************************
abaqus
********************************************************************************

.. code-block:: python

    # example

.. automodule:: compas_fea2.backends.abaqus.components

.. automodule:: compas_fea2.backends.abaqus.job

.. automodule:: compas_fea2.backends.abaqus.writer

"""

from .components import *
from .job import *
from .writer import *
from .structure import *

__all__ = [name for name in dir() if not name.startswith('_')]
