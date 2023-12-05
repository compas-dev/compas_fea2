"""
********************************************************************************
Units
********************************************************************************

compas_fe2 can use Pint for units consistency.

"""

import os
from pint import UnitRegistry
HERE = os.path.dirname(__file__)

# U.define('@alias pascal = Pa')

def units(system='SI'):
    return UnitRegistry(os.path.join(HERE, 'fea2_en.txt'), system=system)
