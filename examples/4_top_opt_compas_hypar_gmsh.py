from compas_fea2.preprocessor.meshing import compas_to_gmsh

from compas_fea2.backends.abaqus.model import Model

from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import Set

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FixedDisplacement
from compas_fea2.backends.abaqus import RollerDisplacementXZ
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep

from compas_fea2.interfaces.viewer.viewer import OptiViewer

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
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))

# Create a shell model from a mesh
model.shell_from_gmesh(gmshModel=gmesh, shell_section=ShellSection(name='section_A', material='mat_A', t=20))

# Find nodes in the model for the boundary conditions
n_fixed_1 = model.get_node_from_coordinates([5000, 0, 0,], 10)
n_fixed_2 = model.get_node_from_coordinates([0, 0, -5000], 10)
n_load = model.get_node_from_coordinates([0, 3000, 0,], 10)

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='fixed_1', selection=[n_fixed_1['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='fixed_2', selection=[n_fixed_2['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[n_load['part-1']], stype='nset'), instance='part-1-1')

model.summary()

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='hypar_gmsh', model=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[FixedDisplacement(name='bc_fix_1', bset='fixed_1'),
                    FixedDisplacement(name='bc_fix_2', bset='fixed_2')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', x=1000))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload']))

# Define the optimisation parameters
problem.set_optimisation_parameters(0.5, 40, 10)

# Get a summary
problem.summary()

# Solve the problem
problem.optimise(path= TEMP + '/topopt_hypar_gmsh')

# Visualie results
v = OptiViewer(problem)
v.show()
