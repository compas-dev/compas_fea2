"""
********************************************************************************
compas_fea2
********************************************************************************

.. currentmodule:: compas_fea2


.. toctree::
    :maxdepth: 1

    compas_fea2.backends
    compas_fea2.cad
    compas_fea2.postprocess
    compas_fea2.preprocess
    compas_fea2.utilities


"""

from __future__ import print_function

import os
import sys
import compas


__author__ = ["Francesco Ranaudo"]
__copyright__ = "Block Research Group"
__license__ = "MIT License"
__email__ = "ranaudo@arch.ethz.ch"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# Check if package is installed from git
# If that's the case, try to append the current head's hash to __version__
try:
    git_head_file = compas._os.absjoin(HOME, '.git', 'HEAD')

    if os.path.exists(git_head_file):
        # git head file contains one line that looks like this:
        # ref: refs/heads/master
        with open(git_head_file, 'r') as git_head:
            _, ref_path = git_head.read().strip().split(' ')
            ref_path = ref_path.split('/')

            git_head_refs_file = compas._os.absjoin(HOME, '.git', *ref_path)

        if os.path.exists(git_head_refs_file):
            with open(git_head_refs_file, 'r') as git_head_ref:
                git_commit = git_head_ref.read().strip()
                __version__ += '-' + git_commit[:8]
except Exception:
    pass

__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
