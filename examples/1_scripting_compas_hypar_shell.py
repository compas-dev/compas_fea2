from compas.datastructures import Mesh

from compas_fea2.backends.abaqus.model import Model
from compas_fea2.backends.abaqus.model import ElasticIsotropic
from compas_fea2.backends.abaqus.model import ShellSection
from compas_fea2.backends.abaqus.model import Set

from compas_fea2.backends.abaqus.problem import Problem
from compas_fea2.backends.abaqus.problem import FixedDisplacement
from compas_fea2.backends.abaqus.problem import RollerDisplacementXZ
from compas_fea2.backends.abaqus.problem import PointLoad
from compas_fea2.backends.abaqus.problem import FieldOutput
from compas_fea2.backends.abaqus.problem import GeneralStaticStep

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
shell_20 = ShellSection(name='section_A', material='mat_A', t=20)

# Create a shell model from a mesh
model.shell_from_mesh(mesh=mesh, shell_section=shell_20)

# Find nodes in the model for the boundary conditions
n_fixed = model.get_node_from_coordinates([5000, 0, 0,], 10)
n_roller  = model.get_node_from_coordinates([0, 0, -5000], 10)
n_load = model.get_node_from_coordinates([0, 3000, 0,], 10)

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='fixed', selection=[n_fixed['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='roller', selection=[n_roller['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[n_load['part-1']], stype='nset'), instance='part-1-1')

# model.summary()

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='hypar', model=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[RollerDisplacementXZ(name='bc_roller', bset='roller'),
                        FixedDisplacement(name='bc_fix', bset='fixed')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', y=-1000))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload']))

# Solve the problem
# problem.write_input_file(path='C:/temp/test_structure')
# problem.summary()
problem.analyse(path= TEMP + '/hypar_shell')
problem.extract()
print(problem.results)
