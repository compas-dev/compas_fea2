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

def init_fea2(verbose=False, point_overlap=True, global_tolerance=1, precision='3f'):
    """Create a default environment file if it doesn't exist and loads its
    variables.

    Parameters
    ----------
    verbose : bool, optional
        Be verbose when printing output, by default False
    point_overlap : bool, optional
        Allow two nodes to be at the same location, by default True
    global_tolerance : int, optional
        Tolerance for the model, by default 1
    precision : str, optional
        Values approximation, by default '3f'
    """
    with open(os.path.abspath(os.path.join(HERE, ".env")), "x") as f:
        f.write('\n'.join([
            "VERBOSE={}".format(verbose),
            "POINT_OVERLAP={}".format(point_overlap),
            "GLOBAL_TOLERANCE={}".format(point_overlap),
            "PRECISION={}".format(precision)
            ]))
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
    except ImportError:
        print('backend plugin not found. Make sure that you have installed it before.')

def _get_backend_implementation(cls):
    return BACKENDS[BACKEND].get(cls)


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

