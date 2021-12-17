from compas_fea2.preprocessor.meshing import compas_to_gmsh

from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part

from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import ShellSection

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep

from compas_fea2.backends.abaqus import Results

from compas_fea2 import DATA
from compas_fea2 import TEMP


from compas.datastructures import Mesh

##### -------------------------- PREPROCESSING --------------------------- #####
# Get a Mesh geometry to create the model
mesh = Mesh.from_obj(DATA + '/hypar.obj')
# Mesh the geometry in gmesh
gmesh = compas_to_gmsh(mesh, lc=100, inspect=True)

##### ------------------------------- MODEL ------------------------------ #####
# Initialise the assembly object
model = Model(name='hypar_gmsh')

# Define materials
mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)
sec = ShellSection(name='section_A', material=mat, t=20)
# Create a shell model from a mesh
part = Part.shell_from_gmesh(name='hypar_part', gmshModel=gmesh, shell_section=sec)


model.add_part(part)
# Find nodes in the model for the boundary conditions
n_fixed = model.get_node_from_coordinates([5000, 0, 0, ], 10)
n_roller = model.get_node_from_coordinates([0, 0, -5000], 10)
n_load = model.get_node_from_coordinates([0, 3000, 0, ], 10)

# Define sets for boundary conditions and loads
# model.add_instance_set(NodesGroup(name='fixed', selection=[n_fixed['part-1']], stype='nset'), instance='part-1-1')
# model.add_instance_set(NodesGroup(name='roller', selection=[n_roller['part-1']], stype='nset'), instance='part-1-1')
# model.add_instance_set(NodesGroup(name='pload', selection=[n_load['part-1']], stype='nset'), instance='part-1-1')

# Assign boundary conditions to the node stes
model.add_rollerXZ_bc(name='bc_roller', part='hypar_part', nodes=[n_roller['hypar_part']])
model.add_fix_bc(name='bc_fix', part='hypar_part', nodes=[n_fixed['hypar_part']])

# model.show()

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='hypar', model=model)

# Define the analysis step
problem.add_step(GeneralStaticStep(name='gstep'))

# Assign a point load to the node set
problem.add_point_load(name='pload', step='gstep', part='hypar_part', nodes=[n_load['hypar_part']], y=-1000)

# Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))

##### --------------------- POSTPROCESS RESULTS -------------------------- #####
results = Results.from_problem(problem, fields=['u'])
pprint(results.nodal)
