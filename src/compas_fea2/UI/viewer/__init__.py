"""
********************************************************************************
Viewer
********************************************************************************

.. currentmodule:: compas_fea2.UI.viewer

.. autosummary::
    :toctree: generated/

    FEA2Viewer

"""

from .viewer import FEA2Viewer
from .shapes import (
    _BCShape,
    FixBCShape,
    PinBCShape,
)

__all__ = [
    "FEA2Viewer",
    "BCShape",
    "FixBCShape",
    "PinBCShape",
]
