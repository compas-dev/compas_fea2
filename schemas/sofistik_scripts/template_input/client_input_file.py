from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from model import *
from input_file import *


def build_model():
    # ----- Model setup -----
    m = Model("Bathe Beam I")

    # ----- Material -----
    m.materials += Material(10, elasticity_modulus=2E8, shear_ratio=0.3, name="Test Material")
    m.sections += RectangularSection(10, height=1000, width=100, material_nr=10, name="Test Section")

    # ----- Geometry -----
    m.nodes += [ Node(1, 0.0, 0.0, 0.0),
                 Node(2, 0.0, 20.0, 0.0) ]
    m.beams += Beam(10, 1, 2, section_nr=10, division=6)
    
    # ----- Boundary Conditions -----
    m.boundary_conditions += BoundaryCondition(1, tx=True, ty=True, tz=True, rx=True, ry=True, rz=True)

    # ----- Loading ----- 
    test_load_z = [NodeLoad(2, pz=-0.1)]
    test_load_x = [NodeLoad(2, px=0.1)]
    m.load_cases += LoadCase(10, test_load_z, name="Test Case Z")
    m.load_cases += LoadCase(20, test_load_x, name="Test Case X")
    m.load_combinations += LoadCombination(100, [m.load_cases[10]], [1.0], 0.0)
    m.load_combinations += LoadCombination(200, [lc for lc in m.load_cases], [1.0, 0.1], 0.0)

    # ----- Analyses -----
    m.analyses += Analysis(1000, m.load_combinations[100], analysis_type=0, name="Test Case Z Linear Analysis")
    m.analyses += Analysis(1001, m.load_combinations[100], analysis_type=1, name="Test Case Z Non-Linear Analysis")
    m.analyses += Analysis(2000, m.load_combinations[200], analysis_type=0, name="Test Case XZ Linear Analysis")
    m.analyses += Analysis(2001, m.load_combinations[200], analysis_type=0, name="Test Case XZ Non-Linear Analysis")

    # ----- Post-pro -----
    m.stresses += StressInterpolation(10, [al for al in m.analyses])
    
    return m



if __name__ == "__main__":
    PATH = desktop = os.path.expanduser("~/Desktop")
    model = build_model()
    parsed_file = InputFile(model)
    parsed_file.write_to_file(PATH)