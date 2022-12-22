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
    compas_fea2.job
    compas_fea2.postprocess
    compas_fea2.utilities

Dev Packages
============

.. toctree::
    :maxdepth: 1

    compas_fea2.UI

"""
import os
import json
from collections import defaultdict
from compas.plugins import pluggable


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

with open(os.path.join(HERE, 'settings.json'), 'r') as f:
    SETTINGS = json.load(f)

PRECISION = SETTINGS["PRECISION"]

def set_precision(precision):
    global PRECISION
    PRECISION = precision

VERBOSE = SETTINGS["VERBOSE"]
POINT_OVERLAP = SETTINGS["POINT_OVERLAP"]
GLOBAL_TOLERANCE = SETTINGS["GLOBAL_TOLERANCE"]

BACKEND = None
BACKENDS = defaultdict(dict)


@pluggable(category='fea_backends', selector='collect_all')
def register_backend():
    raise NotImplementedError


def set_backend(name):
    if name not in ('abaqus', 'opensees', 'ansys', 'sofistik'):
        raise ValueError('{} is not a backend!'.format(name))
    global BACKEND
    BACKEND = name
    register_backend()


def get_backend_implementation(cls):
    return BACKENDS[BACKEND].get(cls)


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

__all_plugins__ = [
    'compas_fea2_abaqus',
    'compas_fea2_ansys',
    'compas_fea2_opensees',
    'compas_fea2_sofistik',
]
