"""
********************************************************************************
opensees
********************************************************************************

.. code-block:: python

    # example

.. automodule:: compas_fea2.backends.opensees.components

.. automodule:: compas_fea2.backends.opensees.job

.. automodule:: compas_fea2.backends.opensees.writer

"""

from .components import *
from .job import *
from .writer import *


__all__ = [name for name in dir() if not name.startswith('_')]

