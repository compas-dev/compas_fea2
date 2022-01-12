from pathlib import Path
from pprint import pprint

from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import BoxSection
from compas_fea2.backends.abaqus import BeamElement
from compas_fea2.backends.abaqus import NodesGroup

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FixedBC
from compas_fea2.backends.abaqus import RollerBCXZ
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep

from compas_fea2.backends.abaqus import Results

from compas_fea2 import TEMP
##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model')

# Add a Part to the model
model.add_part(Part(name='part-1'))

# Add nodes to the part
for x in range(0, 1100, 100):
    model.add_node(Node(xyz=[x, 0.0, 0.0]), part='part-1')
for y in range(100, 600, 100):
    model.add_node(Node(xyz=[x, y, 0.0]), part='part-1')
for x in range(900, -100, -100):
    model.add_node(Node(xyz=[x, y, 0.0]), part='part-1')
for y in range(400, 0, -100):
    model.add_node(Node(xyz=[x, y, 0.0]), part='part-1')

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))

# Define sections
model.add_section(BoxSection(name='section_A', material='mat_A', a=20, b=80, t=5))

# Generate elements between nodes
elements = []
for e in range(len(model.parts['part-1'].nodes)-1):
    elements.append(BeamElement(connectivity=[e, e+1], section='section_A'))
elements.append(BeamElement(connectivity=[len(model.parts['part-1'].nodes)-1, 0], section='section_A'))
model.add_elements(elements=elements, part='part-1')

# # Define groups for boundary conditions and loads
# model.add_nodes_group(name='fixed', nodes=[0],  part='part-1')
# model.add_nodes_group(name='roller', nodes=[10], part='part-1')
# model.add_nodes_group(name='pload', nodes=[20], part='part-1')

# Assign boundary conditions to the node stes
model.add_fix_bc('fixed', 'part-1', [0])
model.add_rollerXZ_bc('roller', 'part-1', [10])

# model.show()

##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='test_structure', model=model)

# Define the analysis step
problem.add_step(GeneralStaticStep(name='step-1'))

# Assign a point load to the node set
problem.add_point_load(name='pload', step='step-1', part='part-1', nodes=[5], y=-1000)

# Define the field outputs required
# problem.add_field_output(fout=FieldOutput(name='fout'), )

# Review
problem.summary()
problem.show()

# # Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))

##### --------------------- POSTPROCESS RESULTS -------------------------- #####
results = Results.from_problem(problem, fields=['u'])
pprint(results.nodal)
