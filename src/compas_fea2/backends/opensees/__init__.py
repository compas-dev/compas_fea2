"""
********************************************************************************
opensees
********************************************************************************

.. code-block:: python

    # example

.. automodule:: compas_fea2.backends.opensees.model

.. automodule:: compas_fea2.backends.opensees.problem

.. automodule:: compas_fea2.backends.opensees.job

"""

from .model import *
from .problem import *
from .job import *
# from .writer import *


__all__ = [name for name in dir() if not name.startswith('_')]

