import matplotlib.pyplot as plt
from compas.geometry import centroid_points
from math import degrees, atan2
import sys
import gmsh
from compas_fea2 import TEMP
from compas_fea2 import DATA
import os
from pathlib import Path
from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import ShellSection

from compas_fea2.problem import Problem
from compas_fea2.problem import StaticStep

from compas_fea2.results import Results

from compas_fea2.postprocessor.stresses import principal_stresses

import compas_fea2
compas_fea2.set_backend('abaqus')


# NOTE: This example is in SI-mm (mm, tonne, s)


def gmsh_geometry(x, y, lc, path):
    gmsh.initialize(sys.argv)
    gmsh.model.add("t1")

    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(x, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(x, y, 0, lc)
    p4 = gmsh.model.geo.addPoint(0, y, 0, lc)
    l1 = gmsh.model.geo.addLine(p1, p2, 1)
    l2 = gmsh.model.geo.addLine(p3, p2, 2)
    l3 = gmsh.model.geo.addLine(p3, p4, 3)
    l4 = gmsh.model.geo.addLine(p4, p1, 4)
    cl1 = gmsh.model.geo.addCurveLoop([l4, l1, -l2, l3])
    s1 = gmsh.model.geo.addPlaneSurface([cl1])

    gmsh.model.geo.synchronize()
    pgroup = gmsh.model.addPhysicalGroup(1, [p1, p2, p4])
    sgroup = gmsh.model.addPhysicalGroup(2, [s1])
    gmsh.model.setPhysicalName(2, sgroup, "My surface")

    gmsh.model.mesh.generate(2)
    return gmsh.model
    # print(gmsh.model.mesh.getNode(nodeTag=10))
    # element = gmsh.model.mesh.getElement(10)
    # gmsh.model.mesh.getElementFaceNodes()
    # print(gmsh.model.mesh.getKeysForElement(1,'Lagrange'))

    # # ... and save it to disk
    # gmsh.write(path)
    # gmsh.finalize()


def plot_vectors(problem, spr, e, scale):
    for part in problem.model.parts:
        centroids = [centroid_points([node.xyz for node in element.nodes])
                     for element in part.elements]
    x = [c[0] for c in centroids]
    y = [c[1] for c in centroids]

    for stype in ['max', 'min']:
        color = 'r' if stype == 'max' else 'b'
        u = e[sp][stype][0]*spr['sp1'][stype]/2
        v = e[sp][stype][1]*spr['sp1'][stype]/2
        plt.quiver(x, y, u, v, color=color, width=1*10**-3)
        plt.quiver(x, y, -u, -v, color=color, width=1*10**-3)
    plt.axis('equal')
    plt.show()


# Generate a cantilever beam using gmsh
lx = 1000
ly = 3000
mesh = gmsh_geometry(lx, ly, 100, DATA+"/t1.stl")
# mesh = Mesh.from_stl(DATA+"/t1.stl")

##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='cantilever_gmsh')

# Define materials
mat = ElasticIsotropic(name='steel', E=29000, v=0.17, density=2.5e-9)

# Define sections
shell_20 = ShellSection(name='shell_20mm', material=mat, t=20)

# Create a Part made of shell elements from a gmsh model
part = Part.from_gmsh(name='cantilever', gmshModel=mesh, section=shell_20)
model.add_part(part)

# Find nodes in the part for the boundary conditions
n_fixed = part.find_nodes_by_location([0, 0, 0, ], 10)
n_roller = part.find_nodes_by_location([lx, 0, 0], 10)
n_load = part.find_nodes_by_location([lx, ly, 0, ], 10)

# Define sets for boundary conditions and loads
# model.add_groups(groups=[n_fixed, n_roller, n_load], part='cantilever')

# Assign boundary conditions to the node stes
for node in n_roller:
    model.add_rollerXZ_bc(node=node)
for node in n_fixed:
    model.add_fix_bc(node=node)

# # # Review
# # model.summary()
# # model.show(node_labels={'cantilever': [0, 1]})

# ##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='principal_stresses', model=model)

# Define the analysis step
step = problem.add_step(StaticStep(name='gstep'))

# Assign a point load to the node set
step.add_point_load(node=n_load[0], x=1000)

# # Define the field outputs required
# problem.add_field_output(name='fout', node_outputs=None, element_outputs=['s'], step='gstep')


# problem.summary()
# problem.show()
# Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))
# print(os.path.join(problem.path, '{}-results.pkl'.format(problem.name)))

##### --------------------- POSTPROCESS RESULTS -------------------------- #####
results = Results.from_problem(problem, fields=['s'], output=True)
spr, e = principal_stresses(results.element['gstep'])

sp = 'sp5'
stype = 'max'

# check the results for an element
id = 0
print(f'the {stype} principal stress for element {id} is: ', spr[sp][stype][id])
print('principal axes (basis):\n', e[sp][stype][:, id])
print('and its inclination w.r.t. World is: ', degrees(atan2(*e[sp][stype][:, id][::-1])))

plot_vectors(problem, spr, e, 10)
