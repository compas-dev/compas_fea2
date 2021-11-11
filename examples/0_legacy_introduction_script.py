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
from compas_fea2.backends.abaqus import Set

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import PinnedDisplacement
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import GravityLoad
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
model.add_node(Node(xyz=[-5., -5., 0.]), part='part-1')
for node in [[5., -5., 0.], [5., 5., 0.], [-5., 5., 0.], [0., 0., 5.]]:
    model.add_node(Node(xyz=node), part='part-1')
# Define materials
model.add_material(ElasticIsotropic(name='mat_elastic', E=10*10**9, v=0.3, p=1500))

# Define sections
model.add_section(CircularSection(name='sec_circ', material='mat_elastic', r=0.010))
model.add_section(ShellSection(name='sec_shell', material='mat_elastic', t=0.005))

# Generate elements between nodes
elements = []
for conn in [[0, 4], [1, 4], [2, 4], [3, 4]]:
    elements.append((BeamElement(connectivity=conn, section='sec_circ')))
model.add_elements(elements=elements, part='part-1')
model.add_element(element=ShellElement(connectivity=[0, 1, 4], section='sec_shell'), part='part-1')

# Define sets for boundary conditions and loads
model.add_instance_set(Set(name='nset_base', selection=[0, 1, 2, 3], stype='nset'), instance='part-1-1')
model.add_instance_set(Set(name='nset_top', selection=[4], stype='nset'), instance='part-1-1')
model.add_instance_set(Set(name='elset_beams', selection=[0, 1, 2, 3], stype='elset'), instance='part-1-1')
model.add_instance_set(Set(name='elset_shell', selection=[4], stype='elset'), instance='part-1-1')
model.summary()
print(model)

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='test_structure', model=model)

# Assign boundary conditions to the node stes
problem.add_bc(PinnedDisplacement(name='disp_pinned', bset='nset_base'))

# Assign a point load to the node set
problem.add_load(PointLoad(name='load_point', lset='nset_top', x=10000, z=-10000))
problem.add_load(GravityLoad(name='load_gravity'))

# Define the field outputs required
problem.add_field_output(fout=FieldOutput(name='fout'))

# Define the analysis step
problem.add_step(GeneralStaticStep(name='gstep', loads=['load_point', 'load_gravity']))

# Solve the problem
problem.summary()
problem.analyse(path=Path(TEMP).joinpath(problem.name))

##### --------------------- POSTPROCESS RESULTS -------------------------- #####
results = Results.from_problem(problem, fields=['u'])
pprint(results.nodal)
