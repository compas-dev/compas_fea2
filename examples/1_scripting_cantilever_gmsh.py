import os
from pathlib import Path
from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import NodesGroup

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FixedBC
from compas_fea2.backends.abaqus import RollerBCXZ
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep
from compas_fea2.backends.abaqus import Results

from compas_fea2.postprocessor.stresses import principal_stresses

from compas_fea2 import DATA
from compas_fea2 import TEMP

import gmsh
import sys
from math import degrees, atan2
from compas.datastructures import Mesh
from compas.geometry import centroid_points
import matplotlib.pyplot as plt


def gmsh_geometry(x, y, lc, path):
    gmsh.initialize(sys.argv)
    gmsh.model.add("t1")

    gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
    gmsh.model.geo.addPoint(x, 0, 0, lc, 2)
    gmsh.model.geo.addPoint(x, y, 0, lc, 3)
    p4 = gmsh.model.geo.addPoint(0, y, 0, lc)
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(3, 2, 2)
    gmsh.model.geo.addLine(3, p4, 3)
    gmsh.model.geo.addLine(4, 1, p4)
    gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)

    gmsh.model.geo.synchronize()
    gmsh.model.addPhysicalGroup(1, [1, 2, 4], 5)
    ps = gmsh.model.addPhysicalGroup(2, [1])
    gmsh.model.setPhysicalName(2, ps, "My surface")

    # We can then generate a 2D mesh...
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

    centroids = [centroid_points([problem.model.parts['cantilever'].nodes[i].xyz for i in element.connectivity])
                 for element in problem.model.parts['cantilever'].elements.values()]
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
mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)

# Define sections
shell_20 = ShellSection(name='section_A', material=mat, t=20)

# Create a shell model from a mesh
part = Part.from_gmsh(name='cantilever', gmshModel=mesh, section=shell_20)
model.add_part(part)

# Find nodes in the model for the boundary conditions
n_fixed = model.get_node_from_coordinates([0, 0, 0, ], 10)
n_roller = model.get_node_from_coordinates([lx, 0, 0], 10)
n_load = model.get_node_from_coordinates([lx, ly, 0, ], 10)

# Define sets for boundary conditions and loads
model.add_nodes_group(name='fixed', nodes=[n_fixed['cantilever']], part='cantilever')
model.add_nodes_group(name='roller', nodes=[n_roller['cantilever']], part='cantilever')
model.add_nodes_group(name='pload', nodes=[n_load['cantilever']], part='cantilever')

# Assign boundary conditions to the node stes
model.add_rollerXZ_bc('bc_roller', nodes=[n_roller['cantilever']], part='cantilever')
model.add_fix_bc(name='bc_fix', nodes=[n_fixed['cantilever']], part='cantilever')
model.summary()
model.show(node_labels={'cantilever': [0, 1]})

##### ----------------------------- PROBLEM ----------------------------- #####
folder = 'C:/temp/'
name = 'principal_stresses'

# Create the Problem object
problem = Problem(name='cantilever_gmsh', model=model)

# Define the analysis step
problem.add_step(GeneralStaticStep(name='gstep'))

# Assign a point load to the node set
problem.add_point_load(name='pload', step='gstep', nodes=[n_load['cantilever']], part='cantilever', x=1000)

# Define the field outputs required
problem.add_field_output(name='fout', node_outputs=None, element_outputs=['s'], step='gstep')


problem.summary()
# problem.show()
# # Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))
# # print(os.path.join(problem.path, '{}-results.pkl'.format(problem.name)))

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
