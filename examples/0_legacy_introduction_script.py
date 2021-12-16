import inspect
from pathlib import Path
from pprint import pprint
from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import CircularSection
from compas_fea2.backends.abaqus import BeamElement
from compas_fea2.backends.abaqus import ShellElement
from compas_fea2.backends.abaqus import RollerBCXY

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import GravityLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep
from compas_fea2.backends.abaqus import GeneralDisplacement

from compas_fea2.backends.abaqus import Results

from compas_fea2 import TEMP
from compas_fea2.backends.abaqus.model import nodes

##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model')

# Add a Part to the model
model.add_part(Part(name='part-1'))

# Add nodes to the part
model.add_node(Node(xyz=[0., 0., 5.]), part='part-1')
nodes = [[5., -5., 0.], [5., 5., 0.], [-5., 5., 0.], [-5., -5., 0.]]
model.add_nodes([Node(xyz=node) for node in nodes], part='part-1')

# Define materials
model.add_material(ElasticIsotropic(name='mat_elastic', E=10*10**9, v=0.3, p=1500))

# Define sections
model.add_section(CircularSection(name='sec_circ',    material='mat_elastic', r=0.010))

# Generate elements between nodes
connectivity = [[0, i] for i in range(1, 5)]
model.add_elements([BeamElement(connectivity=conn, section='sec_circ') for conn in connectivity], part='part-1')

# Assign boundary conditions (3 pins and a rollerXY)
# approach 1: driectly from model
model.add_bc_type(name='bc_pinned', bc_type='fix', part='part-1', nodes=[1])
model.add_pin_bc(name='bc_pinned', part='part-1', nodes=[2, 3, 4])
# approach 2: using a class
# roller = RollerBCXY(name='bc_roller')  # TODO in this case it would be better to assing nodes and part to the object...
# model.add_bc(roller, part='part-1', nodes=[4])

# Review
model.summary()
# model.show()


##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='test_structure', model=model)

# Approach 1: Create a step and assign a gravity load
step_0 = GeneralStaticStep(name='step_pload_0')
step_0.add_gravity_load()
problem.add_step(step_0)

# Approach 2: Add a step and define a point load directly from Problem
problem.add_step(GeneralStaticStep(name='step_pload_1'))
problem.add_point_load(name='load_point', x=10000, z=-10000, nodes=[0], part='part-1', step='step_pload_1')

# Define the field outputs required
fout = FieldOutput(name='fout')
problem.add_output(fout, step_0)

# Review
problem.summary()
problem.show()

# Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))

##### --------------------- POSTPROCESS RESULTS -------------------------- #####
results = Results.from_problem(problem, fields=['u'])
pprint(results.nodal)
