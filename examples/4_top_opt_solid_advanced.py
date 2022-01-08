import sys
from pathlib import Path
from math import radians
from pprint import pprint

import meshio


import numpy as np
import gmsh
import warnings

from compas.geometry import Frame, Point, Vector, Plane, Circle
from compas.geometry import Box, Cylinder
from compas.geometry import Translation, Rotation
from compas.geometry import midpoint_point_point
from compas.datastructures import Mesh

from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import SolidSection
from compas_fea2.backends.abaqus import SolidElement
from compas_fea2.backends.abaqus import NodesGroup

from compas_fea2.backends.abaqus.problem import Problem
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep
from compas_fea2.backends.abaqus import Results

from compas_fea2.interfaces.viewer import OptiViewer

from compas_fea2 import DATA
from compas_fea2 import TEMP


warnings.filterwarnings("ignore")
gmsh.initialize()
gmsh.model.add("plate")

# Outer geometry of the plate
L, B, H, r = 2.50, 0.10, 0.50, 0.05
channel = gmsh.model.occ.addBox(0, 0, 0, L, B, H)

# Holes geoemtry
cylinder_1 = gmsh.model.occ.addCylinder(0.50, 0, 0.25, 0, B, 0, r)
cylinder_2 = gmsh.model.occ.addCylinder(L-0.50, 0, 0.25, 0, B, 0, r)

# Create the holes
plate = gmsh.model.occ.cut([(3, channel)], [(3, cylinder_1), (3, cylinder_2)])

# The next step is to tag physical entities, such as the plate volume, and inlets,
# outlets, channel walls and obstacle walls.
# We start by finding the volumes, which after the `cut`-operation is only the
# plate volume. We could have kept the other volumes by supply keyword arguments
# to the `cut`operation. See the [GMSH Python API](https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/api/gmsh.py#L5143) for more information.


# Syncronize the CAD module before tagging entities.
gmsh.model.occ.synchronize()

# Get the volumes
volumes = gmsh.model.getEntities(dim=3)
# assert(volumes == fluid[0])
plate_marker = 11
gmsh.model.addPhysicalGroup(volumes[0][0], [volumes[0][1]], plate_marker)
gmsh.model.setPhysicalName(volumes[0][0], plate_marker, "plate volume")


# For the surfaces, we start by finding all surfaces, and then compute the
# geometrical center such that we can indentify which are inlets, outlets, walls
# and the obstacle. As the walls will consist of multiple surfaces, and the
# obstacle is circular, we need to find all entites before addin the physical group.

# Get the surfaces
surfaces = gmsh.model.occ.getEntities(dim=2)
inlet_marker, outlet_marker, wall_marker, obstacle_marker = 1, 3, 5, 7
walls = []
obstacles = []
for surface in surfaces:
    com = gmsh.model.occ.getCenterOfMass(surface[0], surface[1])
    if np.allclose(com, [0, B/2, H/2]):
        gmsh.model.addPhysicalGroup(surface[0], [surface[1]], inlet_marker)
        inlet = surface[1]
        gmsh.model.setPhysicalName(surface[0], inlet_marker, "Fluid inlet")
    elif np.allclose(com, [L, B/2, H/2]):
        gmsh.model.addPhysicalGroup(surface[0], [surface[1]], outlet_marker)
        gmsh.model.setPhysicalName(surface[0], outlet_marker, "Fluid outlet")
    elif np.isclose(com[2], 0) or np.isclose(com[1], B) or np.isclose(com[2], H) or np.isclose(com[1], 0):
        walls.append(surface[1])
    else:
        obstacles.append(surface[1])
gmsh.model.addPhysicalGroup(2, walls, wall_marker)
gmsh.model.setPhysicalName(2, wall_marker, "Walls")
gmsh.model.addPhysicalGroup(2, obstacles, obstacle_marker)
gmsh.model.setPhysicalName(2, obstacle_marker, "Obstacle")


# The final step is to set mesh resolutions. We will use `GMSH Fields` to do this.
# One can alternatively set mesh resolutions at points with the command
# `gmsh.model.occ.mesh.setSize`. We start by specifying a distance field from the obstacle surface


gmsh.model.mesh.field.add("Distance", 1)
gmsh.model.mesh.field.setNumbers(1, "FacesList", obstacles)

# Set mesh resolution
resolution = r/5
gmsh.model.mesh.field.add("Threshold", 2)
gmsh.model.mesh.field.setNumber(2, "IField", 1)
gmsh.model.mesh.field.setNumber(2, "LcMin", resolution)
gmsh.model.mesh.field.setNumber(2, "LcMax", 20*resolution)
gmsh.model.mesh.field.setNumber(2, "DistMin", 0.5*r)
gmsh.model.mesh.field.setNumber(2, "DistMax", r)


# We add a similar threshold at the inlet to ensure fully resolved inlet flow
gmsh.model.mesh.field.add("Distance", 3)
gmsh.model.mesh.field.setNumbers(3, "FacesList", [inlet])
gmsh.model.mesh.field.add("Threshold", 4)
gmsh.model.mesh.field.setNumber(4, "IField", 3)
gmsh.model.mesh.field.setNumber(4, "LcMin", 5*resolution)
gmsh.model.mesh.field.setNumber(4, "LcMax", 10*resolution)
gmsh.model.mesh.field.setNumber(4, "DistMin", 0.1)
gmsh.model.mesh.field.setNumber(4, "DistMax", 0.5)


# We combine these fields by using the minimum field
gmsh.model.mesh.field.add("Min", 5)
gmsh.model.mesh.field.setNumbers(5, "FieldsList", [2, 4])
gmsh.model.mesh.field.setAsBackgroundMesh(5)


# Before meshing the model, we need to use the syncronize command
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)


# ------------------------------- COMPAS_FEA2 ---------------------------------#
# Define materials
mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)

# Define sections
sec = SolidSection(name='section_A', material=mat)

part = Part.from_gmsh('rod', gmsh.model, sec, verbose=False)
# del model

model = Model('solid_rod')
model.add_part(part)

# Define sets for boundary conditions and loads
# model.add_instance_set(NodesGroup(name='fixed', selection=[n_fixed['part-1']], stype='nset'), instance='part-1-1')
# model.add_instance_set(NodesGroup(name='roller', selection=[n_roller['part-1']], stype='nset'), instance='part-1-1')
# model.add_instance_set(NodesGroup(name='pload', selection=[n_load['part-1']], stype='nset'), instance='part-1-1')

# Assign boundary conditions to the node stes
# model.add_rollerXZ_bc(name='bc_roller', part='rod', nodes=[300, 301, 302])
model.add_fix_bc(name='bc_fix', part='rod', nodes=[0, 1, 2, 3])

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='solid', model=model)

# Define the analysis step
problem.add_step(GeneralStaticStep(name='gstep'))

# Assign a point load to the node set
n_load = model.get_node_from_coordinates([L/2, 0, 0, ], 0.1)
problem.add_point_load(name='pload', step='gstep', part='rod', nodes=[n_load['rod']], z=-1000)

# Review
problem.summary()
problem.show(width=1600, height=900, scale_factor=0.02)

# Define the optimisation parameters
problem.set_optimisation_parameters(0.2, 40, 10)

# Solve the problem
problem.optimise()

# Visualie results
v = OptiViewer(problem)
v.show()
