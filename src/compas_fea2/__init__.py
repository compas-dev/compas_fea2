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

import os
from dotenv import load_dotenv

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

def init_fea2():
    """Create a default environment file.
    """
    import shutil
    shutil.copyfile(os.path.abspath(os.path.join(DATA, "__templates", ".env")),
                    os.path.abspath(os.path.join(HERE, ".env")))
    load_dotenv()

if not load_dotenv():
    init_fea2()

VERBOSE = os.getenv('VERBOSE').lower() == 'true'
POINT_OVERLAP = os.getenv('POINT_OVERLAP').lower() == 'true'
GLOBAL_TOLERANCE = os.getenv('GLOBAL_TOLERANCE')
PRECISION = os.getenv('PRECISION')
BACKEND = None
BACKENDS = defaultdict(dict)

def set_precision(precision):
    global PRECISION
    PRECISION = precision

# pluggable function to be
def _register_backend():
    """Create the class registry for the plugin.

    Raises
    ------
    NotImplementedError
        This function is implemented within the backend plugin implementation.
    """
    raise NotImplementedError

def set_backend(plugin):
    """Set the backend plugin to be used.

    Parameters
    ----------
    plugin : str
        Name of the plugin library. You can find some backend plugins on the
        official ``compas_fea2`` website.

    Raises
    ------
    ImportError
        If the plugin library is not found.
    """
    import importlib
    global BACKEND
    BACKEND = plugin
    try:
        importlib.import_module(plugin)._register_backend()
    except:
        raise ImportError('backend plugin not found. Make sure that you have installed it before.')

def _get_backend_implementation(cls):
    return BACKENDS[BACKEND].get(cls)


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

