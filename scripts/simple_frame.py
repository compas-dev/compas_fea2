from compas_fea2.backends.abaqus.components import Node
from compas_fea2.backends.abaqus.components import Concrete
from compas_fea2.backends.abaqus.components import ElasticIsotropic
from compas_fea2.backends.abaqus.components import BoxSection
from compas_fea2.backends.abaqus.components import SolidSection
from compas_fea2.backends.abaqus.components import BeamElement
from compas_fea2.backends.abaqus.components import SolidElement
from compas_fea2.backends.abaqus.components import FixedDisplacement
from compas_fea2.backends.abaqus.components import RollerDisplacementXZ
from compas_fea2.backends.abaqus.components import Part
from compas_fea2.backends.abaqus.components import Set
from compas_fea2.backends.abaqus.components import Assembly
from compas_fea2.backends.abaqus.components import Instance
from compas_fea2.backends.abaqus.components import GeneralStaticStep
from compas_fea2.backends.abaqus.components import PointLoad
from compas_fea2.backends.abaqus.components import FieldOutput

from compas_fea2.backends.abaqus import Structure

# Initialise the assembly object
model = Assembly(name='structural_model')

# Add a Part to the model
model.add_part(Part(name='part-1'))
# Add nodes to the part
for x in range(0, 1100, 100):
    model.add_node(Node([x, 0.0, 0.0]), 'part-1')
for y in range(100, 600, 100):
    model.add_node(Node([x, y, 0.0]), 'part-1')
for x in range(900, -100, -100):
    model.add_node(Node([x, y, 0.0]), 'part-1')
for y in range(400, 0, -100):
    model.add_node(Node([x, y, 0.0]), 'part-1')


# Define materials
mat1 = ElasticIsotropic(name='mat1', E=29000, v=0.17, p=2.5e-9)
mat2 = ElasticIsotropic(name='mat2', E=25000, v=0.17, p=2.4e-9)

# Define sections
section_A = BoxSection(name='section_A', material=mat2, a=20, b=80, t1=5, t2=5, t3=5, t4=5)
section_B = BoxSection(name='section_B', material=mat2, a=50, b=100, t1=5, t2=5, t3=5, t4=5)

# Generate elements between nodes
elements = []
for e in range(len(model.parts['part-1'].nodes)-1):
    elements.append((BeamElement([e, e+1], section_B)))
model.add_elements(elements, 'part-1')
model.add_element(BeamElement([29, 0], section_A, elset='test'), 'part-1')

# Define sets for boundary conditions and loads
model.add_assembly_set(Set('fixed', [0], 'nset'), 'part-1-1')
model.add_assembly_set(Set('roller', [10],'nset'), 'part-1-1')
model.add_assembly_set(Set('pload', [20], 'nset'), 'part-1-1')
# sets = [nset_fixed, nset_roller, nset_pload]
# nset_fixed = Set('fixed', [0])
# nset_roller = Set('roller', [10])
# nset_pload = Set('pload', [20])
# sets = [nset_fixed, nset_roller, nset_pload]

# # Create an instance of the part
# instance1 = Instance(name='test_instance', part=part1, sets=sets)

# # Build the assembly
# assembly = Assembly(name='assembly', instances=[instance1])

# Assign boundary conditions to the node stes
bc1 = RollerDisplacementXZ('bc_roller', model.sets['roller'])
bc2 = FixedDisplacement('bc_fix', model.sets['fixed'])

# Assign a point load to the node set
pload1 = PointLoad('pload1', model.sets['pload'], y=-1000)

# Define the field outputs required
fout = FieldOutput('my_fout')

# Define the analysis step
step = GeneralStaticStep('gstep', loads=[pload1], field_output=[fout])

# Create the Structure object
my_structure = Structure('test_structure')

my_structure.set_assembly(model)
my_structure.add_bcs([bc1, bc2])
my_structure.add_step(step)
# Analyse the structure
# my_structure.write_input_file(path='C:/temp/test_structure')
my_structure.analyse(path='C:/temp/test_structure')
