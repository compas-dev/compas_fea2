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
# model = Assembly(name='structural model')

# Define materials
mat1 = ElasticIsotropic(name='mat1', E=29000, v=0.17, p=2.5e-9)
mat2 = ElasticIsotropic(name='mat2', E=25000, v=0.17, p=2.4e-9)

# Define sections
section_A = SolidSection(name='section_A', material=mat1)
section_B = BoxSection(name='section_B', material=mat2, a=50, b=100, t1=5, t2=5, t3=5, t4=5)

# Generate nodes
nodes = []
c=1
for x in range(0,1100,100):
    nodes.append(Node(c,[x, 0.0, 0.0]))
    c+=1
for y in range(100,600,100):
    nodes.append(Node(c,[x, y, 0.0]))
    c+=1
for x in range(900,-100,-100):
    nodes.append(Node(c,[x, y, 0.0]))
    c+=1
for y in range(400,0,-100):
    nodes.append(Node(c,[x, y, 0.0]))
    c+=1

# Generate elements between nodes
elements = []
c=1
for e in range(len(nodes)-1):
    elements.append(BeamElement(c, [nodes[e], nodes[e+1]], section_B))
    c+=1
elements.append(BeamElement(c, [nodes[len(nodes)-1], nodes[0]], section_B))

# Assign nodes and elements to a part
part1 = Part(name='part-1', nodes=nodes, elements=elements)

# Define sets for boundary conditions and loads
nset_fixed = Set('fixed', [nodes[0]])
nset_roller = Set('roller', [nodes[10]])
nset_pload = Set('pload', [nodes[20]])
sets = [nset_fixed, nset_roller, nset_pload]

# Create an instance of the part
instance1 = Instance(name='test_instance', part=part1, sets=sets)

# Build the assembly
assembly = Assembly(name='part-1', instances=[instance1])

# Assign boundary conditions to the node stes
bc1 = RollerDisplacementXZ('bc_roller',nset_roller)
bc2 = FixedDisplacement('bc_fix', nset_fixed)

# Assign a point load to the node set
pload1 = PointLoad('pload1', nset_pload, y=-1000)

# Define the field outputs required
fout = FieldOutput('my_fout')

# Define the analysis step
step = GeneralStaticStep('gstep', loads=[pload1], field_output=[fout])

# Create the Structure object
my_structure = Structure('test_structure', [part1], assembly, [], [bc1, bc2], [step])

# Analyse the structure
# my_structure.write_input_file(path='C:/temp/test_structure')
my_structure.analyse(path='C:/temp/test_structure')
