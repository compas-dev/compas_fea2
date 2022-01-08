from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import SolidSection
from compas_fea2.backends.abaqus import NodeTieConstraint
from compas_fea2.backends.abaqus.model.elements import SolidElement

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep
from compas_fea2.backends.abaqus import GeneralDisplacement

from compas_fea2.backends.abaqus import Results

from pathlib import Path
from compas_fea2 import TEMP

import numpy as np
import scipy.interpolate


def define_arch(n=5):
    cp_out = np.array([[0, 0], [2.5, 3.5], [5, 5], [7.5, 3.5], [10, 0]])
    cp_in = np.array([[0.5, 0], [2.2, 2.5], [5, 4.5], [7.8, 2.5], [9.5, 0]])
    cps = [cp_out, cp_in]

    curves = []
    for ly in [0, 1]:
        for cp in cps:
            curve = scipy.interpolate.interp1d(cp[:, 0], cp[:, 1], kind='quadratic')
            x = np.linspace(np.min(cp[:, 0]), np.max(cp[:, 0]), n)
            y = np.ones_like(x)*ly
            z = curve(x)
            curves.append(np.vstack([x, y, z]).T)

    return curves


##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model')
# Define materials
mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)
# Define sections
sec = SolidSection(name='sec_A', material=mat)

lx, ly, lz = 0.5, 0.3, 0.25
# for n in range(5):
#     brick = Part(name=f'brick-{n}')
#     brick.add_nodes([Node([0., 0., n*lz]),
#                      Node([0., ly, n*lz]),
#                      Node([lx, ly, n*lz]),
#                      Node([lx, 0., n*lz]),
#                      Node([0., 0., (n+1)*lz]),
#                      Node([0., ly, (n+1)*lz]),
#                      Node([lx, ly, (n+1)*lz]),
#                      Node([lx, 0., (n+1)*lz])])
#     brick.add_element(SolidElement([0, 1, 2, 3, 4, 5, 6, 7], sec))
#     # Add a Part to the model
#     model.add_part(brick)

curves = define_arch(n=10)
for i in range(len(curves[0])-1):
    brick = Part(name=f'brick-{i}')
    brick.add_nodes([Node(curves[0][i]),
                     Node(curves[1][i]),
                     Node(curves[3][i]),
                     Node(curves[2][i]),
                     Node(curves[0][i+1]),
                     Node(curves[1][i+1]),
                     Node(curves[3][i+1]),
                     Node(curves[2][i+1])
                     ])
    brick.add_element(SolidElement([0, 1, 2, 3, 4, 5, 6, 7], sec))
    # Add a Part to the model
    model.add_part(brick)

# Assign boundary conditions
model.add_bc_type(name='bc_pinned', bc_type='fix', part='brick-0', nodes=[0, 1, 2, 3])
constraint = NodeTieConstraint(name='tie', master='block-0-1.4', slave='block-1-1.0')
model.add_constraint(constraint)
# Review
# model.summary()
# model.show(scale_factor=0.1)


##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='test_tce', model=model)

# # Approach 1: Create a step and assign a gravity load
# step_0 = GeneralStaticStep(name='step_pload_0')
# step_0.add_gravity_load()
# problem.add_step(step_0)

# Approach 2: Add a step and define a point load directly from Problem
problem.add_step(GeneralStaticStep(name='step_pload_1'))
problem.add_point_load(name='load_point', x=200, y=100, z=-1000, nodes=[3], part='brick-2', step='step_pload_1')

# Define the field outputs required
fout = FieldOutput(name='fout')
problem.add_output(fout, 'step_pload_1')

# Review
problem.summary()
problem.show(scale_factor=0.1)

# Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))
