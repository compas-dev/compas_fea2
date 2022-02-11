"""
********************************************************************************
compas_fea2
********************************************************************************

.. currentmodule:: compas_fea2


API Packages
============

.. toctree::
    :maxdepth: 1

    compas_fea2.model
    compas_fea2.problem
    compas_fea2.results

Dev Packages
============

.. toctree::
    :maxdepth: 1

    compas_fea2.backends
    compas_fea2.interfaces
    compas_fea2.job
    compas_fea2.postprocessor
    compas_fea2.preprocessor
    compas_fea2.utilities

"""
import os
from collections import defaultdict
from compas.plugins import pluggable

from pint import UnitRegistry
units = UnitRegistry()
units.define('@alias pascal = Pa')


__author__ = ["Francesco Ranaudo"]
__copyright__ = "Block Research Group"
__license__ = "MIT License"
__email__ = "ranaudo@arch.ethz.ch"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
UMAT = os.path.abspath(os.path.join(DATA, "umat"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

BACKEND = None
BACKENDS = defaultdict(dict)


@pluggable(category='fea_backends', selector='collect_all')
def register_backend():
    raise NotImplementedError


def set_backend(name):
    global BACKEND
    BACKEND = name
    register_backend()


def get_backend_implementation(cls):
    return BACKENDS[BACKEND].get(cls)


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

__all_plugins__ = [
    'compas_fea2.backends.abaqus'
]
