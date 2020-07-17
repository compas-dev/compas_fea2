"""
********************************************************************************
abaqus
********************************************************************************

.. code-block:: python

    # example

.. automodule:: compas_fea2.backends.abaqus.model

.. automodule:: compas_fea2.backends.abaqus.problem

"""

from .model import *
from .problem import *

__all__ = [name for name in dir() if not name.startswith('_')]
