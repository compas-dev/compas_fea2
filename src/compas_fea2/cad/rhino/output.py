from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from compas_rhino.geometry import RhinoMesh
except:
    pass

from compas.datastructures.mesh import Mesh
from compas.datastructures import Network
from compas.geometry import add_vectors
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.rpc import Proxy

from compas_fea2 import utilities
from compas_fea2.utilities import colorbar
from compas_fea2.preprocess import extrude_mesh
from compas_fea2.utilities import network_order

from compas_fea2._core import CoreStructure


try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass

# try:
#     import rhinoscriptsyntax as rs
# except ImportError:
#     import platform
#     if platform.system() == 'Windows':
#         raise

import json

functions = Proxy('compas_fea.utilities.functions')
meshing   = Proxy('compas_fea.preprocess.meshing')


# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)
