from pathlib import Path
from pprint import pprint

from compas.datastructures import Mesh

from compas_fea2.backends.abaqus.model import Model
from compas_fea2.backends.abaqus.model import ElasticIsotropic
from compas_fea2.backends.abaqus.model import BoxSection
from compas_fea2.backends.abaqus.model import NodesGroup

from compas_fea2.backends.abaqus.problem import Problem
from compas_fea2.backends.abaqus.problem import FieldOutput
from compas_fea2.backends.abaqus.problem import GeneralStaticStep
from compas_fea2.backends.abaqus import Results

from compas_fea2 import DATA
from compas_fea2 import TEMP

# Get a Mesh geometry to create the model
mesh = Mesh.from_obj(DATA + '/hypar.obj')

##### ------------------------------ MODEL ------------------------------ #####
# Initialise the assembly object
model = Model(name='hypar')

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))

# Define sections
box_20_80 = BoxSection(name='section_A', material='mat_A', a=20, b=80, t=5)

# Create a frame model from a mesh
model.frame_from_mesh(mesh=mesh, beam_section=box_20_80)

# Find nodes in the model for the boundary conditions
n_fixed = model.get_node_from_coordinates([5000, 0, 0, ], 10)
n_roller = model.get_node_from_coordinates([0, 0, -5000], 10)
n_load = model.get_node_from_coordinates([0, 3000, 0, ], 10)

# Define sets for boundary conditions and loads
# model.add_instance_set(NodesGroup(name='fixed', selection=[n_fixed['part-1']], stype='nset'), instance='part-1-1')
# model.add_instance_set(NodesGroup(name='roller', selection=[n_roller['part-1']], stype='nset'), instance='part-1-1')
# model.add_instance_set(NodesGroup(name='pload', selection=[n_load['part-1']], stype='nset'), instance='part-1-1')

# Assign boundary conditions to the node stes
model.add_rollerXZ_bc(name='bc_roller', part='part-1', nodes=[n_roller['part-1']])
model.add_fix_bc(name='bc_fix', part='part-1', nodes=[n_fixed['part-1']])

# model.show()

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='hypar', model=model)

# Define the analysis step
problem.add_step(GeneralStaticStep(name='gstep'))

# Assign a point load to the node set
problem.add_point_load(name='pload', step='gstep', part='part-1', nodes=[n_load['part-1']], y=-1000)

# Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))

##### --------------------- POSTPROCESS RESULTS -------------------------- #####
results = Results.from_problem(problem, fields=['u'])
pprint(results.nodal)
